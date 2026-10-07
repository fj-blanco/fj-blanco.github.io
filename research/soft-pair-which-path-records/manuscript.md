# Soft-pair which-path records from a gapped detector

Javier Blanco-Romero

Department of Telematic Engineering, Universidad Carlos III de Madrid, Leganés, Madrid, Spain

<a id="abstract"></a>

## Abstract

An internal energy gap suppresses detector excitation, but leaves a soft pair-emission channel open. We calculate the path information carried by this channel for a ground-state Unruh–DeWitt detector held in a superposition of two fixed positions in the Minkowski vacuum. For a massless scalar field in $3+1$ dimensions and a pulse stretched as $\chi(t/T)$, the second-order visibility loss decreases faster than every inverse power of $T$. The fourth-order term instead scales as $T^{-4}$. We give its coefficient for real Schwartz pulses and show that it is independent of the fixed, normalized spatial profile at leading order. A Gaussian pulse gives $\lambda^4d^2/(60\pi^3\Omega^2T^4)$, with coupling $\lambda$, separation $d$, and gap $\Omega$. A joint weak-coupling, slow-switching limit controls the full observable and makes the final excitation probability negligible compared with the visibility loss. Conditioning on the detector returning to its ground state therefore retains the leading field record.

<a id="introduction"></a>

## Introduction

A detector in its ground state can respond very weakly to a slowly switched vacuum interaction. This does not by itself establish that the field has retained little information about the detector's position. A final state containing the ground-state detector and two arbitrarily soft quanta remains available, even when the internal energy gap is finite.

