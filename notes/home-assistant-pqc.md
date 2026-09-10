---
title: Post-Quantum TLS in Home Assistant
description: An experiment tracing post-quantum TLS across Home Assistant HTTP, MQTT, and gRPC paths.
date: 2026-09-10
permalink: /notes/home-assistant-pqc/
---

<header class="article-header">
  <h1>Post-Quantum TLS in Home Assistant</h1>
  <p class="byline">
    <strong>Javier Blanco-Romero</strong><br>
    Researcher at Universidad Carlos III de Madrid<br>
    <time datetime="2026-09-10">10 September 2026</time>
  </p>
  <a class="repo-link" href="https://github.com/perlab-uc3m/home-assistant-pqc">Code on GitHub <span aria-hidden="true">→</span></a>
</header>

I am preparing a [Home Assistant](https://github.com/home-assistant/core) installation at home, and at some point I wondered how ready the system already was for post-quantum cryptography. I initially expected to find some place where ML-KEM or another post-quantum primitive could be added to Home Assistant itself. Instead, much of the transition had already happened below the application layer.

Home Assistant does not use a single communication stack. The path depends mainly on the integration and on how the device or service exposes its API. Many cloud and local integrations use HTTPS through aiohttp or httpx, while some integrations such as [Starlink](https://www.home-assistant.io/integrations/starlink/) use gRPC internally. MQTT is more explicit and users configure a broker for devices and services that communicate through [MQTT](https://www.home-assistant.io/integrations/mqtt/). Local smart-home devices may instead use [Matter](https://www.home-assistant.io/integrations/matter/), [Zigbee](https://www.home-assistant.io/integrations/zha/), [Z-Wave](https://www.home-assistant.io/integrations/zwave_js/), or [Bluetooth](https://www.home-assistant.io/integrations/bluetooth/), depending on the protocol supported by the device and the available radio hardware.

For the TLS paths considered here, the structure is roughly:

```text
aiohttp / httpx ──> Python ssl ──> OpenSSL
MQTT ──> Paho ────> Python ssl ──> OpenSSL
gRPC ─────────────> grpcio ──────> bundled TLS stack
```

These paths do not all follow the same TLS policy.

I used GPT-5.6 Sol to help me explore the code and put the tests together, then ran the experiments against the official Home Assistant images and captured the actual TLS `ClientHello` messages. Home Assistant 2026.9.1 contains Python 3.14.6 linked against OpenSSL 3.5.7.

[OpenSSL 3.5](https://docs.openssl.org/3.5/man3/SSL_CTX_set1_curves/) implements `X25519MLKEM768`, the hybrid TLS 1.3 group standardized in [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024.html). It combines X25519 with ML-KEM-768. OpenSSL includes it in its default TLS group list and sends it as one of the initial key shares.

Home Assistant does not explicitly request that group. Its usual Python TLS paths inherit the OpenSSL defaults, and the packets show that the hybrid key exchange is already there.

| Path        | Home Assistant 2026.9.1   | Development image, 2026-09-09 |
| ----------- | ------------------------- | ----------------------------- |
| Python HTTP | `X25519MLKEM768 + X25519` | `X25519MLKEM768 + X25519`     |
| MQTT / Paho | `X25519MLKEM768 + X25519` | `X25519MLKEM768 + X25519`     |
| gRPC        | P-256                     | `X25519MLKEM768 + X25519`     |

The Python result was the same for a standard Python SSL context, Home Assistant's own client context, aiohttp, httpx, and Paho MQTT. Each advertised the same OpenSSL group set and sent two initial key shares, `X25519MLKEM768` and X25519. The X25519 share provides classical fallback when the peer does not support the hybrid group.

gRPC behaved differently in the released image. Home Assistant 2026.9.1 contains grpcio 1.78.0, whose wheel carries its own TLS libraries instead of using the OpenSSL library linked to Python. Its `ClientHello` advertised only P-256 for key exchange and sent only a P-256 share. It was 303 bytes, compared with roughly 1.5 kB for the Python/OpenSSL `ClientHello` carrying the hybrid share.

I repeated the same experiment with a Home Assistant development image from September 9. It contains grpcio 1.83.1. Its gRPC `ClientHello` had grown to 1,504 bytes and now advertised `X25519MLKEM768` together with X25519.

**The change came from a dependency update, not from a new Home Assistant cryptographic implementation.**

[Bas Westerbaan made a similar point recently](https://x.com/bwesterb/status/2097787901408932289). Commenting on a [post-quantum readiness survey](https://github.com/xuxu298/PQReadinessIndex), he joked that *"Who installs software updates by sector"* might be a better title. The Home Assistant result is a good example. Part of the current TLS transition happens because the software below the application is updated. The Python paths inherited `X25519MLKEM768` from OpenSSL, while gRPC gained it later through grpcio.

Key exchange is only one part of TLS, so I also checked authentication. `X25519MLKEM768` protects the key exchange, while certificate authentication and the TLS `CertificateVerify` signature are separate. The tested Python/OpenSSL paths advertise the three ML-DSA signature schemes and completed TLS 1.3 handshakes using `X25519MLKEM768` together with ML-DSA-65 authentication. The Home Assistant HTTPS server context also loaded an ML-DSA-65 certificate and completed the same type of handshake.

The gRPC results show the transition in two steps. grpcio 1.78.0 already supports ML-DSA-65 authentication, but still uses P-256 for key exchange. grpcio 1.83.1 combines ML-DSA-65 authentication with `X25519MLKEM768`. Again, no Home Assistant source change was required.

ML-DSA certificates are standardized in [RFC 9881](https://www.rfc-editor.org/rfc/rfc9881.html), but the use of ML-DSA signatures in TLS 1.3 is still defined by the [IETF ML-DSA TLS draft](https://datatracker.ietf.org/doc/draft-ietf-tls-mldsa/). The ML-DSA tests here are therefore interoperability experiments, not a production deployment recommendation.

This makes "PQC-ready" a less simple label than it may sound. Key exchange and authentication can move at different times, and two connections from the same application can use different cryptographic policies because different libraries own them.

I also checked that the result was not just coming from version numbers. I used an OpenSSL configuration that removed ML-KEM from the available TLS groups. The affected paths stopped offering `X25519MLKEM768`, and the assurance probes failed as expected. The tests therefore check the TLS behavior seen on the wire, not only the installed library version.

MQTT was tested end to end as well. A complete Home Assistant `MqttClientSetup` → Paho → TLS 1.3 → [Mosquitto](https://github.com/eclipse-mosquitto/mosquitto) path subscribed to a topic, published a QoS 1 message, and received the expected payload. The separate Paho `ClientHello` capture shows the hybrid and classical key shares, while the application test confirms that this is the path used by a working Home Assistant MQTT connection.

This does not mean that Home Assistant as a whole is post-quantum secure. The experiments here concern TLS. Home Assistant also communicates with local devices through Matter, Zigbee, Z-Wave, and Bluetooth, which use their own security mechanisms. Their public-key authentication or key-establishment mechanisms will need their own post-quantum transition. Updating OpenSSL can move an important part of Home Assistant's TLS traffic to post-quantum cryptography, but it does not move the whole smart-home stack.

The main result is that much of Home Assistant's post-quantum TLS support already comes from the libraries below it. Rather than adding another crypto layer, a useful contribution may simply be to test that official images keep this capability as OpenSSL, grpcio, and other dependencies change.

All the code is available at **[perlab-uc3m/home-assistant-pqc](https://github.com/perlab-uc3m/home-assistant-pqc)**.
