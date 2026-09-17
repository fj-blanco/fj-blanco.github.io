---

title: Native ROS 2 on Zephyr
description: Running the normal ROS 2 C stack directly on an ESP32-S3 using Zephyr and Cyclone DDS.
date: 2026-09-16
permalink: /notes/ros2-zephyr/
------------------------------

<header class="article-header">

  <h1>Native ROS 2 on Zephyr</h1>

  <p class="byline">

```
<strong>Javier Blanco-Romero</strong><br>

Researcher at Universidad Carlos III de Madrid<br>

<time datetime="2026-09-16">16 September 2026</time>
```

  </p>

<a class="repo-link" href="https://github.com/servoagents/ros2_zephyr">Code on GitHub <span aria-hidden="true">→</span></a>

</header>

I have been spending some time exploring different ways of running ROS 2 on embedded devices.

Most of it started around [micro-ROS](https://github.com/micro-ROS) and Zephyr. I have also been experimenting with the Zephyr integration of [rmw_zenoh_pico](https://github.com/esol-community/rmw_zenoh_pico), including an ESP32 example using `rclc` over Zenoh-Pico. That work is being discussed in [rmw_zenoh_pico issue #8](https://github.com/esol-community/rmw_zenoh_pico/issues/8).

In the usual Micro XRCE-DDS setup, the microcontroller runs a lightweight XRCE client and connects to a Micro XRCE-DDS Agent on a more capable machine. The Agent bridges that client into the DDS/ROS 2 network.

While working on those paths I also wanted to try direct DDS. If the microcontroller has enough RAM and networking support, it should in principle be possible for it to participate directly in DDS instead of putting an XRCE Agent or another protocol hop in between.

I started with [Eclipse Cyclone DDS](https://github.com/eclipse-cyclonedds/cyclonedds). Cyclone already had some Zephyr support, but using it on current Zephyr versions and on an ESP32-S3 exposed a few portability and resource issues. I have been testing the ongoing [Cyclone DDS Zephyr PR #2461](https://github.com/eclipse-cyclonedds/cyclonedds/pull/2461) and shared a couple of small follow-up fixes from this work.

Once direct DDS was working, I started putting the ROS layer on top.

The project is split into two repositories with different roles. A fair amount of this was done by button-pushing GPT-5.6 Sol High and then checking what actually happens on the board.

[ros2_zephyr](https://github.com/servoagents/ros2_zephyr) is the Zephyr integration and build layer. It pins the ROS 2, Zephyr and Cyclone DDS versions used by the project, cross-compiles the selected ROS packages into static firmware libraries, exposes the Zephyr CMake and Kconfig integration, and keeps the platform-specific compatibility code and hardware samples in one place.

[rmw_cyclonedds_c](https://github.com/servoagents/rmw_cyclonedds_c) is the middleware repository. It contains two ROS packages. `rmw_cyclonedds_c` implements the standard RMW C API and maps ROS publishers, subscriptions, waits and QoS onto Cyclone DDS. `rosidl_typesupport_cyclonedds_c` generates the DDS type descriptions and the field-by-field conversions used by ROS C message types.

I did not try to port `rmw_cyclonedds_cpp` directly. It is useful as a reference for ROS/DDS behavior, but its architecture is aimed at a full ROS 2 environment, with dynamic type construction, introspection and a broader runtime setup. For the embedded version I wanted a smaller profile with static linking, generated C type support, explicit resource ownership, fixed-size messages and no runtime RMW plugin loading.

The application side still uses normal ROS 2 C APIs.

```text
rclc -> rcl -> rmw_cyclonedds_c -> Cyclone DDS -> Zephyr
```

Keeping the middleware separate from the Zephyr integration also makes it possible to test the ROS/DDS behavior on Linux first, before adding RTOS, cross-compilation and hardware-specific variables.

I tested the complete stack over Wi-Fi against an unmodified ROS 2 Lyrical machine using `rmw_cyclonedds_cpp`. The ESP32-S3 can publish directly to a desktop ROS 2 subscriber and subscribe directly to a desktop publisher.

There is no Micro XRCE-DDS Agent in between. The board is a normal DDS/RTPS participant.

The current profile is still small. It uses fixed-size messages and best-effort QoS. I tested `std_msgs/msg/UInt32` at 1, 10 and 100 Hz in both directions.

The complete subscriber firmware uses 1,016,132 bytes of flash. A direct Cyclone DDS version of the same experiment uses 913,700 bytes. In this build, keeping `rclc`, `rcl` and the RMW adds about 100 kB, or 11.2%, to the flash footprint.

The subscriber uses about 258 kB of linked DRAM. The publisher is slightly smaller in flash, at about 940 kB, with almost the same DRAM use.

Most of the debugging ended up being about resource sizing. At one point the board discovered the desktop participant but stopped during endpoint discovery. Packet captures initially pointed towards retransmission or Wi-Fi. JTAG tracing later showed that one of Cyclone's builtin discovery workers was using more stack than we had reserved. During discovery it used a little over 6 kB and crossed into the adjacent thread stack, corrupting saved execution state. Moving the Cyclone workers to 8 kB fixed that problem.

That exposed another limit. The configured Zephyr POSIX mutex pool was also too small for the number of DDS objects created while processing the endpoints advertised by a normal ROS 2 peer. The direct DDS experiment worked with 192 mutex slots, while the complete ROS node needed 256. Increasing the pool removed that limit.

With those resource limits adjusted, normal DDS discovery worked. No RTPS change and no Wi-Fi driver workaround were needed.

The final firmware has 12 threads and reserves about 70 kB of thread stack in total. The busiest Cyclone worker, `dq.builtins`, used around 7.7 kB of its 8 kB allocation during the accepted tests. The application thread also came fairly close to its 12 kB limit.

A few upstream issues also came up during the work.

Zephyr 4.4.0 through 4.4.2 have a `pthread_cond_timedwait()` issue where the mutex is not reacquired after a timeout. The fix already exists on Zephyr `main`. I opened [Zephyr issue #119029](https://github.com/zephyrproject-rtos/zephyr/issues/119029) and [PR #119030](https://github.com/zephyrproject-rtos/zephyr/pull/119030) to backport the existing fix and regression test to the 4.4 stable branch.

While moving the ROS side to Lyrical I found a separate XTypes mismatch in `rmw_cyclonedds_cpp`. Generated ROS-to-DDS IDL uses member names such as `data_`, while the dynamic type path used the introspection name `data`. I opened [ros2/rmw_cyclonedds#604](https://github.com/ros2/rmw_cyclonedds/pull/604) with a small fix and regression test. It is still a draft because patched and unpatched processes advertise different TypeInformation.

At this point I have three embedded ROS 2 paths that I want to keep exploring with the same `rclc` application model:

* [Micro XRCE-DDS](https://github.com/micro-ROS/rmw_microxrcedds), with the usual client/Agent setup.
* [rmw_zenoh_pico](https://github.com/esol-community/rmw_zenoh_pico), which I have been testing on Zephyr and ESP32.
* Native DDS through `rmw_cyclonedds_c`.

They make different trade-offs in memory, discovery, routing and deployment. The useful part is that the application can stay on the same ROS 2 C API.

The next step for `rmw_cyclonedds_c` is Reliable QoS, followed by Transient Local and enough graph support for normal ROS 2 tools to see the embedded node. Later I would like to run the same application through XRCE-DDS, Zenoh-Pico and Cyclone DDS on the same hardware and compare memory use, discovery traffic, latency, jitter, throughput and energy.

For now, the result is fairly narrow. A normal ROS 2 C node can run on an ESP32-S3 under Zephyr and exchange messages directly with stock ROS 2 over Cyclone DDS, without an Agent.

All the integration code is available at **[servoagents/ros2_zephyr](https://github.com/servoagents/ros2_zephyr)** and the middleware implementation at **[servoagents/rmw_cyclonedds_c](https://github.com/servoagents/rmw_cyclonedds_c)**.

## Technical appendix

The hardware acceptance test used an ESP32-S3-DevKitC, Zephyr 4.4.2, Zephyr SDK 1.0.1 and ROS 2 Lyrical on the desktop.

The tested middleware profile is best-effort, volatile and keep-last. It currently supports scalar, fixed-array and nested fixed-size messages. Reliable QoS, variable-size messages, services, actions, DDS Security and a complete remote graph are not yet supported.

The accepted Wi-Fi configuration uses five 8,192-byte Cyclone worker stacks, 256 POSIX mutex slots and 96 condition-variable slots.

| Thread             | Reserved | Subscriber used | Publisher used |
| ------------------ | -------: | --------------: | -------------: |
| `recv`             |  8,192 B |         3,984 B |        1,792 B |
| `tev`              |  8,192 B |         3,584 B |        3,408 B |
| `dq.user`          |  8,192 B |           528 B |          528 B |
| `dq.builtins`      |  8,192 B |         7,696 B |        7,696 B |
| `gc`               |  8,192 B |         4,096 B |        4,096 B |
| application `main` | 12,288 B |        11,312 B |       11,264 B |

The subscriber image uses 1,016,132 bytes of flash and 258,072 bytes of linked DRAM. The publisher uses 939,508 bytes of flash and 258,064 bytes of linked DRAM.

The measured DDS allocator peak was around 100 kB. The ROS allocator stayed below 1 kB in these tests. These figures do not include all kernel, network-driver, libc or static memory.

There is also one ESP32-specific build detail. Upstream `rclc` links its action paths into the executor library even when the application only uses pub/sub. This pulls in `rcl_action`, whose UUID helper uses `rand()`. On this build that also pulls Picolibc's `random()` into the image, where it conflicts with the function of the same name in the Espressif Wi-Fi adapter. `ros2_zephyr` currently provides a small `rand()`/`srand()` compatibility shim only for ESP32 Wi-Fi builds.

The 1/10/100 Hz runs are functional tests. The observed packet intervals show batching and should not be interpreted as one-way latency measurements.
