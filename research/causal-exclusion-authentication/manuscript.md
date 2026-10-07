# Causal-Exclusion Authentication in Quantum Field Theory

Javier Blanco-Romero

Department of Telematic Engineering, Universidad Carlos III de Madrid, Leganés, Madrid, Spain

<a id="abstract"></a>

## Abstract

We formulate an authentication task for causal access across a spacetime cut. The field starts in a prescribed state, the adversary acts in an excluded region, and the verifier measures in a commuting algebra. Locality then bounds the joint forgery probability by the reference acceptance of the deployed test, even when the adversary uses independent quantum memory, postselection, or a collective operation across repetitions. A bounded local test gives explicit finite-copy amplification, while optimized collective tests have Araki relative entropy as their asymptotic soundness exponent. For a coherent excitation of the chiral current on a null half-line, this exponent is a weighted null energy and grows with the packet energy and its distance from the cut. The task certifies causal access rather than identity, ownership, or a unique emission point.

<a id="introduction"></a>

## Introduction

<a id="sec:intro"></a>

Locality assigns commuting observable algebras to causally disjoint regions \[[1](#ref-haag1964algebraic)\]. Suppose a receiver checks for a public field signature while an adversary is confined to a commuting algebra. Starting from a prescribed reference state, the adversary cannot raise the joint acceptance probability above that state's false-positive probability, even by postselection. This supplies a statistical test of the hypothesis that only the excluded region acted. It does not identify the source or locate a unique emission event.

Spacetime secret sharing distributes an unknown system among authorized regions \[[2](#ref-hayden2019localizing)\]. Relativistic state verification and position verification constrain where an unknown state or response can be produced \[[3](#ref-kent2014secure), [4](#ref-kent2011quantum), [5](#ref-chandran2009position), [6](#ref-buhrman2014position)\]. Here the signal and test may both be public. The alternative being rejected is simply preparation from a prescribed state using the excluded algebra.

For each fixed verifier, we show that its reference acceptance is exactly the worst-case forgery probability. Independent repetitions permit amplification, and optimized collective tests have the Araki relative-entropy exponent. In the chiral current, this becomes weighted null energy. We also give a bounded-region detector and distinguish its achievable rate from optimization over the full half-line. The constituent locality, hypothesis-testing, and coherent-state entropy results are established; our contribution is their application to this access test.

Section [2](#sec:primitive) treats one invocation, Sec. [3](#sec:amplification) treats repetition, and Sec. [4](#sec:current) gives the field realization.

<a id="causal-exclusion-authentication"></a>

## Causal-exclusion authentication

<a id="sec:primitive"></a>

<a id="setup"></a>

### Setup

Let $\mathcal{M},\mathcal{N}\subset B(\mathcal{H})$ be von Neumann algebras with

<a id="eq:commuting-algebras"></a>

$$
\mathcal{N}\subseteq\mathcal{M}',\tag{1}
$$

and let $\Omega\in\mathcal{H}$ be a unit reference vector. The adversary controls $\mathcal{M}$ and the verifier accepts according to an effect $\Pi\in\mathcal{N}$. An honest invocation applies a public unitary $U\in\mathcal{N}$ and prepares $U\Omega$. We write

$$
\omega_0(X)=\langle\Omega,X\Omega\rangle,
\qquad
\omega_1(X)=\langle U\Omega,XU\Omega\rangle,\tag{2}
$$

so the reference acceptance and honest completeness are

<a id="eq:q-c"></a>

$$
q=\omega_0(\Pi),
\qquad
c=\omega_1(\Pi).\tag{3}
$$

The security objective is to bound the probability that an adversarial branch occurs and the verifier accepts. Discarded branches count as failures. This joint event is the right quantity when postselection is allowed.

The adversary may use a memory $\mathcal{H}_{\mathrm a}$, initially independent of the field. A purification lets us take its state to be a vector $\varphi\in\mathcal{H}_{\mathrm a}$. On the joint system define

<a id="eq:extended-reference"></a>

$$
\widetilde{\mathcal{N}}=\mathcal{N}\bar\otimes\mathbb C\mathbf{1},
\qquad
\widetilde\omega_0(X)
=\langle\Omega\otimes\varphi,X\Omega\otimes\varphi\rangle.\tag{4}
$$

In the Heisenberg picture, an accepted adversarial branch is a normal, completely positive, subunital map $\Phi$ on $B(\mathcal{H}\otimes\mathcal{H}_{\mathrm a})$. We allow every such map that is $\widetilde{\mathcal{N}}$-bimodular:

<a id="eq:bimodular"></a>

$$
\Phi(N_1XN_2)=N_1\Phi(X)N_2\tag{5}
$$

for all $N_1,N_2\in\widetilde{\mathcal{N}}$ and $X$. Bimodularity says that the operation leaves verifier observables as spectators. It is slightly more general than asking for Kraus operators in the adversary algebra. In particular, it includes every finite or countable local subinstrument

<a id="eq:subinstrument"></a>

$$
\begin{split}
B_j&\in\mathcal{M}\bar\otimes B(\mathcal{H}_{\mathrm a}),
\qquad
\sum_{j\in J}B_j^*B_j\le\mathbf{1},\\
\Phi_B(X)&=\sum_{j\in J}B_j^*XB_j.
\end{split}\tag{6}
$$

with strong convergence of the sum, because every $B_j$ commutes with $\widetilde{\mathcal{N}}$. The set $J$ contains the outcomes counted as an attempted forgery; the inequality allows all other outcomes to be discarded.

<a id="one-shot-soundness"></a>

### One-shot soundness

**Theorem 1 (Locality soundness).** <a id="thm:locality"></a> Every accepted operation in the model above satisfies

<a id="eq:locality-soundness"></a>

$$
p_{\mathrm{forge}}
:=\widetilde\omega_0\!\left(
\Phi(\Pi\otimes\mathbf{1})\right)
\le\omega_0(\Pi)=q.\tag{7}
$$

For the local subinstrument [(6)](#eq:subinstrument), this probability is

<a id="eq:kraus-forgery"></a>

$$
\sum_{j\in J}
\langle\Omega\otimes\varphi,
B_j^*(\Pi\otimes\mathbf{1})B_j
\Omega\otimes\varphi\rangle.\tag{8}
$$

For a fixed test $\Pi$, the bound is tight.

*Proof.* Bimodularity pulls the verifier effect through the adversarial operation,

$$
\Phi(\Pi\otimes\mathbf{1})
=(\Pi\otimes\mathbf{1})\Phi(\mathbf{1})
=\Phi(\mathbf{1})(\Pi\otimes\mathbf{1}).\tag{9}
$$

The operator $\Phi(\mathbf{1})$ is the effect associated with the accepted branch. It commutes with $\Pi\otimes\mathbf{1}$ and lies between zero and the identity. Hence

$$
0\le\Phi(\Pi\otimes\mathbf{1})
\le\Pi\otimes\mathbf{1}.\tag{10}
$$

Applying the reference state proves the bound. The identity operation attains $q$, so no smaller universal value is possible for the same test.

The theorem controls joint rather than conditional success. If branch $j$ occurs with probability $p_j$ and has conditional acceptance $a_j$, then the bounded quantity is $\sum_jp_ja_j$. A rare branch may have $a_j=1$ without violating soundness. Its rarity remains part of the authentication error. This is also why every scheduled attempt must be counted. If $T$ reset invocations satisfy the assumptions conditionally on the previous transcript, their total false-acceptance probability is at most $\sum_tq_t$.

The exact result assumes that the deployed acceptance effect belongs to $\mathcal{N}$. A simple perturbative estimate covers imperfect localization. If $\|\Pi-\Pi_0\|\le\epsilon$ for an ideal effect $\Pi_0\in\mathcal{N}$, positivity and subunitality give

<a id="eq:approx-locality"></a>

$$
\begin{split}
\widetilde\omega_0\!\left(\Phi(\Pi\otimes\mathbf{1})\right)
&\le\omega_0(\Pi_0)+\epsilon\\
&\le\omega_0(\Pi)+2\epsilon.
\end{split}\tag{11}
$$

The field theory supplies the algebraic inequality; a detector model must supply $\epsilon$.

Soundness depends on the reference acceptance of the actual test. It can be calibrated directly. If $m$ independent reference runs yield frequency $\widehat q$, then Hoeffding's inequality gives, with confidence at least $1-\eta$,

<a id="eq:calibration"></a>

$$
q\le q_{\mathrm{up}}
:=\min\!\left\{1,\widehat q+
\sqrt{\frac{\log(1/\eta)}{2m}}\right\}.\tag{12}
$$

The calibration requires independent, stationary reference runs. These statistical assumptions are separate from locality.

The map formulation is algebraic. It does not claim that every formal Kraus family in a local algebra has a confined laboratory implementation. Some idealized field-measurement prescriptions conflict with causal signaling constraints \[[7](#ref-sorkin1993impossible), [8](#ref-jubb2022causal)\]. System-probe schemes provide a physically grounded class of causal measurements \[[9](#ref-fewster2020measurement), [10](#ref-bostelmann2021impossible)\], while completely positive maps give a broader language for local operations \[[11](#ref-kitajima2018local)\]. Enlarging the adversary class to all bimodular maps is conservative for any realizable subclass it contains.

<a id="amplification-and-the-optimal-rate"></a>

## Amplification and the optimal rate

<a id="sec:amplification"></a>

The one-shot theorem becomes useful when the verifier can distinguish the honest and reference states inside $\mathcal{N}$. If their restrictions to $\mathcal{N}$ differ, they differ on a self-adjoint element. Rescaling that element gives an effect $Q\in\mathcal{N}$ with

<a id="eq:gap"></a>

$$
c:=\omega_1(Q)>\omega_0(Q)=:q.\tag{13}
$$

Thus separation never requires an unbounded field observable.

<a id="a-finite-copy-test"></a>

### A finite-copy test

Consider $n$ independent preparations of either state. Write $Q^{(1)}=Q$ and $Q^{(0)}=\mathbf{1}-Q$. Measure each copy with $\{Q,\mathbf{1}-Q\}$ and accept when at least a fraction $\tau\in(q,c)$ of the outcomes equal one. The resulting effect is

<a id="eq:threshold-effect"></a>

$$
\Pi_{n,\tau} = \sum_{\substack{x\in\{0,1\}^n\\ \sum_kx_k\ge n\tau}}
\bigotimes_{k=1}^{n}Q^{(x_k)}.\tag{14}
$$

The tensor products form a product POVM, so $0\le\Pi_{n,\tau}\le\mathbf{1}$ and $\Pi_{n,\tau}\in\mathcal{N}^{\bar\otimes n}$ even when $Q$ is not a projection. The outcomes are Bernoulli variables with means $c$ and $q$ under the honest and reference product states. Hoeffding's inequality therefore gives \[[12](#ref-hoeffding1963probability)\]

<a id="eq:complete-hoeffding"></a>

<a id="eq:sound-hoeffding"></a>

$$
\begin{aligned}
\omega_1^{\otimes n}(\Pi_{n,\tau})
&\ge1-\exp[-2n(c-\tau)^2],\qquad\text{(15)}\\
\omega_0^{\otimes n}(\Pi_{n,\tau})
&\le\exp[-2n(\tau-q)^2].\qquad\text{(16)}
\end{aligned}
$$

Theorem [1](#thm:locality), applied to the product verifier algebra, makes the second line a forgery bound against every joint bimodular strategy across the copies. The adversary need not act copywise.

At the midpoint $\tau=(c+q)/2$, both errors are at most

<a id="eq:midpoint"></a>

$$
\exp\!\left[-\frac{n(c-q)^2}{2}\right].\tag{17}
$$

Hence completeness and soundness errors are at most $\varepsilon$ once

<a id="eq:sample-complexity"></a>

$$
n\ge \frac{2}{(c-q)^2}\log\frac1\varepsilon.\tag{18}
$$

This test uses one bounded effect and classical thresholding. It is explicit, though generally not optimal.

<a id="the-optimal-exponent"></a>

### The optimal exponent

Let $D_{\mathcal{N}}(\omega_1\|\omega_0)$ denote the Araki relative entropy of the restrictions to $\mathcal{N}$ \[[13](#ref-araki1976relative)\]. For $0<\delta<1/2$, define

<a id="eq:beta"></a>

$$
\beta_{\delta}^{(n)}
=\inf_{\substack{0\le\Pi_n\le\mathbf{1}\\
\Pi_n\in\mathcal{N}^{\bar\otimes n}\\
\omega_1^{\otimes n}(\Pi_n)\ge1-\delta}}
\omega_0^{\otimes n}(\Pi_n).\tag{19}
$$

The identity attack in Theorem [1](#thm:locality) shows that the worst-case forgery probability of a fixed test equals its reference acceptance. Thus $\beta_{\delta}^{(n)}$ is also the smallest worst-case forgery probability among tests with completeness at least $1-\delta$.

**Theorem 2 (Optimal independent-copy rate).** <a id="thm:stein"></a> Let $\mathcal{N}$ be $\sigma$-finite, let $\omega_0,\omega_1$ be faithful normal states on $\mathcal{N}$, and suppose $D_{\mathcal{N}}(\omega_1\|\omega_0)<\infty$. Every effect $\Pi\in\mathcal{N}$ satisfying $\omega_1(\Pi)\ge1-\delta$ obeys

<a id="eq:one-shot-converse"></a>

$$
\omega_0(\Pi)
\ge
\exp\!\left[
-\frac{D_{\mathcal{N}}(\omega_1\|\omega_0)+h_2(\delta)}
{1-\delta}
\right],\tag{20}
$$

where $h_2(\delta)=-\delta\log\delta-(1-\delta)\log(1-\delta)$. In addition,

<a id="eq:stein"></a>

$$
\lim_{n\to\infty}
-\frac1n\log\beta_{\delta}^{(n)}
=D_{\mathcal{N}}(\omega_1\|\omega_0).\tag{21}
$$

*Proof.* Apply the binary measurement defined by $\Pi$. Monotonicity of Araki relative entropy reduces the problem to two Bernoulli distributions \[[14](#ref-uhlmann1977relative)\]. Put $r=\omega_1(\Pi)$ and $s=\omega_0(\Pi)$. Then

$$
\begin{split}
D_{\mathcal{N}}(\omega_1\|\omega_0)
&\ge d(r\|s)\\
&\ge r\log(1/s)-h_2(r)\\
&\ge(1-\delta)\log(1/s)-h_2(\delta),
\end{split}\tag{22}
$$

where the last line uses $r\ge1-\delta>1/2$. Rearrangement gives Eq. [(20)](#eq:one-shot-converse). Pautrat and Wang prove the needed Stein lemma for faithful normal states on a $\sigma$-finite von Neumann algebra \[[15](#ref-hiai1991proper), [16](#ref-ogawa2000strong), [17](#ref-pautrat2023ke)\], which gives Eq. [(21)](#eq:stein).

The two statements have different force. Equation [(20)](#eq:one-shot-converse) is a finite-copy lower bound, whereas Eq. [(21)](#eq:stein) is an asymptotic equality. Relative entropy does not imply $\beta_\delta^{(1)}=e^{-D_{\mathcal{N}}}$. The threshold test above also need not attain the Stein exponent. The optimization permits collective effects on $\mathcal{N}^{\bar\otimes n}$, whose physical implementation is a separate measurement-design problem.

<a id="null-cut-realization-in-the-chiral-current"></a>

## Null-cut realization in the chiral current

<a id="sec:current"></a>

The abstract exponent acquires a geometric meaning in the chiral $U(1)$ current. Let $j(u)$ be the current on a light ray, and let $\mathcal{A}(I)$ be the von Neumann algebra generated by Weyl unitaries $W(f)=e^{ij(f)}$ with real $f\in C_c^\infty(I)$. Put

<a id="eq:halflines"></a>

$$
\mathcal{M}=\mathcal{A}((0,\infty)),
\qquad
\mathcal{N}=\mathcal{A}((-\infty,0)).\tag{23}
$$

We fix the displacement and vacuum noise operationally,

<a id="eq:symplectic"></a>

<a id="eq:vacuum-characteristic"></a>

$$
\begin{aligned}
W(f)W(h)&=e^{-i\sigma(f,h)/2}W(f+h),\qquad\text{(24)}\\
\omega_0(W(th))&=e^{-t^2v_h/2},\qquad
v_h=\langle\Omega,j(h)^2\Omega\rangle.\qquad\text{(25)}
\end{aligned}
$$

In this convention $\sigma$ is a fixed nonzero multiple of $\int f(u)h'(u)du$. Its coefficient, the covariance, and the stress tensor must all refer to the same current normalization. In particular, a Weyl convention with phase $-i\sigma$ uses a symplectic form half as large as ours. We express geometric rates in physical energy, leaving that normalization explicit. Disjoint smearing supports commute, hence $\mathcal{N}\subseteq\mathcal{M}'$. The cut specifies null-ray access; the algebras by themselves do not specify a detector coupling or a unique emission point.

<a id="eq:access-cut"></a>

$$
\underbrace{(-\infty,0)}_{\text{honest source and verifier}}
\,\big|\,
\underbrace{(0,\infty)}_{\text{excluded actor}}.\tag{26}
$$

Choose $a>0$ and a nonzero real profile $f\in C_c^\infty((-\infty,-a))$. The honest unitary is $U=W(f)\in\mathcal{N}$, and

<a id="eq:coherent-state"></a>

$$
\omega_f(X)
=\langle W(f)\Omega,XW(f)\Omega\rangle
=\omega_0(W(f)^*XW(f)).\tag{27}
$$

We first exhibit a bounded local verifier. For real $h\in C_c^\infty((-\infty,0))$, set

$$
d:=\omega_f(W(h))-\omega_0(W(h)).\tag{28}
$$

Whenever $d\ne0$, put $\theta=\arg d$ and define

<a id="eq:weyl-effect"></a>

$$
X_h=\frac{e^{-i\theta}W(h)+e^{i\theta}W(h)^*}{2},
\qquad
Q_h=\frac{\mathbf{1}+X_h}{2}.\tag{29}
$$

Because $X_h$ is the real part of a phase times a unitary, $-\mathbf{1}\le X_h\le\mathbf{1}$ and $Q_h$ is an effect in $\mathcal{N}$. Its expectation gap is $|d|/2>0$. With Eq. [(24)](#eq:symplectic), $\omega_f(W(h))=e^{i\sigma(f,h)}\omega_0(W(h))$. The gap has the closed form

<a id="eq:explicit-weyl-gap"></a>

$$
\omega_f(Q_h)-\omega_0(Q_h)
=\left|\sin\frac{\sigma(f,h)}{2}\right|
e^{-v_h/2}.\tag{30}
$$

Such an $h$ always exists. The symplectic form is a nonzero multiple of $-\int f'(u)h(u)\,du$. Since a nonzero compactly supported $f$ has $f'\ne0$, one may choose a bump $h$ supported where $f'$ is nonzero and then rescale it so that $\sigma(f,h)\notin2\pi\mathbb Z$. Equation [(30)](#eq:explicit-weyl-gap) also displays the verifier-design tradeoff: scaling $h$ increases the symplectic phase but incurs a Gaussian penalty through $v_h$.

<a id="a-bounded-region-detector"></a>

### A bounded-region detector

Choose a bounded interval $I\subset(-\infty,0)$ containing the supports of $f,h$, with $\mu=\sigma(f,h)>0$ and $v=v_h>0$. The quadrature $j(h)$ has laws $N(\mu,v)$ and $N(0,v)$ in the honest and reference states. Allow independent calibrated Gaussian readout noise of variance $v_d\ge0$. On $n$ independent copies, accept if the mean readout exceeds

$$
t_n=\mu-\sqrt{(v+v_d)/n}\,z_\delta,\quad
z_\delta=\Phi^{-1}(1-\delta),\tag{31}
$$

where $\Phi$ is the standard normal distribution function. The induced effect belongs to $\mathcal{A}(I)^{\bar\otimes n}$. Its completeness is exactly $1-\delta$ and its worst-case joint forgery probability is

<a id="eq:local-homodyne"></a>

$$
q_n=\overline\Phi\!\left(\frac{\sqrt n\mu}{\sqrt{v+v_d}}-z_\delta\right),
\qquad \overline\Phi=1-\Phi.\tag{32}
$$

This follows from the Gaussian law of the sample mean and Theorem [1](#thm:locality), including arbitrary collective attacks. The measured exponent is $\mu^2/[2(v+v_d)]$. The assumed quadrature coupling and independent noise are a detector model, not consequences of modular theory. Finite readout resolution can instead be included in the deployed effect and its calibrated reference acceptance.

<a id="the-full-half-line-exponent"></a>

### The full half-line exponent

Write the physical coherent energy density as

<a id="eq:energy-density"></a>

$$
\rho_f(u)=c_j(f'(u))^2,\quad c_j>0,\qquad
E_f=\int_{-\infty}^{0}\rho_f(u)\,du.\tag{33}
$$

Here $c_j$ is fixed by the same current as $\sigma,v_h$; no independent choice of these constants is permitted. Geometric modular covariance makes the vacuum modular flow act by dilations about the cut \[[18](#ref-bisognano1975duality), [19](#ref-bisognano1976duality), [20](#ref-brunetti1993modular)\]. Coherent-state relative entropy formulas then give \[[21](#ref-longo2019entropy), [22](#ref-casini2019coherent), [23](#ref-bostelmann2022relative)\]

<a id="eq:current-entropy"></a>

$$
\begin{split}
D_{\mathcal{N}}(\omega_f\|\omega_0)
&=2\pi\int_{-\infty}^{0}(-u)\rho_f(u)\,du\\
&=:M_f.
\end{split}\tag{34}
$$

The factor $-u$ weights energy by its null distance from the cut. This is the modular-energy functional that underlies the relative-entropy formulation of the Bekenstein bound \[[24](#ref-casini2008bekenstein)\]. Since the packet lies in $u\le-a$,

<a id="eq:standoff"></a>

$$
M_f\ge2\pi aE_f.\tag{35}
$$

The half-line algebra is $\sigma$-finite in the vacuum representation; the vacuum and coherent states are faithful and normal; and compact support makes $M_f$ finite. Theorem [2](#thm:stein) therefore gives, for fixed $0<\delta<1/2$,

<a id="eq:explicit-rate"></a>

$$
\beta_\delta^{(n)}
=\exp[-nM_f+o(n)].\tag{36}
$$

For a coherent packet with mean occupation $\bar n>0$, define its mean angular frequency by $\bar\omega:=E_f/\bar n$ and set $\lambda_{\mathrm{eff}}=2\pi/\bar\omega$ in units $\hbar=c=1$. Then

<a id="eq:geometry-energy"></a>

$$
M_f\ge
4\pi^2\,\frac{a}{\lambda_{\mathrm{eff}}}\,\bar n.\tag{37}
$$

For a narrowband packet, $\lambda_{\mathrm{eff}}$ agrees with the central wavelength up to the relative bandwidth. Distance from the cut and packet energy therefore increase the exponent optimized over the entire half-line algebra. Equation [(37)](#eq:geometry-energy) is a lower bound on the asymptotic exponent, not a one-shot false-acceptance formula.

The distinction between the full algebra and a deployed receiver matters. Translate $f$, $h$, and the fixed-size detector interval together farther from the cut. Vacuum translation invariance leaves $\mu$, $v$, and the finite-detector performance in Eq. [(32)](#eq:local-homodyne) unchanged, whereas $M_f$ grows. The additional half-line exponent requires a different measurement that uses more of the available algebra. Equation [(37)](#eq:geometry-energy) is therefore not a performance gain for a translated fixed apparatus.

<a id="scope"></a>

## Scope

<a id="sec:limits"></a>

Acceptance rules out only the adversary model specified by the excluded algebra and reference state. It does not identify the emitter, prove possession of a secret, locate a unique event, or provide secrecy. The number $q$ is a false-positive probability, not a posterior probability that an accepted event was honest.

The reference assumptions are part of the claim. Each invocation must begin in the prescribed field state, with adversarial memory initially independent of it. Initial field-memory correlations require a new joint reference state. The Stein rate further assumes independent honest and reference copies. Several modes in one correlated vacuum need not realize this tensor-product model and require a separate hypothesis-testing analysis.

Exact one-shot soundness also requires the deployed effect to commute with the adversary algebra. Equation [(11)](#eq:approx-locality) isolates a known localization error, while Eq. [(12)](#eq:calibration) accommodates noise and loss through the measured reference acceptance. Deriving the localization error from a detector coupling remains model dependent.

Perfect local one-shot authentication is unavailable in standard vacuum representations. The Reeh-Schlieder property makes the vacuum separating for a local algebra, so every nonzero local effect has positive vacuum expectation \[[25](#ref-reeh1961bemerkungen), [26](#ref-witten2018aps)\]. Authentication is therefore statistical.

Finally, Theorem [1](#thm:locality) applies to each authorized invocation. Reuse requires scheduling, fresh-reference accounting, and replay protection. The result is neither a key-establishment protocol nor a composable security theorem.

<a id="conclusion"></a>

## Conclusion

<a id="sec:conclusion"></a>

Locality turns a causal cut into an authentication resource. For any fixed local test, the exact worst-case forgery probability is its reference acceptance. A bounded effect and classical thresholding amplify any local statistical gap, while optimized collective tests converge at the Araki relative-entropy rate. In the chiral current this optimized half-line rate is a weighted null energy. A detector confined to a bounded interval has its own achievable rate, which need not improve when moved with the pulse. The resulting certificate concerns causal access, with explicit reference and localization assumptions.

<a id="ai-assistance"></a>

## AI assistance

The research vision and original ideas are the author's. The author used OpenAI's GPT models, including Astra, and Anthropic's Claude Opus models for writing, theorem proving, and literature review. GPT models were used most often, and Astra was the most useful overall. This work is in progress. Not all claims have been verified by a human.

<a id="references"></a>

## References

<a id="ref-haag1964algebraic"></a>

\[1\]

Rudolf Haag and Daniel Kastler. An algebraic approach to quantum field theory. *Journal of Mathematical Physics*, 5(7):848–861, 1964.

<a id="ref-hayden2019localizing"></a>

\[2\]

Patrick Hayden and Alex May. Localizing and excluding quantum information; or, how to share a quantum secret in spacetime. *Quantum*, 3:196, 2019.

<a id="ref-kent2014secure"></a>

\[3\]

Adrian Kent, Serge Massar, and Jonathan Silman. Secure and robust transmission and verification of unknown quantum states in minkowski space. *Scientific Reports*, 4(1):3901, 2014.

<a id="ref-kent2011quantum"></a>

\[4\]

Adrian Kent, William J. Munro, and Timothy P. Spiller. Quantum tagging: Authenticating location via quantum information and relativistic signaling constraints. *Physical Review A*, 84(1):012326, 2011.

<a id="ref-chandran2009position"></a>

\[5\]

Nishanth Chandran, Vipul Goyal, Ryan Moriarty, and Rafail Ostrovsky. Position based cryptography. In *Annual International Cryptology Conference*, pages 391–407. Springer, 2009.

<a id="ref-buhrman2014position"></a>

\[6\]

Harry Buhrman, Nishanth Chandran, Serge Fehr, Ran Gelles, Vipul Goyal, Rafail Ostrovsky, and Christian Schaffner. Position-based quantum cryptography: Impossibility and constructions. *SIAM Journal on Computing*, 43(1):150–178, 2014.

<a id="ref-sorkin1993impossible"></a>

\[7\]

Rafael D Sorkin. Impossible measurements on quantum fields. In *Directions in general relativity: Proceedings of the 1993 International Symposium, Maryland*, volume 2, pages 293–305, 1993.

<a id="ref-jubb2022causal"></a>

\[8\]

I Jubb. Causal state updates in real scalar quantum field theory. *Physical Review D*, 105(2):025003, 2022.

<a id="ref-fewster2020measurement"></a>

\[9\]

Christopher J. Fewster and Rainer Verch. Quantum fields and local measurements. *Communications in Mathematical Physics*, 378(2):851–889, 2020.

<a id="ref-bostelmann2021impossible"></a>

\[10\]

Henning Bostelmann, Christopher J Fewster, and Maximilian H Ruep. Impossible measurements require impossible apparatus. *Physical Review D*, 103(2):025017, 2021.

<a id="ref-kitajima2018local"></a>

\[11\]

Yuichiro Kitajima. Local operations and completely positive maps in algebraic quantum field theory. In *Reality and Measurement in Algebraic Quantum Theory*, volume 261 of *Springer Proceedings in Mathematics & Statistics*, pages 83–95. Springer, 2018.

<a id="ref-hoeffding1963probability"></a>

\[12\]

Wassily Hoeffding. Probability inequalities for sums of bounded random variables. *Journal of the American statistical association*, 58(301):13–30, 1963.

<a id="ref-araki1976relative"></a>

\[13\]

Huzihiro Araki. Relative entropy of states of von Neumann algebras. *Publications of the Research Institute for Mathematical Sciences*, 11(3):809–833, 1975.

<a id="ref-uhlmann1977relative"></a>

\[14\]

Armin Uhlmann. Relative entropy and the Wigner-Yanase-Dyson-Lieb concavity in an interpolation theory. *Communications in Mathematical Physics*, 54(1):21–32, 1977.

<a id="ref-hiai1991proper"></a>

\[15\]

Fumio Hiai and Dénes Petz. The proper formula for relative entropy and its asymptotics in quantum probability. *Communications in Mathematical Physics*, 143:99–114, 1991.

<a id="ref-ogawa2000strong"></a>

\[16\]

Tomohiro Ogawa and Hiroshi Nagaoka. Strong converse and Stein's lemma in quantum hypothesis testing. *IEEE Transactions on Information Theory*, 46(7):2428–2433, 2000.

<a id="ref-pautrat2023ke"></a>

\[17\]

Yan Pautrat and Simeng Wang. Ke Li's lemma for quantum hypothesis testing in general von Neumann algebras. *Annales Henri Poincaré*, 24(7):2323–2339, 2023.

<a id="ref-bisognano1975duality"></a>

\[18\]

Joseph J Bisognano and Eyvind H Wichmann. On the duality condition for a hermitian scalar field. *Journal of Mathematical Physics*, 16(4):985–1007, 1975.

<a id="ref-bisognano1976duality"></a>

\[19\]

Joseph J Bisognano and Eyvind H Wichmann. On the duality condition for quantum fields. *Journal of mathematical physics*, 17(3):303–321, 1976.

<a id="ref-brunetti1993modular"></a>

\[20\]

Romeo Brunetti, D Guido, and Roberto Longo. Modular structure and duality in conformal quantum field theory. *Communications in Mathematical Physics*, 156(1):201–219, 1993.

<a id="ref-longo2019entropy"></a>

\[21\]

Roberto Longo. Entropy of coherent excitations. *Letters in Mathematical Physics*, 109(12):2587–2600, 2019.

<a id="ref-casini2019coherent"></a>

\[22\]

Horacio Casini, Sergio Grillo, and Diego Pontello. Relative entropy for coherent states from Araki formula. *Physical Review D*, 99(12):125020, 2019.

<a id="ref-bostelmann2022relative"></a>

\[23\]

Henning Bostelmann, Daniela Cadamuro, and Simone Del Vecchio. Relative entropy of coherent states on general CCR algebras. *Communications in Mathematical Physics*, 389(1):661–691, 2022.

<a id="ref-casini2008bekenstein"></a>

\[24\]

Horacio Casini. Relative entropy and the Bekenstein bound. *Classical and Quantum Gravity*, 25(20):205021, 2008.

<a id="ref-reeh1961bemerkungen"></a>

\[25\]

Helmut Reeh and Siegfried Schlieder. Bemerkungen zur unitären Äquivalenz von Lorentzinvarianten Feldern. *Il Nuovo Cimento*, 22(5):1051–1068, 1961.

<a id="ref-witten2018aps"></a>

\[26\]

Edward Witten. APS medal for exceptional achievement in research: Invited article on entanglement properties of quantum field theory. *Reviews of Modern Physics*, 90(4):045003, 2018.