Detectors in superpositions of trajectories provide a direct setting in which to distinguish these questions \[[1](#ref-Foo2020), [2](#ref-Gooding2026)\]. The difference between reversible field dressing and a final loss of interference is well established \[[3](#ref-Unruh2000), [4](#ref-GundhiBassi2023)\]. Recent analyses have clarified the role of switching in producing a final field record \[[5](#ref-Gundhi2024), [6](#ref-GundhiUlbricht2025)\].

Pair creation below an internal excitation threshold is known from the microscopic dynamical Casimir effect \[[7](#ref-Souza2018), [8](#ref-LoLaw2018), [9](#ref-Farias2019)\]. Its relation to decoherence also has a long history \[[10](#ref-Dalvit2000)\]. In particular, a fifth-power low-frequency spectrum already occurs in the scalar oscillator model of Ref. \[[9](#ref-Farias2019)\]. Related work treats the internal degree of freedom and field as a composite environment \[[11](#ref-Sinha2021)\], and derives spatial decoherence for stationary accelerated motion \[[12](#ref-Jakubec2026)\].

Here we calculate the final, unconditional path visibility for two static branches and a stretched switching pulse. We obtain the soft-pair coefficient, control the higher-order remainder, and show that the excitation probability can be asymptotically smaller than the loss of interference. This separates two observables often identified at second order: the response of the internal detector and the information left in the field.

We use two stationary branches so that switching, rather than acceleration, is the only drive. This restriction also permits an exact relation between path coherence and the distribution of total field momentum. All results below concern a free massless scalar field in $3+1$-dimensional Minkowski spacetime. We set $\hbar=c=1$.

<a id="model-and-path-observable"></a>

## Model and path observable

Let the two positions be $\boldsymbol{x}_A$ and $\boldsymbol{x}_B$, with $\boldsymbol{d}=\boldsymbol{x}_B-\boldsymbol{x}_A$ and $d=|\boldsymbol{d}|$. The interaction-picture Hamiltonian on either branch is

<a id="eq:H"></a>

$$
\begin{aligned}
H_X(t)&=\lambda\chi_T(t)\mu(t)\Phi_{\boldsymbol{x}_X}(t),
 &\chi_T(t)&=\chi(t/T),\qquad\text{(1)}\\
\mu(t)&=\sigma^+\mathrm{e}^{\mathrm{i}\Omega t}+\sigma^-\mathrm{e}^{-\mathrm{i}\Omega t},
 &\Omega&>0.
\end{aligned}
$$

Here $\lambda$ is dimensionless. We take $\chi\in\mathcal{S}(\mathbb R)$ to be real and nonzero; a smooth compactly supported function is allowed. The smeared field is

<a id="eq:smear"></a>

$$
\Phi_{\boldsymbol{x}}(t)=\int\mathrm{d}^3\boldsymbol{y}\,f(\boldsymbol{y}-\boldsymbol{x})\phi(t,\boldsymbol{y}),
 \qquad \int\mathrm{d}^3\boldsymbol{y}\,f(\boldsymbol{y})=1,\tag{2}
$$

where $f\in\mathcal{S}(\mathbb R^3)$ is real and radial. A fixed nonzero spatial width is retained throughout the perturbative calculation. Spatial profiles and higher-order detector calculations require care \[[13](#ref-Hummer2016)\]; no pointlike limit of the full theory is used here. The profile and Hamiltonian are defined in the common rest frame of the two branches.

Our Fourier conventions are

<a id="eq:fourier"></a>

$$
\widehat\chi(\nu)=\int\mathrm{d}s\,\chi(s)\mathrm{e}^{\mathrm{i}\nu s},
 \qquad \widetilde f(\boldsymbol{k})=\int\mathrm{d}^3\boldsymbol{y}\,f(\boldsymbol{y})\mathrm{e}^{-\mathrm{i}\boldsymbol{k}\cdot\boldsymbol{y}}.\tag{3}
$$

With $k=|\boldsymbol{k}|$ and $[a_{\boldsymbol{k}},a_{\boldsymbol{p}}^{\dagger}]=\delta^3(\boldsymbol{k}-\boldsymbol{p})$, the creation part of $\Phi_{\boldsymbol{x}}$ is

<a id="eq:modes"></a>

$$
\Phi_{\boldsymbol{x}}^{(+)}(t)=\int\mathrm{d}^3\boldsymbol{k}\,b(k)\mathrm{e}^{\mathrm{i}kt-\mathrm{i}\boldsymbol{k}\cdot\boldsymbol{x}}a_{\boldsymbol{k}}^{\dagger},
 \quad b(k)=\frac{\widetilde f(k)}{\sqrt{2k(2\pi)^3}}.\tag{4}
$$

Initially the detector is in $\lvert g\rangle$, the field in $\lvert 0\rangle$, and the paths have equal amplitudes. Write

<a id="eq:visibility"></a>

$$
\lvert \Psi_X\rangle=U_X\lvert g,0\rangle,\qquad
 \mathcal{C}_T=\langle\Psi_A|\Psi_B\rangle,\qquad
 \mathcal{V}_T=|\mathcal{C}_T|.\tag{5}
$$

The visibility is unconditional: neither the internal state nor the field is measured or postselected. The paths are split and recombined with the interaction off. For Schwartz pulses this is an asymptotic protocol; compactly supported pulses permit exact finite-time separation of these operations. Recoil, control noise, and motion during the interaction are excluded.

Let $\lvert \Psi_{\rm ref}\rangle$ denote the final state for a detector at the origin, and let $\boldsymbol{P}$ be the free-field momentum. Translation covariance gives

<a id="eq:translation"></a>

$$
\lvert \Psi_X\rangle=\mathrm{e}^{-\mathrm{i}\boldsymbol{P}\cdot\boldsymbol{x}_X}\lvert \Psi_{\rm ref}\rangle,
 \qquad
 \mathcal{C}_T=\langle \Psi_{\rm ref}\rvert\mathrm{e}^{-\mathrm{i}\boldsymbol{P}\cdot\boldsymbol{d}}\lvert \Psi_{\rm ref}\rangle.\tag{6}
$$

Parity makes this overlap real. In the weak-coupling region where $\mathcal{C}_T>0$, define

<a id="eq:momentum"></a>

$$
D_{\boldsymbol{d}}=1-\cos(\boldsymbol{P}\cdot\boldsymbol{d}),\qquad
 1-\mathcal{V}_T=\langle \Psi_{\rm ref}\rvert D_{\boldsymbol{d}}\lvert \Psi_{\rm ref}\rangle.\tag{7}
$$

This identity is exact. The positive operator $D_{\boldsymbol{d}}$ annihilates the vacuum and preserves field particle number. Branch-independent vacuum phases therefore drop out before any expansion is made. A pair is resolved through its *total* momentum, not through its particle number alone.

<a id="the-channel-missed-at-second-order"></a>

## The channel missed at second order

Expand the reference-branch state as

$$
\lvert \Psi_{\rm ref}\rangle=\sum_{n=0}^{\infty}\lambda^n\lvert \psi_n(T)\rangle,
 \qquad \lvert \psi_0\rangle=\lvert g,0\rangle.\tag{8}
$$

Equation [(7)](#eq:momentum) yields, at fixed $T$,

<a id="eq:series"></a>

$$
1-\mathcal{V}_T=\lambda^2v_2(T)+\lambda^4v_4(T)+R_6(\lambda,T),
 \quad R_6=O_T(\lambda^6),\tag{9}
$$

where

<a id="eq:v2state"></a>

<a id="eq:v4state"></a>

$$
\begin{aligned}
v_2&=\langle \psi_1\rvert D_{\boldsymbol{d}}\lvert \psi_1\rangle,\qquad\text{(10)}\\
v_4&=\langle \psi_2\rvert D_{\boldsymbol{d}}\lvert \psi_2\rangle
       +2\operatorname{Re}\langle \psi_1\rvert D_{\boldsymbol{d}}\lvert \psi_3\rangle.\qquad\text{(11)}
\end{aligned}
$$

Odd orders vanish by field parity. The first coefficient is equivalently half the squared distance between the first-order branch states.

The first-order state contains an excited detector and one quantum, with amplitude $-\mathrm{i}b(k)\widehat\chi_T(k+\Omega)$. Angular integration gives

<a id="eq:v2"></a>

$$
v_2(T)=\frac{1}{4\pi^2}\int_0^{\infty}\mathrm{d}k\,k|\widetilde f(k)|^2
 |\widehat\chi_T(k+\Omega)|^2[1-\operatorname{sinc}(kd)],\tag{12}
$$

where $\operatorname{sinc}z=\sin z/z$ and $\widehat\chi_T(\nu)=T\widehat\chi(T\nu)$. Since $k+\Omega\geq\Omega>0$,

<a id="eq:super"></a>

$$
v_2(T)=O_N(T^{-N})\quad\text{for every }N>0.\tag{13}
$$

The same bound holds for $\|\psi_1(T)\|$. At fixed smearing, $\|\psi_3(T)\|=O(T^3)$, so the last term of Eq. [(11)](#eq:v4state) also decreases faster than every inverse power. The remaining term need not do so.

The second-order state contains a vacuum part and a two-particle part, both with the detector in $\lvert g\rangle$. Denote the latter by $\lvert \zeta_T\rangle$. The Dyson expansion gives

<a id="eq:pair"></a>

$$
\lvert \zeta_T\rangle=\int\mathrm{d}^3\boldsymbol{k}\,\mathrm{d}^3\boldsymbol{p}\,
 b(k)b(p)F_T(k,p)a_{\boldsymbol{k}}^{\dagger}a_{\boldsymbol{p}}^{\dagger}\lvert g,0\rangle,\tag{14}
$$

with the symmetric kernel

<a id="eq:F"></a>

$$
\begin{aligned}
F_T(k,p)={}&-\int_{-\infty}^{\infty}\mathrm{d}u\,\mathrm{e}^{\mathrm{i}(k+p)u}
 \int_0^{\infty}\mathrm{d}r\,\mathrm{e}^{-\mathrm{i}\Omega r}\\
&\times\chi_T(u+r/2)\chi_T(u-r/2)
 \cos[(k-p)r/2].\qquad\text{(15)}
\end{aligned}
$$

Here $u=(t+t')/2$ and $r=t-t'\geq0$ are the mean time and the ordered time difference. Symmetrizing the two creation operators produces the cosine. There is no additional $1/2$ in Eq. [(14)](#eq:pair).

The two vacuum contractions in $\|\zeta_T\|^2$ give a factor of two. Using Eq. [(7)](#eq:momentum), the exact two-particle contribution to the fourth-order coefficient is

<a id="eq:pairvisibility"></a>

<a id="eq:pairdominates"></a>

$$
\begin{aligned}
v_{4,\mathrm{pair}}(T)={}&\frac{1}{8\pi^4}\int_0^{\infty}\mathrm{d}k\,\mathrm{d}p\,kp
 |\widetilde f(k)\widetilde f(p)|^2|F_T(k,p)|^2\\
&\times[1-\operatorname{sinc}(kd)\operatorname{sinc}(pd)],\qquad\text{(16)}\\
v_4(T)={}&v_{4,\mathrm{pair}}(T)+O_N(T^{-N}).\qquad\text{(17)}
\end{aligned}
$$

The product of sinc functions follows from averaging $\cos[(\boldsymbol{k}+\boldsymbol{p})\cdot\boldsymbol{d}]$ over the two independent directions. A sum of single-quantum losses does not give the same factor before taking the soft limit.

<a id="a-fourth-order-soft-pair-law"></a>

## A fourth-order soft-pair law

Set $h(s)=\chi(s)^2$ and define

<a id="eq:K"></a>

$$
\mathcal{K}[\chi]=\int_0^{\infty}\mathrm{d}q\,q^5|\widehat h(q)|^2.\tag{18}
$$

For fixed $d>0$, $\Omega>0$, and the profiles specified above, our main result is

<a id="eq:main"></a>

$$
\boxed{\displaystyle
 v_4(T)=\frac{d^2\mathcal{K}[\chi]}{480\pi^4\Omega^2T^4}+o(T^{-4}).}\tag{19}
$$

The coefficient is strictly positive: $\widehat h(0)=\int\chi(s)^2\mathrm{d}s>0$, and $\widehat h$ is continuous. It depends on the pulse shape but not on the spatial profile beyond $\widetilde f(0)=1$. Equation [(19)](#eq:main) is a statement about the fourth-order coefficient; an unrestricted fixed-$\lambda$ limit does not follow from it.

To derive it, put $k=a/T$ and $p=b/T$ in Eq. [(15)](#eq:F), then rescale both times. The integrand of the half-line time integral is even at its endpoint. Integration by parts therefore gives, for fixed $a,b\geq0$,

<a id="eq:softF"></a>

$$
F_T(a/T,b/T)=\frac{\mathrm{i}T}{\Omega}\widehat h(a+b)
       +O\!\left(\frac{1}{\Omega^3T}\right).\tag{20}
$$

The term proportional to $\Omega^{-2}$ vanishes because the first endpoint derivative is zero. Meanwhile,

<a id="eq:softgeometry"></a>

$$
T^2[1-\operatorname{sinc}(ad/T)\operatorname{sinc}(bd/T)]
 \longrightarrow\frac{d^2}{6}(a^2+b^2).\tag{21}
$$

Substitution into Eq. [(16)](#eq:pairvisibility) gives

<a id="eq:limitintegral"></a>

$$
\begin{aligned}
\lim_{T\to\infty}T^4v_{4,\mathrm{pair}}(T)
 &=\frac{d^2}{48\pi^4\Omega^2}\\
&\quad\times\int_0^{\infty}\mathrm{d}a\,\mathrm{d}b\,ab(a^2+b^2)|\widehat h(a+b)|^2.\qquad\text{(22)}
\end{aligned}
$$

The passage to this limit is justified in Appendix [A](#app:bounds). With $q=a+b$ and $x=a/q$, the remaining integral separates. In particular,

$$
\int_0^1\mathrm{d}x\,x(1-x)[x^2+(1-x)^2]=\frac{1}{10},\tag{23}
$$

which proves Eq. [(19)](#eq:main).

The soft kernel can also be read from the effective interaction

<a id="eq:effective"></a>

$$
H^{(g)}_{\mathrm{eff},X}(t)
 =-\frac{\lambda^2}{\Omega}\chi_T(t)^2:\!\Phi_{\boldsymbol{x}_X}(t)^2\!:\,.\tag{24}
$$

This is the low-frequency ground-state interaction obtained by eliminating a virtual internal excitation, up to a common vacuum phase. Such effective quadratic couplings underlie microscopic dynamical Casimir radiation \[[7](#ref-Souza2018), [8](#ref-LoLaw2018), [9](#ref-Farias2019)\]. Equation [(20)](#eq:softF) derives the needed limit directly from the original Hamiltonian; Eq. [(24)](#eq:effective) is not used at high frequency or as an exact replacement for that Hamiltonian.

There are two factors in the $T^{-4}$ law. Pair creation has probability of order $\lambda^4/(\Omega^2T^2)$. The emitted wavelengths are of order $T$, so resolving fixed arms costs a further factor $d^2/T^2$. The internal detector is left in the same ground state on both branches. The record in this channel is carried by the field.

<a id="visibility-without-an-internal-excitation"></a>

## Visibility without an internal excitation

A comparison of perturbative coefficients alone leaves an order-of-limits problem. For any fixed pulse and profile specified above, take $\lambda\to0^+$ and

<a id="eq:jointscale"></a>

$$
T(\lambda)=\Omega^{-1}\lambda^{-\beta},
 \qquad 0<\beta<\frac15.\tag{25}
$$

Then the *full* visibility obeys

<a id="eq:joint"></a>

$$
\boxed{\displaystyle
 1-\mathcal{V}_{T(\lambda)}\sim
 \frac{\lambda^4d^2\mathcal{K}[\chi]}{480\pi^4\Omega^2T(\lambda)^4}.}\tag{26}
$$

Indeed, $v_2(T)=O_N(T^{-N})$ makes $\lambda^2v_2=o(\lambda^4T^{-4})$ by choosing $N>4+2/\beta$. At fixed smearing, the Dyson bound in Appendix [A](#app:bounds) gives $R_6=O(\lambda^6T^6)$ when $\lambda B_fT\ll1$. Relative to the pair term this is $O(\lambda^2T^{10})=O(\lambda^{2-10\beta})$. The range of $\beta$ is sufficient, not asserted to be optimal.

Let $P_e$ be the probability of finding the internal detector excited after the pulse. Only odd Dyson orders enter its amplitude. The same bound gives

<a id="eq:noexcitation"></a>

$$
\begin{aligned}
P_e&\leq 2\lambda^2\|\psi_1(T)\|^2+O(\lambda^6T^6),\\
\frac{P_e}{1-\mathcal{V}_T}&\longrightarrow0
 \quad\text{along Eq.~\href{#eq:jointscale}{(25)}}.\qquad\text{(27)}
\end{aligned}
$$

Thus the small excitation probability does not account for the leading loss of path coherence.

A final internal measurement isolates the pair channel. Let $\mathcal{V}_g$ be the visibility conditioned on a ground-state outcome. The excited one-particle sector is then absent, and the vacuum is annihilated by $D_{\boldsymbol{d}}$. At any fixed $T$,

<a id="eq:conditional4"></a>

$$
1-\mathcal{V}_g=\lambda^4v_{4,\mathrm{pair}}(T)+O_T(\lambda^6).\tag{28}
$$

Normalization by the ground-state probability changes this expression only at sixth order. For the full conditional observable,

<a id="eq:conditional"></a>

$$
|\mathcal{V}_g-\mathcal{V}_T|\leq\frac{2P_e}{1-P_e},
 \qquad 1-\mathcal{V}_g\sim1-\mathcal{V}_T.\tag{29}
$$

To obtain the bound, split the branch overlap as $\mathcal{C}_T=\mathcal{C}_g+\mathcal{C}_e$. Both branches have the same $P_e$, $|\mathcal{C}_e|\leq P_e$, and $\mathcal{V}_g=|\mathcal{C}_g|/(1-P_e)$. A ground-state outcome retains the leading soft-pair record.

<a id="gaussian-example"></a>

## Gaussian example

For $\chi(s)=\mathrm{e}^{-s^2/2}$, both time integrals in Eq. [(15)](#eq:F) can be evaluated. Defining $w(z)=\mathrm{e}^{-z^2}\operatorname{erfc}(-\mathrm{i}z)$, $z=\Omega T$, and $\delta=(k-p)T/2$, one obtains

<a id="eq:gaussianF"></a>

$$
F_T(k,p)=-\frac{\pi T^2}{2}\mathrm{e}^{-(k+p)^2T^2/4}
 [w(-z+\delta)+w(-z-\delta)].\tag{30}
$$

This expression retains the full gap dependence and provides a direct check of the soft expansion. It applies with any of the fixed spatial profiles above; those profiles remain in Eq. [(16)](#eq:pairvisibility).

Here $\widehat h(q)=\sqrt\pi\mathrm{e}^{-q^2/4}$, and

<a id="eq:gauss4"></a>

$$
\mathcal{K}[\chi]=8\pi,\qquad
 v_4(T)\sim\frac{d^2}{60\pi^3\Omega^2T^4}.\tag{31}
$$

For comparison, Laplace expansion of Eq. [(12)](#eq:v2) gives

<a id="eq:gauss2"></a>

$$
v_2(T)\sim\frac{d^2}{32\pi\Omega^4T^6}\mathrm{e}^{-\Omega^2T^2}.\tag{32}
$$

The exponential suppression of the one-quantum channel is absent from the pair channel. At this order the final pair energy, $k+p$, can be arbitrarily small: $\Omega$ is the energy of an intermediate state, not a lower bound on the final field energy.

For this pulse a slower growth of $T$ also suffices: $\Omega T=\sqrt{a\log(1/\lambda)}$ with $a>2$. Here $\|\psi_1(T)\|^2=O(T^{-2}\mathrm{e}^{-\Omega^2T^2})$, so both the excitation bound and the remainder remain negligible relative to $\lambda^4T^{-4}$. This alternative scale gives the same full-visibility and conditional-visibility conclusions.

<a id="interpretation-and-scope"></a>

## Interpretation and scope

The energy comes from the switching, not from the vacuum. Smooth switching removes high-frequency transients, but a massless field still has modes slower than the pulse. A virtual detector transition couples those modes in pairs. Once the coupling is off, their branch-dependent state remains; subsequent common free evolution does not change the overlap. This is the sense in which the record is persistent. It does not preclude an active quantum eraser.

The result is not a nonzero lower bound on coherence. In the controlled limit [(25)](#eq:jointscale), the loss tends to zero. Rather, the result changes its rate and its physical channel. The second-order excitation probability can be exponentially small while the loss of path coherence is only algebraically small. Exponentiating the second-order response would miss this distinction: a gapped quantum detector does not generate the coherent states of a prescribed linear source.

The gap moves the first algebraic contribution to fourth order, where it is governed by $\widehat{\chi^2}$ rather than $\widehat\chi$. The limit $\Omega\to0$ cannot be taken in Eq. [(19)](#eq:main), whose derivation requires $\Omega T\gg1$.

Several restrictions matter. The field is massless, the arm separation and detector size remain fixed, and the *entire pulse* is stretched as $\chi(t/T)$. Increasing a holding time while keeping the switch-on and switch-off intervals fixed is a different limit. No claim is made here for moving paths, a thermal field, a charged particle in quantum electrodynamics, or a universal fixed-coupling adiabatic theorem. The dependence on $\widetilde f(0)$ does not license removal of the spatial regulator from higher-order vacuum terms.

The distinction is operational: an internal measurement can find the detector in its ground state while the field carries the leading path record. Equations [(19)](#eq:main), [(26)](#eq:joint), and [(29)](#eq:conditional) quantify this statement without identifying reduced internal response with preserved interference.

<a id="bounds-and-limits"></a>

## Bounds and limits

<a id="app:bounds"></a>

<a id="soft-frequency-limit-under-the-integral"></a>

### Soft-frequency limit under the integral

Define

$$
A(q,r)=\int\mathrm{d}s\,\mathrm{e}^{\mathrm{i}qs}\chi(s+r/2)\chi(s-r/2).\tag{33}
$$

It is a Schwartz function of $(q,r)$ and is even in $r$. Writing $M=\Omega T$, $q=a+b$, and $\delta_0=(a-b)/2$, Eq. [(15)](#eq:F) becomes

<a id="eq:rescaledF"></a>

$$
F_T(a/T,b/T)=-T^2\int_0^{\infty}\mathrm{d}r\,
 \mathrm{e}^{-\mathrm{i}Mr}A(q,r)\cos(\delta_0r).\tag{34}
$$

For fixed $a,b$, endpoint integration by parts gives Eq. [(20)](#eq:softF), since $A(q,0)=\widehat h(q)$ and $\partial_r A(q,0)=0$.

Uniform control follows by splitting at $q=M$. For $q\leq M$, the two phases have frequencies $M\pm\delta_0\geq M/2$. Integration by parts and the Schwartz bounds on $A$ imply

$$
\left|\frac{\Omega}{T}F_T(a/T,b/T)\right|
 \leq C_N(1+q)^{-N}.\tag{35}
$$

For $q>M$, direct integration gives the bound $C_NM(1+q)^{-N}$. Also,

$$
0\leq T^2[1-\operatorname{sinc}(ad/T)\operatorname{sinc}(bd/T)]
 \leq\frac{d^2}{6}(a^2+b^2).\tag{36}
$$

One way to see the last inequality is to average $1-\cos[(a\boldsymbol{n}+b\boldsymbol{m})\cdot\boldsymbol{d}/T]\leq[(a\boldsymbol{n}+b\boldsymbol{m})\cdot\boldsymbol{d}/T]^2/2$ over independent unit vectors. Since $\widetilde f$ is bounded, the rescaled integrand is dominated on $q\leq M$ by an integrable function. The $q>M$ tail is bounded by a constant times $M^2\int_M^{\infty}\mathrm{d}q\,q^5(1+q)^{-2N}$ and vanishes for sufficiently large $N$. This proves Eq. [(22)](#eq:limitintegral) without an unregulated exchange of limits.

<a id="higher-order-remainder"></a>

### Higher-order remainder

Let

$$
B_f^2=\int\mathrm{d}^3\boldsymbol{k}\,|b(k)|^2<\infty,
 \qquad z=2|\lambda|B_fT\|\chi\|_1.\tag{37}
$$

After $n$ interaction vertices, at most $n$ field quanta are present. The creation and annihilation bounds on each particle sector, followed by the ordered time integrals, give

<a id="eq:dysonbound"></a>

$$
\|\lambda^n\psi_n(T)\|\leq\frac{z^n}{\sqrt{n!}}.\tag{38}
$$

The detector monopole has operator norm one. As $D_{\boldsymbol{d}}$ is bounded by two and only even total orders survive, the terms of total order at least six in Eq. [(7)](#eq:momentum) are $O(z^6)$ as $z\to0$. This also keeps $\mathcal{C}_T$ positive in the regime used in Eq. [(26)](#eq:joint).

Equation [(38)](#eq:dysonbound) gives $\|\psi_3\|=O(T^3)$. The first-order norm decreases faster than every inverse power by the same Fourier bound as Eq. [(13)](#eq:super). Cauchy–Schwarz then proves Eq. [(17)](#eq:pairdominates). Along Eq. [(25)](#eq:jointscale), $z=O(\lambda^{1-\beta})\to0$ and $\lambda^6T^6=o(\lambda^4T^{-4})$. For the excited sector, the sum of odd orders starting at three has norm $O(z^3)$. Applying $\|u+v\|^2\leq2\|u\|^2+2\|v\|^2$ proves Eq. [(27)](#eq:noexcitation).

<a id="ai-assistance"></a>

## AI assistance

The research vision and original ideas are the author's. The author used OpenAI's GPT models, including Astra, and Anthropic's Claude Opus models for writing, theorem proving, and literature review. GPT models were used most often, and Astra was the most useful overall. This work is in progress. Not all claims have been verified by a human.

<a id="references"></a>

## References

<a id="ref-Foo2020"></a>

\[1\]

Joshua Foo, Sho Onoe, and Magdalena Zych. Unruh–deWitt detectors in quantum superpositions of trajectories. *Phys. Rev. D*, 102(8):085013, 2020.

<a id="ref-Gooding2026"></a>

\[2\]

Cisco Gooding, Taylor Cey, and Robert Mann. Testing superpositions of detector trajectories, 2026.

<a id="ref-Unruh2000"></a>

\[3\]

William G. Unruh. False loss of coherence. In Heinz-Peter Breuer and Francesco Petruccione, editors, *Relativistic Quantum Measurement and Decoherence*, volume 559 of *Lecture Notes in Physics*, pages 125–140. Springer, Berlin, Heidelberg, 2000.

<a id="ref-GundhiBassi2023"></a>

\[4\]

Anirudh Gundhi and Angelo Bassi. Motion of an electron through vacuum fluctuations. *Phys. Rev. A*, 107(6):062801, 2023.

<a id="ref-Gundhi2024"></a>

\[5\]

Anirudh Gundhi. Decoherence due to the Casimir effect? *Phys. Rev. D*, 110(11):116001, 2024.

<a id="ref-GundhiUlbricht2025"></a>

\[6\]

Anirudh Gundhi and Hendrik Ulbricht. Measuring decoherence due to quantum vacuum fluctuations. *Phys. Rev. Lett.*, 135(2):020402, 2025.

<a id="ref-Souza2018"></a>

\[7\]

Reinaldo de Melo e Souza, François Impens, and Paulo A. Maia Neto. Microscopic dynamical Casimir effect. *Phys. Rev. A*, 97(3):032514, 2018.

<a id="ref-LoLaw2018"></a>

\[8\]

Lezhi Lo and C. K. Law. Quantum radiation from a shaken two-level atom in vacuum. *Phys. Rev. A*, 98(6):063807, 2018.

<a id="ref-Farias2019"></a>

\[9\]

M. Belén Farías, C. D. Fosco, Fernando C. Lombardo, and Francisco D. Mazzitelli. Motion induced radiation and quantum friction for a moving atom. *Phys. Rev. D*, 100(3):036013, 2019.

<a id="ref-Dalvit2000"></a>

\[10\]

Diego A. R. Dalvit and Paulo A. Maia Neto. Decoherence via the dynamical Casimir effect. *Phys. Rev. Lett.*, 84(5):798–801, 2000.

<a id="ref-Sinha2021"></a>

\[11\]

Kanupriya Sinha, Adrián Ezequiel Rubio López, and Yiğit Subaşı. Dissipative dynamics of a particle coupled to a field via internal degrees of freedom. *Phys. Rev. D*, 103(5):056023, 2021.

<a id="ref-Jakubec2026"></a>

\[12\]

Clemens Jakubec, Aaron Bartleson, Peter W. Milonni, and Kanu Sinha. Decoherence of spatial superpositions along stationary worldlines, 2026.

<a id="ref-Hummer2016"></a>

\[13\]

Daniel Hümmer, Eduardo Martín-Martínez, and Achim Kempf. Renormalized Unruh–DeWitt particle detector models for boson and fermion fields. *Phys. Rev. D*, 93(2):024019, 2016.
