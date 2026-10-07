# Causal-Exclusion Authentication in Quantum Field Theory

Javier Blanco-Romero and Florina Almenares Mendoza

Department of Telematic Engineering, Universidad Carlos III de Madrid, Leganés, Madrid, Spain

Work in progress. Results and proofs remain under review.

Abstract {#abstract .unnumbered}
--------

A receiver can test whether a field signal required access to her side of a causal cut, without sharing any secret with the source. The field starts in a known reference state, such as the vacuum, and the forger can act only on the far side of the cut. Her operations then commute with everything the receiver measures, so all she can do is choose which runs to keep. For any acceptance test, the probability that she attempts a forgery and the test accepts is therefore at most the test\'s acceptance rate on the untouched reference state, even with quantum memory, postselection, and collective attacks. Repetition separates honest signals from forgeries at an optimal rate given by the Araki relative entropy of the two states on the receiver\'s observables. For a coherent pulse of the chiral current this rate is the pulse energy weighted by its distance from the cut, so it grows as the pulse moves away. A detector of fixed size carried along with the pulse does not see this growth.

Introduction {#sec:intro}
------------

Authentication usually rests on something the forger lacks, typically a secret key. Relativity offers another thing she may lack, namely access to a region of spacetime. Picture a verifier who receives a field signal and asks a modest question. Did preparing this signal require access to her side of a causal cut, or could someone confined to the other side have produced it?

Quantum field theory answers through locality. Observables of causally disjoint regions commute \[[1](#ref-haag1964algebraic)\], so an operation on the excluded side cannot change the statistics of anything the verifier measures. The forger\'s only lever is selection, keeping some runs and discarding others. That can raise the verifier\'s acceptance rate on the kept runs, but never the joint probability that a forgery was attempted and accepted, because the two events are compatible and their conjunction is never more likely than acceptance alone. Starting from a prescribed reference state, the forgery probability of any test is therefore bounded by its false-positive rate $q$ on the undisturbed reference,

$$p_{\mathrm{forge}}\le q .$$

For the vacuum this rate cannot vanish, since by the Reeh-Schlieder theorem every nonzero local test fires on the vacuum with positive probability \[[2](#ref-reeh1961bemerkungen), [3](#ref-witten2018aps)\]. Authentication has to be statistical, and repetition suppresses forgery at a rate set by quantum hypothesis testing, the Araki relative entropy between the honest and reference states as seen by the verifier. For the chiral current on a light ray cut at the origin, with the verifier on the side $u<0$, a coherent pulse with energy density $\rho_f(u)$ gives the rate

$$D=2\pi\int_{-\infty}^0|u|\,\rho_f(u)\,du ,$$

its energy weighted by $2\pi$ times the null distance from the cut. A pulse far from the cut stands out against a colder vacuum, an advantage only measurements that use the whole half-line can exploit.

Related relativistic primitives, such as spacetime secret sharing \[[4](#ref-hayden2019localizing)\] and relativistic state and position verification \[[5](#ref-kent2014secure), [6](#ref-kent2011quantum), [7](#ref-chandran2009position), [8](#ref-buhrman2014position)\], constrain where an unknown system or response can be produced. Here signal and test are public, and the hypothesis rejected is that the state came from a prescribed reference through operations in the excluded region. The ingredients are established, and our contribution is to assemble them into an access test with a geometric rate. Such a test could complement the preshared key that authenticates the classical channel of quantum key distribution \[[9](#ref-bennett1984quantum)\], wherever the geometry of the laboratories is known and trusted.

Section [2](#sec:primitive) treats one run and proves the soundness bound. Section [3](#sec:amplification) treats repetition and the optimal rate, and Sec. [4](#sec:current) computes that rate for a pulse of the chiral current and compares it with a detector of fixed size. Section [5](#sec:limits) states precisely what an acceptance certifies.

One run {#sec:primitive}
-------

### Observables and regions

Quantum observables are operators on a Hilbert space $\mathcal{H}$. We write $B(\mathcal{H})$ for the bounded operators on $\mathcal{H}$, $X^*$ for the adjoint of $X$, $\|X\|$ for the operator norm, and $\mathbf{1}$ for the identity; logarithms are natural. The operations available to one party form an algebra, because sums, products, and adjoints of accessible operators are again accessible. A von Neumann algebra is such an algebra of bounded operators that contains the identity and is closed under weak limits. It is the standard model for the observables of a spacetime region in quantum field theory \[[1](#ref-haag1964algebraic)\]. The forger controls a von Neumann algebra $\mathcal{M}$ and the verifier a von Neumann algebra $\mathcal{N}$.

The commutant of $\mathcal{M}$,

$$\mathcal{M}'=\{X\in B(\mathcal{H}):XA=AX\ \text{for all}\ A\in\mathcal{M}\},$$

collects every bounded operator that commutes with all of the forger\'s operators. Locality enters through a single inclusion,

`<a id="eq:commuting-algebras"></a>`{=html} $$\mathcal{N}\subseteq\mathcal{M}'.

\tag{1}$$

In field theory $\mathcal{M}$ and $\mathcal{N}$ are the algebras of two causally disjoint regions, and Einstein causality says that their observables commute, which is exactly Eq. [(1)](#eq:commuting-algebras). Operationally, commuting observables can be measured in either order with the same joint statistics, and an operation localized on one side cannot change the statistics of the other.

### The test and the honest signal

Each run starts from a unit vector $\Omega\in\mathcal{H}$, the reference state, for instance the vacuum. For any $X\in B(\mathcal{H})$,

$$\omega_0(X)=\langle\Omega,X\Omega\rangle$$

is its expectation value in the reference state.

The verifier ends each run with a yes-or-no test. A two-outcome quantum measurement assigns to the outcome "accept" an effect $\Pi$, an operator with $0\le\Pi\le\mathbf{1}$ whose expectation value is the probability of acceptance, and to "reject" the complementary effect $\mathbf{1}-\Pi$. Effects generalize projections. A sharp measurement has $\Pi^2=\Pi$, while a noisy or coarse-grained detector has some eigenvalues strictly between zero and one. The test is performed in the verifier\'s laboratory, so $\Pi\in\mathcal{N}$.

An honest source sits on the verifier\'s side and applies a public unitary $U\in\mathcal{N}$, preparing $U\Omega$ with expectations $\omega_1(X)=\langle U\Omega,XU\Omega\rangle$. Two numbers characterize the test, its false-positive rate $q$ on the reference state and its completeness $c$ on the honest state,

`<a id="eq:q-c"></a>`{=html} $$q=\omega_0(\Pi),
\qquad
c=\omega_1(\Pi).

\tag{2}$$

### The forger

A real adversary may try many times, keep a quantum record of what she did, and keep a run only when that record looks promising. A security statement that ignored any of these moves would be fragile, so we model the forger generously. She may bring a quantum memory with Hilbert space $\mathcal{H}_{\mathrm a}$, initially uncorrelated with the field. Purifying it if necessary, we take its initial state to be a unit vector $\varphi\in\mathcal{H}_{\mathrm a}$. On the joint space $\mathcal{H}\otimes\mathcal{H}_{\mathrm a}$ the reference expectation is $\widetilde\omega_0(X)=\langle\Omega\otimes\varphi,X\,\Omega\otimes\varphi\rangle$. The verifier does not touch the memory, so her observables on the joint space are those of $\mathcal{N}$ acting on the field and the identity on the memory,

`<a id="eq:extended-reference"></a>`{=html} $$\widetilde{\mathcal{N}}=\mathcal{N}\bar\otimes\mathbb C\mathbf{1},

\tag{3}$$

where $\bar\otimes$ is the tensor product of von Neumann algebras.

The forger acts on the field and her memory, perhaps records outcomes, and keeps the run only for some of them. The cleanest description follows observables rather than states. For each joint observable $X$, let $\Phi(X)$ be the operator whose reference expectation is the expectation of $X$ after the forger\'s operation, counted only on the runs she keeps. For example, suppose she performs a measurement whose outcome $j$ maps the joint state $\psi$ to the unnormalized state $B_j\psi$, with Kraus operators $B_j$, and keeps the outcomes $j\in J$. Then

`<a id="eq:subinstrument"></a>`{=html} $$\Phi_B(X)=\sum_{j\in J}B_j^*XB_j,
\qquad
\sum_{j\in J}B_j^*B_j\le\mathbf{1},

\tag{4}$$

with the sum converging strongly. Such a map $\Phi$ is completely positive, meaning that it keeps positive operators positive even when extended to act on further systems, so that all probabilities stay nonnegative. It is normal, a continuity property shared by all physical operations. And it is subunital, $\Phi(\mathbf{1})\le\mathbf{1}$. The operator $\Phi(\mathbf{1})$ is the effect "this run is kept," and its expectation is the probability of keeping a run, which may be small. The inequality in Eq. [(4)](#eq:subinstrument) is what allows the forger to discard unfavorable outcomes.

Locality asks that the verifier\'s observables be spectators to the forger\'s operation,

`<a id="eq:bimodular"></a>`{=html} $$\Phi(N_1XN_2)=N_1\Phi(X)N_2\quad\text{for all}\ N_1,N_2\in\widetilde{\mathcal{N}},

\tag{5}$$

a property called $\widetilde{\mathcal{N}}$-bimodularity. A forger confined to her region satisfies it automatically. Her Kraus operators lie in $\mathcal{M}\bar\otimes B(\mathcal{H}_{\mathrm a})$, so by Eq. [(1)](#eq:commuting-algebras) they commute with every $N\in\widetilde{\mathcal{N}}$, and then $\sum_jB_j^*N_1XN_2B_j=N_1\bigl(\sum_jB_j^*XB_j\bigr)N_2$. We allow every normal, completely positive, subunital, bimodular map, a slightly larger class than local Kraus families, which only strengthens the forger.

### Locality soundness

What should count as a successful forgery? If the forger may discard runs, the conditional probability of acceptance on kept runs can be made large by keeping only lucky runs. The meaningful quantity is the joint probability that a run is kept and accepted, with discarded runs counted as failures.

**Theorem 1 (Locality soundness).** `<a id="thm:locality"></a>`{=html} Every normal, completely positive, subunital, $\widetilde{\mathcal{N}}$-bimodular map $\Phi$ satisfies

`<a id="eq:locality-soundness"></a>`{=html} $$p_{\mathrm{forge}}
:=\widetilde\omega_0\!\left(
\Phi(\Pi\otimes\mathbf{1})\right)
\le\omega_0(\Pi)=q.

\tag{6}$$

For the local Kraus family [(4)](#eq:subinstrument), the forgery probability is

`<a id="eq:kraus-forgery"></a>`{=html} $$p_{\mathrm{forge}}=\sum_{j\in J}
\langle\Omega\otimes\varphi,
B_j^*(\Pi\otimes\mathbf{1})B_j\,
\Omega\otimes\varphi\rangle.

\tag{7}$$

The bound is attained by doing nothing, so for a fixed test it is tight.

*Proof.* Bimodularity lets the verifier\'s effect slide through the forger\'s operation,

$$\Phi(\Pi\otimes\mathbf{1})
=(\Pi\otimes\mathbf{1})\Phi(\mathbf{1})
=\Phi(\mathbf{1})(\Pi\otimes\mathbf{1}).
\tag{8}$$

The forgery event is thus the product of two commuting effects, "accepted" and "kept." Since $0\le\Phi(\mathbf{1})\le\mathbf{1}$, this product lies below its first factor,

$$0\le\Phi(\Pi\otimes\mathbf{1})
\le\Pi\otimes\mathbf{1}.
\tag{9}$$

Taking the reference expectation gives Eq. [(6)](#eq:locality-soundness). The identity map is an allowed operation and attains $q$.

Postselection is accounted for through the joint probability. Suppose the forger\'s branch $j$ occurs with probability $p_j$ and is then accepted with probability $a_j$. The bounded quantity is $\sum_jp_ja_j$. A rare branch may well have $a_j=1$, and its rarity is exactly what keeps the total below $q$. The same bookkeeping forces every scheduled attempt to be counted. If $T$ runs each start from a fresh reference state and satisfy the assumptions conditionally on the earlier transcript, the probability of at least one false acceptance is at most $\sum_{t=1}^Tq_t$, where $q_t$ bounds the reference acceptance of run $t$ after every earlier transcript.

### From the algebra to the laboratory

Two practical issues connect the theorem to an experiment. First, $q$ is a property of the deployed test, so it can be calibrated. If $m$ independent and stationary reference runs give an empirical acceptance frequency $\widehat q$, Hoeffding\'s inequality gives, except with a calibration failure probability $\eta\in(0,1)$,

`<a id="eq:calibration"></a>`{=html} $$q\le q_{\mathrm{up}}
:=\min\!\left\{1,\widehat q+
\sqrt{\frac{\log(1/\eta)}{2m}}\right\}.

\tag{10}$$

Detector noise and loss are absorbed into $q$ this way. Second, a real detector is only approximately localized. If the deployed effect $\Pi$ lies within operator-norm distance $\epsilon$ of an ideal effect $\Pi_0\in\mathcal{N}$, positivity and subunitality give

`<a id="eq:approx-locality"></a>`{=html} $$\begin{split}
\widetilde\omega_0\!\left(\Phi(\Pi\otimes\mathbf{1})\right)
&\le\omega_0(\Pi_0)+\epsilon\\
&\le\omega_0(\Pi)+2\epsilon.
\end{split}

\tag{11}$$

The field theory supplies the inequality, and a detector model must supply $\epsilon$.

The forger class is deliberately generous. Not every formal Kraus family in a local algebra has a confined laboratory implementation, and some idealized field measurements would even permit superluminal signaling \[[10](#ref-sorkin1993impossible), [11](#ref-jubb2022causal)\]. System-probe models give a physically grounded class of local measurements \[[12](#ref-fewster2020measurement), [13](#ref-bostelmann2021impossible)\], and completely positive maps provide a broader language \[[14](#ref-kitajima2018local)\]. Every implementation that respects Eq. [(1)](#eq:commuting-algebras) is covered by the same bound.

Repetition and the optimal rate {#sec:amplification}
-------------------------------

Since $q>0$ for the vacuum, one run cannot authenticate with certainty, and the verifier must repeat. As in any statistical test, evidence accumulates over repetitions, and the question is how fast. Repetition helps only if her algebra distinguishes the honest state from the reference state at all. Suppose the two states give different expectations to some Hermitian $X\in\mathcal{N}$. Shifting and rescaling $X$ produces an effect $Q\in\mathcal{N}$ with

`<a id="eq:gap"></a>`{=html} $$c:=\omega_1(Q)>\omega_0(Q)=:q.

\tag{12}$$

A bounded effect always suffices, so no unbounded field observable is needed to start amplifying.

### A simple threshold test

Consider $n$ independent preparations, all honest or all reference. The observables of $n$ copies form the algebra $\mathcal{N}^{\bar\otimes n}$. Measure $\{Q,\mathbf{1}-Q\}$ on each copy, writing $Q^{(1)}=Q$ and $Q^{(0)}=\mathbf{1}-Q$, and accept when at least a fraction $\tau\in(q,c)$ of the outcomes equal one. The corresponding effect sums over all accepted outcome strings $x$,

`<a id="eq:threshold-effect"></a>`{=html} $$\Pi_{n,\tau}
=
\sum_{\substack{x\in\{0,1\}^n\\ \sum_kx_k\ge n\tau}}
\bigotimes_{k=1}^{n}Q^{(x_k)}.

\tag{13}$$

Since the terms come from a product measurement, $0\le\Pi_{n,\tau}\le\mathbf{1}$ and $\Pi_{n,\tau}\in\mathcal{N}^{\bar\otimes n}$, even when $Q$ is not a projection. The outcomes are independent coin flips with mean $c$ for honest copies and mean $q$ for reference copies, and Hoeffding\'s inequality bounds both error types \[[15](#ref-hoeffding1963probability)\],

`<a id="eq:complete-hoeffding"></a>`{=html} $$\begin{aligned}
\omega_1^{\otimes n}(\Pi_{n,\tau})
&\ge1-\exp[-2n(c-\tau)^2],
\end{aligned}\tag{14}$$

`<a id="eq:sound-hoeffding"></a>`{=html} $$\begin{aligned}
\omega_0^{\otimes n}(\Pi_{n,\tau})
&\le\exp[-2n(\tau-q)^2].

\end{aligned}\tag{15}$$

Now apply Theorem [1](#thm:locality) with the product algebra $\mathcal{N}^{\bar\otimes n}$ in place of $\mathcal{N}$. The second line becomes a forgery bound against every joint strategy, including collective operations entangled across all $n$ copies. Acting coherently on many runs does not help the forger, because she still cannot touch the verifier\'s statistics.

At the midpoint $\tau=(c+q)/2$ both errors are at most $\exp[-n(c-q)^2/2]$, so both fall below a target $\varepsilon$ once

`<a id="eq:sample-complexity"></a>`{=html} $$n\ge \frac{2}{(c-q)^2}\log\frac1\varepsilon.

\tag{16}$$

This test uses one bounded effect and classical counting. Its rate depends on the chosen effect, and optimizing over all measurements leads to a property of the two states alone.

### The optimal exponent

How fast can any test suppress forgery? By Theorem [1](#thm:locality), the worst-case forgery probability of a fixed test equals its reference acceptance, so the question concerns the reference state alone. If the verifier tolerates rejecting an honest signal with probability at most $\delta\in(0,1/2)$, the smallest forgery probability achievable on $n$ copies is

`<a id="eq:beta"></a>`{=html} $$\beta_{\delta}^{(n)}
=\inf_{\substack{0\le\Pi_n\le\mathbf{1}\\
\Pi_n\in\mathcal{N}^{\bar\otimes n}\\
\omega_1^{\otimes n}(\Pi_n)\ge1-\delta}}
\omega_0^{\otimes n}(\Pi_n).

\tag{17}$$

In the language of hypothesis testing this is the type-II error, the probability of accepting when the reference hypothesis is true, minimized at fixed completeness. Its decay is governed by the Araki relative entropy $D_{\mathcal{N}}(\omega_1\|\omega_0)$ of the two states restricted to $\mathcal{N}$ \[[16](#ref-araki1976relative)\], the von Neumann algebra version of $\operatorname{Tr}\rho(\log\rho-\log\sigma)$ for density matrices $\rho$ and $\sigma$. Classically it is the average log-likelihood ratio, the evidence that one honest sample provides against the reference hypothesis.

**Theorem 2 (Optimal independent-copy rate).** `<a id="thm:stein"></a>`{=html} Let $\mathcal{N}$ be $\sigma$-finite, meaning that it admits a faithful normal state. Let $\omega_0,\omega_1$ be faithful normal states on $\mathcal{N}$, so every nonzero effect has positive expectation, and suppose $D_{\mathcal{N}}(\omega_1\|\omega_0)<\infty$. Every effect $\Pi\in\mathcal{N}$ with $\omega_1(\Pi)\ge1-\delta$ obeys

`<a id="eq:one-shot-converse"></a>`{=html} $$\omega_0(\Pi)
\ge
\exp\!\left[
-\frac{D_{\mathcal{N}}(\omega_1\|\omega_0)+h_2(\delta)}
{1-\delta}
\right],

\tag{18}$$

where $h_2(\delta)=-\delta\log\delta-(1-\delta)\log(1-\delta)$ is the binary entropy. Moreover,

`<a id="eq:stein"></a>`{=html} $$\lim_{n\to\infty}
-\frac1n\log\beta_{\delta}^{(n)}
=D_{\mathcal{N}}(\omega_1\|\omega_0).

\tag{19}$$

*Proof.* Measuring $\Pi$ turns both states into coin flips, heads with probability $r=\omega_1(\Pi)$ for the honest state and $s=\omega_0(\Pi)$ for the reference. Relative entropy can only decrease under this coarse graining \[[17](#ref-uhlmann1977relative)\], so it is at least the classical relative entropy $d(r\|s)$ of the two coins,

$$\begin{split}
D_{\mathcal{N}}(\omega_1\|\omega_0)
&\ge d(r\|s)\\
&\ge r\log(1/s)-h_2(r)\\
&\ge(1-\delta)\log(1/s)-h_2(\delta).
\end{split}
\tag{20}$$

The last line uses $r\ge1-\delta>1/2$. Solving for $s$ gives Eq. [(18)](#eq:one-shot-converse). The asymptotic equality [(19)](#eq:stein) is the quantum Stein lemma, proved for faithful normal states on a $\sigma$-finite von Neumann algebra by Pautrat and Wang \[[18](#ref-hiai1991proper), [19](#ref-ogawa2000strong), [20](#ref-pautrat2023ke)\].

The relative entropy is thus the number of nats of evidence per copy that an optimal verifier can collect. For a finite block of $n$ copies, Eq. [(18)](#eq:one-shot-converse) applied to the product states, with $D_{\mathcal{N}}$ replaced by $nD_{\mathcal{N}}$, gives a converse with explicit dependence on $\delta$. Equation [(19)](#eq:stein) identifies the limiting exponent, while the threshold test offers a simpler implementation whose rate may be smaller.

A pulse on a light ray {#sec:current}
----------------------

### The chiral current

To give the relative entropy a geometric meaning we need a field in which it can be computed. The simplest is the chiral $U(1)$ current. A massless scalar field in $1+1$ dimensions splits into left-moving and right-moving parts. The derivative of one of them is the chiral current $j(u)$, a field that depends only on the null coordinate $u$ along a light ray. Its coherent states are classical pulses traveling at the speed of light. We use units with $\hbar$ and the speed of light equal to one.

As with any field, physical observables come from smearing. For a real test function $f$, smooth and with compact support, $j(f)=\int j(u)f(u)\,du$ is the current averaged against $f$, and the Weyl unitary $W(f)=e^{ij(f)}$ displaces the field by a classical profile determined by $f$. For an interval $I$ of the light ray, let $\mathcal{A}(I)$ be the von Neumann algebra generated by the $W(f)$ with $f$ supported in $I$. Cut the ray at the origin and give the two sides to the two players,

`<a id="eq:halflines"></a>`{=html} $$\mathcal{M}=\mathcal{A}((0,\infty)),
\qquad
\mathcal{N}=\mathcal{A}((-\infty,0)).

\tag{21}$$

The verifier and the honest source live on $u<0$, and the forger is confined to $u>0$. Weyl operators with disjoint supports commute, so $\mathcal{N}\subseteq\mathcal{M}'$.

Two numbers fix how the field responds to smearing. The Weyl relations and the vacuum expectation of a Weyl operator read

`<a id="eq:symplectic"></a>`{=html} $$\begin{aligned}
W(f)W(h)&=e^{-i\sigma(f,h)/2}W(f+h),\end{aligned}\tag{22}$$

`<a id="eq:vacuum-characteristic"></a>`{=html} $$\begin{aligned}
\omega_0(W(th))&=e^{-t^2v_h/2},\qquad
v_h=\langle\Omega,j(h)^2\Omega\rangle,

\end{aligned}\tag{23}$$

for real test functions $f,h$ and real $t$. The symplectic form $\sigma(f,h)$, a fixed nonzero multiple of $\int f(u)h'(u)\,du$, sets the commutator of two smeared currents, and $v_h$ is the vacuum variance of $j(h)$, its quantum noise. The coefficient in $\sigma$, the variance, and the energy density below must all refer to one current normalization; a Weyl convention with phase $-i\sigma$ instead of $-i\sigma/2$, for example, uses a symplectic form half as large. We state physical rates in terms of energy, which removes this ambiguity.

For the honest signal, fix a standoff $a>0$ and a nonzero real profile $f$ supported in $(-\infty,-a)$, so the pulse sits at least a null distance $a$ from the cut. The honest unitary $U=W(f)\in\mathcal{N}$ prepares the coherent state

`<a id="eq:coherent-state"></a>`{=html} $$\omega_f(X)
=\langle W(f)\Omega,XW(f)\Omega\rangle
=\omega_0(W(f)^*XW(f)).

\tag{24}$$

### A bounded local test

First we check that a bounded effect on the verifier\'s side sees the pulse, as Sec. [3](#sec:amplification) requires. Probe the field with a Weyl unitary $W(h)$, $h$ real and supported in $(-\infty,0)$. By Eq. [(22)](#eq:symplectic) the pulse multiplies its expectation by a phase, $\omega_f(W(h))=e^{i\sigma(f,h)}\omega_0(W(h))$. Let $d=\omega_f(W(h))-\omega_0(W(h))$ and, when $d\ne0$, let $\theta=\arg d$. The operators

`<a id="eq:weyl-effect"></a>`{=html} $$X_h=\frac{e^{-i\theta}W(h)+e^{i\theta}W(h)^*}{2},
\qquad
Q_h=\frac{\mathbf{1}+X_h}{2}

\tag{25}$$

satisfy $-\mathbf{1}\le X_h\le\mathbf{1}$, because $X_h$ is the real part of a unitary, so $Q_h$ is an effect in $\mathcal{N}$. Its gap is

`<a id="eq:explicit-weyl-gap"></a>`{=html} $$\omega_f(Q_h)-\omega_0(Q_h)
=\left|\sin\frac{\sigma(f,h)}{2}\right|
e^{-v_h/2}.

\tag{26}$$

The formula displays the basic tradeoff of field detection. A stronger probe $h$ increases the signal phase $\sigma(f,h)$, but it also increases the vacuum noise $v_h$, which washes out the expectation through the Gaussian factor. A suitable probe always exists. The phase $\sigma(f,h)$ is a multiple of $-\int f'(u)h(u)\,du$, a nonzero compactly supported $f$ has $f'\ne0$ somewhere, and a bump $h$ placed there and rescaled gives $\sigma(f,h)\notin2\pi\mathbb Z$.

### The optimal rate is a weighted energy

Write the energy density of the classical pulse and its total energy as

`<a id="eq:energy-density"></a>`{=html} $$\rho_f(u)=c_j(f'(u))^2,\quad c_j>0,\qquad
E_f=\int_{-\infty}^{0}\rho_f(u)\,du,

\tag{27}$$

with the constant $c_j$ fixed by the same current normalization as $\sigma$ and $v_h$. Two known facts now combine. The vacuum modular flow of a half-line, the intrinsic dynamics for which the restricted vacuum is a thermal state, acts by dilations about its edge \[[21](#ref-bisognano1975duality), [22](#ref-bisognano1976duality), [23](#ref-brunetti1993modular)\]. And the relative entropy of a coherent state equals the expectation of the corresponding modular Hamiltonian in the classical pulse \[[24](#ref-longo2019entropy), [25](#ref-casini2019coherent), [26](#ref-bostelmann2022relative)\]. Together they give

`<a id="eq:current-entropy"></a>`{=html} $$D_{\mathcal{N}}(\omega_f\|\omega_0)
=2\pi\int_{-\infty}^{0}(-u)\rho_f(u)\,du
=:M_f.

\tag{28}$$

The same functional underlies the relative-entropy formulation of the Bekenstein bound \[[27](#ref-casini2008bekenstein)\].

The weight $2\pi(-u)$ explains why the position of the pulse matters. For a thermal state at inverse temperature $\beta$, the relative entropy of a coherent displacement is $\beta$ times the energy it adds. Here the half-line vacuum is thermal for the dilation generator, and $2\pi(-u)$ plays the role of a local inverse temperature. This temperature refers to modular flow, not to any heating of the field, but it is a faithful guide to distinguishability. The same added energy carries more relative entropy farther from the edge. Because the pulse lies in $u\le-a$,

`<a id="eq:standoff"></a>`{=html} $$M_f\ge2\pi aE_f.

\tag{29}$$

The half-line algebra is $\sigma$-finite in the vacuum representation, the vacuum and coherent states are faithful and normal, and compact support makes $M_f$ finite. Theorem [2](#thm:stein) therefore gives, for fixed $0<\delta<1/2$,

`<a id="eq:explicit-rate"></a>`{=html} $$\beta_\delta^{(n)}
=\exp[-nM_f+o(n)].

\tag{30}$$

Counting quanta makes the scales concrete. Let the coherent pulse have mean occupation $\bar n>0$, define its mean angular frequency $\bar\omega=E_f/\bar n$, and set $\lambda_{\mathrm{eff}}=2\pi/\bar\omega$. Then $E_f=2\pi\bar n/\lambda_{\mathrm{eff}}$ and

`<a id="eq:geometry-energy"></a>`{=html} $$M_f\ge
4\pi^2\,\frac{a}{\lambda_{\mathrm{eff}}}\,\bar n.

\tag{31}$$

For a narrowband pulse $\lambda_{\mathrm{eff}}$ is the central wavelength, up to the relative bandwidth. A coherent pulse with mean occupation $\bar n=1$ at standoff $a=\lambda_{\mathrm{eff}}$ already gives at least $4\pi^2\simeq39.5$ nats per copy. The occupation is a mean over the coherent state\'s particle-number distribution, so this concerns the coherent pulse, not a one-particle state. It is also an asymptotic rate for optimal measurements on the whole half-line, and any single test still obeys the one-shot lower bound of Eq. [(18)](#eq:one-shot-converse).

### What a fixed detector sees

A deployed receiver measures something specific. Take a bounded interval $I\subset(-\infty,0)$ containing the supports of $f$ and $h$, with $\mu=\sigma(f,h)>0$ and $v=v_h>0$. The smeared current $j(h)$ is Gaussian, distributed as $N(\mu,v)$ under the pulse and as $N(0,v)$ under the vacuum, where $N(m,s)$ denotes a normal law with mean $m$ and variance $s$. Add independent calibrated Gaussian readout noise of variance $v_d\ge0$. On $n$ copies, accept if the mean readout exceeds

$$t_n=\mu-\sqrt{(v+v_d)/n}\,z_\delta,\quad
z_\delta=\Phi_{\rm G}^{-1}(1-\delta),
\tag{32}$$

where $\Phi_{\rm G}$ is the standard normal distribution function. The induced effect lies in $\mathcal{A}(I)^{\bar\otimes n}$. Its completeness is exactly $1-\delta$, and by Theorem [1](#thm:locality) its worst-case forgery probability, collective attacks included, is

`<a id="eq:local-homodyne"></a>`{=html} $$q_n=\overline\Phi_{\rm G}\!\left(\frac{\sqrt n\mu}{\sqrt{v+v_d}}-z_\delta\right),
\qquad \overline\Phi_{\rm G}=1-\Phi_{\rm G}.

\tag{33}$$

At fixed $\delta$, the exponent $-\lim_{n\to\infty}n^{-1}\log q_n$ is the signal-to-noise ratio $\mu^2/[2(v+v_d)]$. The Gaussian coupling and the independent readout noise are a detector model; finite resolution can be included instead in the deployed effect and its calibrated $q$.

Now translate $f$, $h$, and $I$ together away from the cut. The vacuum is translation invariant, so $\mu$, $v$, and Eq. [(33)](#eq:local-homodyne) do not change, while $M_f$ grows. Modular theory explains the difference. For tests confined to $I=(b_1,b_2)$, the same Stein lemma gives the optimal exponent $D_{\mathcal{A}(I)}(\omega_f\|\omega_0)$, which can only be smaller than the half-line value, since restricting the measurement algebra cannot increase relative entropy. The vacuum modular flow of an interval is again geometric \[[28](#ref-hislop1982modular)\], and the coherent-state formula \[[29](#ref-garbarz2023interval)\] replaces the half-line weight $-u$ by

$$\frac{(u-b_1)(b_2-u)}{b_2-b_1}=\Bigl(\frac1{d_1}+\frac1{d_2}\Bigr)^{-1},$$

where $d_1=u-b_1$ and $d_2=b_2-u$ are the distances to the two edges of $I$. This weight is controlled by the nearer edge, vanishes at both, and is unchanged when the interval and the pulse move together. An interval has hot edges of its own. The optimal rate of the interval, like the homodyne rate, therefore stays fixed. The growing half-line rate reflects the larger region between the pulse and the fixed cut, and exploiting it requires measurements that reach beyond any interval carried with the pulse. The entropy formula does not by itself prescribe a detector that attains it.

What acceptance certifies {#sec:limits}
-------------------------

Acceptance rejects one hypothesis, namely that the observed state was prepared from the prescribed reference state using operations in the excluded region. The certificate concerns causal access to the reference field. Identifying the emitter or establishing a secret would require further protocol steps. The number $q$ is a false-acceptance probability under the hypothesis of excluded access; reading an accepted run as evidence of honesty also requires prior probabilities for the competing preparations.

The experiment must specify its initial state and count its attempts. Our model starts each run in the prescribed field state with independent forger memory, and the Stein rate uses independent field copies. Correlated modes or initial field-memory correlations require a joint reference model. A detector implementation must establish commutation with the excluded algebra or bound the localization error in Eq. [(11)](#eq:approx-locality). Repeated use also requires fresh references and a schedule that counts discarded attempts and prevents replay.

Conclusion {#sec:conclusion}
----------

Locality turns a causal cut into an authentication resource. A forger confined to the excluded side can only select runs, so the exact worst-case forgery probability of any local test is its reference acceptance. Repetition amplifies any local statistical gap, and the best achievable rate is the relative entropy of the honest and reference states on the verifier\'s algebra. For a pulse of the chiral current this rate is the pulse energy measured against the position-dependent modular temperature of the half-line vacuum, so energy and distance from the cut buy authentication together. A fixed detector carried with the pulse keeps the same rate, which shows that the measurement region is part of the resource.

Acknowledgments {#acknowledgments .unnumbered}
---------------

The authors thank colleagues at Universidad Carlos III de Madrid for discussions.

AI assistance {#ai-assistance .unnumbered}
-------------

AI tools assisted with writing, mathematical derivations, literature review, and numerical code. Some claims in this working paper remain to be independently checked.

References {#references .unnumbered}
----------

1.  `<a id="ref-haag1964algebraic"></a>`{=html} Rudolf Haag and Daniel Kastler. An algebraic approach to quantum field theory. *Journal of Mathematical Physics*, 5(7):848--861, 1964.

2.  `<a id="ref-reeh1961bemerkungen"></a>`{=html} Helmut Reeh and Siegfried Schlieder. Bemerkungen zur unitären Äquivalenz von Lorentzinvarianten Feldern. *Il Nuovo Cimento*, 22(5):1051--1068, 1961.

3.  `<a id="ref-witten2018aps"></a>`{=html} Edward Witten. Notes on some entanglement properties of quantum field theory. *Reviews of Modern Physics*, 90:045003, 2018.

4.  `<a id="ref-hayden2019localizing"></a>`{=html} Patrick Hayden and Alex May. Localizing and excluding quantum information; or, how to share a quantum secret in spacetime. *Quantum*, 3:196, 2019.

5.  `<a id="ref-kent2014secure"></a>`{=html} Adrian Kent, Serge Massar, and Jonathan Silman. Secure and robust transmission and verification of unknown quantum states in minkowski space. *Scientific Reports*, 4(1):3901, 2014.

6.  `<a id="ref-kent2011quantum"></a>`{=html} Adrian Kent, William J. Munro, and Timothy P. Spiller. Quantum tagging: Authenticating location via quantum information and relativistic signaling constraints. *Physical Review A*, 84(1):012326, 2011.

7.  `<a id="ref-chandran2009position"></a>`{=html} Nishanth Chandran, Vipul Goyal, Ryan Moriarty, and Rafail Ostrovsky. Position based cryptography. In *Annual International Cryptology Conference*, pages 391--407. Springer, 2009.

8.  `<a id="ref-buhrman2014position"></a>`{=html} Harry Buhrman, Nishanth Chandran, Serge Fehr, Ran Gelles, Vipul Goyal, Rafail Ostrovsky, and Christian Schaffner. Position-based quantum cryptography: Impossibility and constructions. *SIAM Journal on Computing*, 43(1):150--178, 2014.

9.  `<a id="ref-bennett1984quantum"></a>`{=html} Charles H. Bennett and Gilles Brassard. Quantum cryptography: Public key distribution and coin tossing. In *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing*, pages 175--179, 1984.

10. `<a id="ref-sorkin1993impossible"></a>`{=html} Rafael D Sorkin. Impossible measurements on quantum fields. In *Directions in general relativity: Proceedings of the 1993 International Symposium, Maryland*, volume 2, pages 293--305, 1993.

11. `<a id="ref-jubb2022causal"></a>`{=html} I Jubb. Causal state updates in real scalar quantum field theory. *Physical Review D*, 105(2):025003, 2022.

12. `<a id="ref-fewster2020measurement"></a>`{=html} Christopher J. Fewster and Rainer Verch. Quantum fields and local measurements. *Communications in Mathematical Physics*, 378:851--889, 2020.

13. `<a id="ref-bostelmann2021impossible"></a>`{=html} Henning Bostelmann, Christopher J Fewster, and Maximilian H Ruep. Impossible measurements require impossible apparatus. *Physical Review D*, 103(2):025017, 2021.

14. `<a id="ref-kitajima2018local"></a>`{=html} Yuichiro Kitajima. Local operations and completely positive maps in algebraic quantum field theory. In *Reality and Measurement in Algebraic Quantum Theory*, volume 261 of *Springer Proceedings in Mathematics & Statistics*, pages 83--95. Springer, 2018.

15. `<a id="ref-hoeffding1963probability"></a>`{=html} Wassily Hoeffding. Probability inequalities for sums of bounded random variables. *Journal of the American statistical association*, 58(301):13--30, 1963.

16. `<a id="ref-araki1976relative"></a>`{=html} Huzihiro Araki. Relative entropy of states of von Neumann algebras. *Publications of the Research Institute for Mathematical Sciences*, 11(3):809--833, 1976.

17. `<a id="ref-uhlmann1977relative"></a>`{=html} Armin Uhlmann. Relative entropy and the Wigner-Yanase-Dyson-Lieb concavity in an interpolation theory. *Communications in Mathematical Physics*, 54(1):21--32, 1977.

18. `<a id="ref-hiai1991proper"></a>`{=html} Fumio Hiai and Dénes Petz. The proper formula for relative entropy and its asymptotics in quantum probability. *Communications in Mathematical Physics*, 143:99--114, 1991.

19. `<a id="ref-ogawa2000strong"></a>`{=html} Tomohiro Ogawa and Hiroshi Nagaoka. Strong converse and Stein\'s lemma in quantum hypothesis testing. *IEEE Transactions on Information Theory*, 46(7):2428--2433, 2000.

20. `<a id="ref-pautrat2023ke"></a>`{=html} Yan Pautrat and Simeng Wang. Ke Li\'s lemma for quantum hypothesis testing in general von Neumann algebras. *Annales Henri Poincaré*, 24(7):2323--2339, 2023.

21. `<a id="ref-bisognano1975duality"></a>`{=html} Joseph J Bisognano and Eyvind H Wichmann. On the duality condition for a hermitian scalar field. *Journal of Mathematical Physics*, 16(4):985--1007, 1975.

22. `<a id="ref-bisognano1976duality"></a>`{=html} Joseph J Bisognano and Eyvind H Wichmann. On the duality condition for quantum fields. *Journal of mathematical physics*, 17(3):303--321, 1976.

23. `<a id="ref-brunetti1993modular"></a>`{=html} Romeo Brunetti, D Guido, and Roberto Longo. Modular structure and duality in conformal quantum field theory. *Communications in Mathematical Physics*, 156(1):201--219, 1993.

24. `<a id="ref-longo2019entropy"></a>`{=html} Roberto Longo. Entropy of coherent excitations. *Letters in Mathematical Physics*, 109:2587--2600, 2019.

25. `<a id="ref-casini2019coherent"></a>`{=html} Horacio Casini, Sergio Grillo, and Diego Pontello. Relative entropy for coherent states from Araki formula. *Physical Review D*, 99(12):125020, 2019.

26. `<a id="ref-bostelmann2022relative"></a>`{=html} Henning Bostelmann, Daniela Cadamuro, and Simone Del Vecchio. Relative entropy of coherent states on general CCR algebras. *Communications in Mathematical Physics*, 389(1):661--691, 2022.

27. `<a id="ref-casini2008bekenstein"></a>`{=html} Horacio Casini. Relative entropy and the Bekenstein bound. *Classical and Quantum Gravity*, 25(20):205021, 2008.

28. `<a id="ref-hislop1982modular"></a>`{=html} Peter D Hislop and Roberto Longo. Modular structure of the local algebras associated with the free massless scalar field theory. *Communications in Mathematical Physics*, 84(1):71--85, 1982.

29. `<a id="ref-garbarz2023interval"></a>`{=html} Alan Garbarz and Gabriel Palau. Relative entropy of an interval for a massless boson at finite temperature. *Physical Review D*, 107(12):125016, 2023.
