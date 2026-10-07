# Soft-pair which-path records from a gapped detector

Javier Blanco-Romero

Department of Telematic Engineering, Universidad Carlos III de Madrid, Leganés, Madrid, Spain

Work in progress. Results and proofs remain under review.

Abstract {#abstract .unnumbered}
--------

A two-level detector with an energy gap, switched on and off slowly, is almost never excited by the vacuum. It can still leave a record of where it was. We place a ground-state Unruh-DeWitt detector in a superposition of two fixed positions in the Minkowski vacuum of a massless scalar field and stretch its switching pulse by a time $T$. The one-quantum channel, which excites the detector, costs less visibility than any inverse power of $T$. A second channel stays open, in which a virtual excitation emits a pair of soft quanta and returns the detector to its ground state. This pair channel costs visibility at fourth order in the coupling and only as $T^{-4}$, with a coefficient set by the pulse shape and independent of the detector\'s spatial profile. In a joint weak-coupling and slow-switching limit, the pair channel controls the full visibility, the excitation probability is negligible in comparison, and a detector found in its ground state still carries the leading path record in the field.

Introduction
------------

Take a two-level detector with energy gap $\Omega$, hold it in a superposition of two places, and couple it to the vacuum of a massless field through a pulse that switches on and off over a long time $T$. The detector is almost never excited, because a slow pulse has no Fourier component at the frequency $\Omega$ it would need. It is tempting to conclude that the field learns almost nothing about the path. That conclusion is too quick. In second-order perturbation theory the detector can borrow its gap energy for a moment, emit two quanta of arbitrarily low frequency, and fall back to its ground state. Nothing forbids these soft pairs, since their total energy can be as small as the pulse allows, and they carry information about where the detector was.

Detectors on superposed trajectories have become a standard setting for asking such questions \[[1](#ref-Foo2020), [2](#ref-Gooding2026)\]. The difference between field dressing, which disappears when the coupling is switched off, and a lasting loss of interference is well understood \[[3](#ref-Unruh2000), [4](#ref-GundhiBassi2023)\], and recent work has clarified how switching produces a final field record \[[5](#ref-Gundhi2024), [6](#ref-GundhiUlbricht2025)\]. Pair creation below an internal excitation threshold is the microscopic dynamical Casimir effect \[[7](#ref-Souza2018), [8](#ref-LoLaw2018), [9](#ref-Farias2019)\], its link to decoherence has a long history \[[10](#ref-Dalvit2000)\], and the fifth-power low-frequency spectrum that drives our result already appears in the oscillator model of Ref. \[[9](#ref-Farias2019)\]. Related work treats the internal degree of freedom and the field as a composite environment \[[11](#ref-Sinha2021)\], and derives spatial decoherence for uniformly accelerated motion \[[12](#ref-Jakubec2026)\].

We compute the final path visibility $\mathcal{V}_T$ for two static branches separated by a distance $d$ and a pulse $\chi(t/T)$ with coupling $\lambda$. Keeping the branches static isolates the switching as the only drive. The one-quantum loss falls faster than any power of $T$, while the soft pairs give

$$1-\mathcal{V}_T\simeq\frac{\lambda^4d^2}{60\pi^3\Omega^2T^4}$$

for a Gaussian pulse. Two factors make up this law. A pair is created with probability of order $\lambda^4/(\Omega^2T^2)$, and its wavelengths are of order $T$, so resolving arms a distance $d$ apart costs a further $d^2/T^2$. The internal state of the detector is the same on both branches, and the record lives in the field. The detector\'s response and the information left in the field, two observables often identified at second order, separate at fourth.

Section [2](#sec:model) sets up the model and writes the visibility as a property of the total field momentum. Section [3](#sec:second) shows what second order misses, Sec. [4](#sec:law) derives the soft-pair law, and Sec. [5](#sec:joint) controls the full visibility and the ground-state conditioned one. Section [6](#sec:gauss) works out the Gaussian pulse. We use units with $\hbar=c=1$.

Model and path observable {#sec:model}
-------------------------

The two positions are $\bm x_A$ and $\bm x_B$, with $\bm d=\bm x_B-\bm x_A$ and $d=|\bm d|$. On either branch $X\in\{A,B\}$ the detector is an Unruh-DeWitt detector, a two-level system with ground state $\lvert g\rangle$, excited state $\lvert e\rangle$ and raising and lowering operators $\sigma^\pm$, coupled linearly to a free massless scalar field $\phi$ in $3+1$ dimensional Minkowski spacetime. In the interaction picture,

`<a id="eq:H"></a>`{=html} $$\begin{aligned}
 H_X(t)&=\lambda\chi_T(t)\mu(t)\Phi_{\bm x_X}(t),
 &\chi_T(t)&=\chi(t/T),\end{aligned}\tag{1}$$

$$\begin{aligned}
 \mu(t)&=\sigma^+\mathrm{e}^{\mathrm{i}\Omega t}+\sigma^-\mathrm{e}^{-\mathrm{i}\Omega t},
 &\Omega&>0,
\end{aligned}$$

with dimensionless coupling $\lambda$ and gap $\Omega$. The switching function $\chi$ is real, nonzero and a Schwartz function, $\chi\in\mathcal{S}(\mathbb R)$, meaning smooth with all derivatives decaying faster than any power; smooth compactly supported pulses are included. The parameter $T$ stretches the whole pulse. The detector samples the field over a fixed region,

`<a id="eq:smear"></a>`{=html} $$\Phi_{\bm x}(t)=\int\mathrm{d}^3\bm y\,f(\bm y-\bm x)\phi(t,\bm y),
 \qquad \int\mathrm{d}^3\bm y\,f(\bm y)=1,
\tag{2}$$

where the profile $f\in\mathcal{S}(\mathbb R^3)$ is real and radial. This fixed nonzero width regularizes the perturbative calculation, and no pointlike limit is taken, since spatial profiles matter in higher-order detector calculations \[[13](#ref-Hummer2016)\]. Profile and Hamiltonian are defined in the common rest frame of the two branches.

We Fourier transform with

`<a id="eq:fourier"></a>`{=html} $$\widehat\chi(\nu)=\int\mathrm{d}s\,\chi(s)\mathrm{e}^{\mathrm{i}\nu s},
 \qquad \widetilde f(\bm k)=\int\mathrm{d}^3\bm y\,f(\bm y)\mathrm{e}^{-\mathrm{i}\bm k\cdot\bm y}.
 
\tag{3}$$

With $k=|\bm k|$ and $[a_{\bm k},a_{\bm p}^{\dagger}]=\delta^3(\bm k-\bm p)$, the creation part of the smeared field is

`<a id="eq:modes"></a>`{=html} $$\Phi_{\bm x}^{(+)}(t)=\int\mathrm{d}^3\bm k\,b(k)\mathrm{e}^{\mathrm{i}kt-\mathrm{i}\bm k\cdot\bm x}a_{\bm k}^{\dagger},
 \quad b(k)=\frac{\widetilde f(k)}{\sqrt{2k(2\pi)^3}}.
\tag{4}$$

The detector starts in $\lvert g\rangle$, the field in its vacuum $\lvert 0\rangle$, and the two paths have equal amplitudes. If $U_X$ is the evolution along branch $X$, the final branch states, their overlap and the visibility are

`<a id="eq:visibility"></a>`{=html} $$\lvert \Psi_X\rangle=U_X\lvert g,0\rangle,\qquad
 \mathcal{C}_T=\langle\Psi_A|\Psi_B\rangle,\qquad
 \mathcal{V}_T=|\mathcal{C}_T|.
\tag{5}$$

Nothing is measured or postselected. The paths are split and recombined while the interaction is off, exactly for compactly supported pulses and asymptotically for Schwartz pulses. We ignore recoil, control noise and motion during the interaction.

The two branches differ only by a translation, which turns the visibility into a statement about momentum. Let $\lvert \Psi_{\rm ref}\rangle$ be the final state of a detector at the origin and $\bm P$ the total momentum of the free field. Then

`<a id="eq:translation"></a>`{=html} $$\lvert \Psi_X\rangle=\mathrm{e}^{-\mathrm{i}\bm P\cdot\bm x_X}\lvert \Psi_{\rm ref}\rangle,
 \qquad
 \mathcal{C}_T=\langle \Psi_{\rm ref}\rvert\mathrm{e}^{-\mathrm{i}\bm P\cdot\bm d}\lvert \Psi_{\rm ref}\rangle.
 
\tag{6}$$

Parity makes this overlap real, and in the weak-coupling regime, where $\mathcal{C}_T>0$,

`<a id="eq:momentum"></a>`{=html} $$D_{\bm d}=1-\cos(\bm P\cdot\bm d),\qquad
 1-\mathcal{V}_T=\langle \Psi_{\rm ref}\rvert D_{\bm d}\lvert \Psi_{\rm ref}\rangle.
 
\tag{7}$$

This identity is exact. The positive operator $D_{\bm d}$ annihilates the vacuum and preserves particle number, so branch-independent vacuum phases drop out before any expansion. The field resolves the path through the total momentum of the quanta it holds, so a pair counts according to how its two momenta add up.

What second order misses {#sec:second}
------------------------

Expand the reference state in the coupling,

$$\lvert \Psi_{\rm ref}\rangle=\sum_{n=0}^{\infty}\lambda^n\lvert \psi_n(T)\rangle,
 \qquad \lvert \psi_0\rangle=\lvert g,0\rangle.
\tag{8}$$

Equation [(7)](#eq:momentum) then gives, at fixed $T$,

`<a id="eq:series"></a>`{=html} $$1-\mathcal{V}_T=\lambda^2v_2(T)+\lambda^4v_4(T)+R_6(\lambda,T),
 \quad R_6=O_T(\lambda^6),
\tag{9}$$

where $O_T$ means a bound whose constant may depend on $T$, and

`<a id="eq:v2state"></a>`{=html} $$\begin{aligned}
 v_2&=\langle \psi_1\rvert D_{\bm d}\lvert \psi_1\rangle,\end{aligned}\tag{10}$$

`<a id="eq:v4state"></a>`{=html} $$\begin{aligned}
 v_4&=\langle \psi_2\rvert D_{\bm d}\lvert \psi_2\rangle
       +2\operatorname{Re}\langle \psi_1\rvert D_{\bm d}\lvert \psi_3\rangle.
\end{aligned}\tag{11}$$

Odd orders vanish by field parity, and $v_2$ is half the squared distance between the two first-order branch states.

At first order the detector is excited and one quantum is emitted, with amplitude $-\mathrm{i}b(k)\widehat\chi_T(k+\Omega)$. Angular integration gives

`<a id="eq:v2"></a>`{=html} $$v_2(T)=\frac{1}{4\pi^2}\int_0^{\infty}\mathrm{d}k\,k|\widetilde f(k)|^2
 |\widehat\chi_T(k+\Omega)|^2[1-\operatorname{sinc}(kd)],
\tag{12}$$

with $\operatorname{sinc}z=\sin z/z$ and $\widehat\chi_T(\nu)=T\widehat\chi(T\nu)$. The pulse must supply the frequency $k+\Omega\ge\Omega$, and a stretched Schwartz pulse has none to spare,

`<a id="eq:super"></a>`{=html} $$v_2(T)=O_N(T^{-N})\quad\text{for every }N>0,
\tag{13}$$

where the constant may depend on $N$. The same holds for $\|\psi_1(T)\|$. At fixed smearing $\|\psi_3(T)\|=O(T^3)$, so the second term of Eq. [(11)](#eq:v4state) is also negligible. The first term need not be.

At second order the detector is back in $\lvert g\rangle$, and the state has a vacuum part and a two-particle part $\lvert \zeta_T\rangle$. The Dyson expansion gives

`<a id="eq:pair"></a>`{=html} $$\lvert \zeta_T\rangle=\int\mathrm{d}^3\bm k\,\mathrm{d}^3\bm p\,
 b(k)b(p)F_T(k,p)a_{\bm k}^{\dagger}a_{\bm p}^{\dagger}\lvert g,0\rangle,
 
\tag{14}$$

with the symmetric kernel

`<a id="eq:F"></a>`{=html} $$\begin{aligned}
 F_T(k,p)={}&-\int_{-\infty}^{\infty}\mathrm{d}u\,\mathrm{e}^{\mathrm{i}(k+p)u}
 \int_0^{\infty}\mathrm{d}r\,\mathrm{e}^{-\mathrm{i}\Omega r}\\

 &\times\chi_T(u+r/2)\chi_T(u-r/2)
 \cos[(k-p)r/2].
\end{aligned}\tag{15}$$

Here $u=(t+t')/2$ is the mean time of the two vertices and $r=t-t'\ge0$ their ordered separation, during which the detector sits in its excited state and accumulates the phase $\mathrm{e}^{-\mathrm{i}\Omega r}$. Symmetrizing the two creation operators produces the cosine, and Eq. [(14)](#eq:pair) has no extra factor $1/2$.

The two vacuum contractions in $\|\zeta_T\|^2$ give a factor two, and Eq. [(7)](#eq:momentum) gives the exact two-particle contribution

`<a id="eq:pairvisibility"></a>`{=html} $$\begin{aligned}
 v_{4,\mathrm{pair}}(T)={}&\frac{1}{8\pi^4}\int_0^{\infty}\mathrm{d}k\,\mathrm{d}p\,kp
 |\widetilde f(k)\widetilde f(p)|^2|F_T(k,p)|^2\\

 &\times[1-\operatorname{sinc}(kd)\operatorname{sinc}(pd)],\end{aligned}\tag{16}$$

`<a id="eq:pairdominates"></a>`{=html} $$\begin{aligned}
 v_4(T)={}&v_{4,\mathrm{pair}}(T)+O_N(T^{-N}).
\end{aligned}\tag{17}$$

The product of sinc functions comes from averaging $\cos[(\bm k+\bm p)\cdot\bm d]$ over the two independent directions, as the total momentum dictates.

The soft-pair law {#sec:law}
-----------------

The pair amplitude at low frequency is controlled by the square of the pulse, $h(s)=\chi(s)^2$, through

`<a id="eq:K"></a>`{=html} $$\mathcal{K}[\chi]=\int_0^{\infty}\mathrm{d}q\,q^5|\widehat h(q)|^2.
\tag{18}$$

For fixed $d>0$, $\Omega>0$ and the profiles above, our main result is

`<a id="eq:main"></a>`{=html} $$\boxed{\displaystyle
 v_4(T)=\frac{d^2\mathcal{K}[\chi]}{480\pi^4\Omega^2T^4}+o(T^{-4}).}
 
\tag{19}$$

The coefficient is strictly positive, because $\widehat h(0)=\int\chi^2\,\mathrm{d}s>0$ and $\widehat h$ is continuous. It depends on the pulse shape, and on the spatial profile only through $\widetilde f(0)=1$. Equation [(19)](#eq:main) concerns the fourth-order coefficient; Sec. [5](#sec:joint) turns it into a statement about the full visibility.

To see where it comes from, measure frequencies in units of $1/T$, setting $k=a/T$ and $p=b/T$ in Eq. [(15)](#eq:F), and rescale both times. The integrand of the half-line integral over $r$ is even at its endpoint $r=0$, so one integration by parts gives, for fixed $a,b\ge0$,

`<a id="eq:softF"></a>`{=html} $$F_T(a/T,b/T)=\frac{\mathrm{i}T}{\Omega}\widehat h(a+b)
       +O\!\left(\frac{1}{\Omega^3T}\right).
\tag{20}$$

The would-be $\Omega^{-2}$ term vanishes with the first endpoint derivative. The geometric factor expands as

`<a id="eq:softgeometry"></a>`{=html} $$T^2[1-\operatorname{sinc}(ad/T)\operatorname{sinc}(bd/T)]
 \longrightarrow\frac{d^2}{6}(a^2+b^2).
\tag{21}$$

Substituting both into Eq. [(16)](#eq:pairvisibility),

`<a id="eq:limitintegral"></a>`{=html} $$\begin{aligned}
 \lim_{T\to\infty}T^4v_{4,\mathrm{pair}}(T)
 &=\frac{d^2}{48\pi^4\Omega^2}\\

 &\quad\times\int_0^{\infty}\mathrm{d}a\,\mathrm{d}b\,ab(a^2+b^2)|\widehat h(a+b)|^2,
 
\end{aligned}\tag{22}$$

with the exchange of limit and integral justified in Appendix [A](#app:bounds). With $q=a+b$ and $x=a/q$ the integral separates, and

$$\int_0^1\mathrm{d}x\,x(1-x)[x^2+(1-x)^2]=\frac{1}{10}
\tag{23}$$

gives Eq. [(19)](#eq:main).

The same kernel follows from the effective ground-state interaction

`<a id="eq:effective"></a>`{=html} $$H^{(g)}_{\mathrm{eff},X}(t)
 =-\frac{\lambda^2}{\Omega}\chi_T(t)^2:\!\Phi_{\bm x_X}(t)^2\!:\,,
 
\tag{24}$$

obtained by eliminating the virtual excitation at low frequency, up to a common vacuum phase. Quadratic couplings of this kind drive microscopic dynamical Casimir radiation \[[7](#ref-Souza2018), [8](#ref-LoLaw2018), [9](#ref-Farias2019)\], and they explain why $\widehat{\chi^2}$ rather than $\widehat\chi$ appears. We use Eq. [(24)](#eq:effective) only as intuition; Eq. [(20)](#eq:softF) derives the limit from the original Hamiltonian.

Visibility without an internal excitation {#sec:joint}
-----------------------------------------

Comparing perturbative coefficients at fixed $T$ leaves an order of limits open, since the remainder $R_6$ may grow with $T$. We therefore let both parameters move together. For any fixed pulse and profile as above, take $\lambda\to0^+$ and

`<a id="eq:jointscale"></a>`{=html} $$T(\lambda)=\Omega^{-1}\lambda^{-\beta},
 \qquad 0<\beta<\frac15.
\tag{25}$$

Then the full visibility obeys

`<a id="eq:joint"></a>`{=html} $$\boxed{\displaystyle
 1-\mathcal{V}_{T(\lambda)}\sim
 \frac{\lambda^4d^2\mathcal{K}[\chi]}{480\pi^4\Omega^2T(\lambda)^4}.}
 
\tag{26}$$

The second-order term is $\lambda^2v_2=o(\lambda^4T^{-4})$ once $N>4+2/\beta$ in Eq. [(13)](#eq:super). With $B_f$ the norm of the mode function $b$, defined in Appendix [A](#app:bounds), the Dyson bound there gives $R_6=O(\lambda^6T^6)$ when $\lambda B_fT\ll1$, which relative to the pair term is $O(\lambda^2T^{10})=O(\lambda^{2-10\beta})$. This range of $\beta$ suffices, and we have not tried to optimize it.

Let $P_e$ be the probability of finding the detector excited after the pulse. Only odd Dyson orders contribute to its amplitude, and the same bound gives

`<a id="eq:noexcitation"></a>`{=html} $$\begin{aligned}
 P_e&\leq 2\lambda^2\|\psi_1(T)\|^2+O(\lambda^6T^6),\\

 \frac{P_e}{1-\mathcal{V}_T}&\longrightarrow0
 \quad\text{along Eq.~(25)}.
\end{aligned}\tag{27}$$

The rare excitations therefore cannot account for the leading loss of path coherence.

Measuring the detector at the end isolates the pair channel. Let $\mathcal{V}_g$ be the visibility conditioned on finding $\lvert g\rangle$. The excited one-particle sector is then absent and $D_{\bm d}$ annihilates the vacuum, so at any fixed $T$

`<a id="eq:conditional4"></a>`{=html} $$1-\mathcal{V}_g=\lambda^4v_{4,\mathrm{pair}}(T)+O_T(\lambda^6),
 
\tag{28}$$

where normalizing by the ground-state probability enters only at sixth order. For the full conditional observable, split the overlap as $\mathcal{C}_T=\mathcal{C}_g+\mathcal{C}_e$ into ground and excited parts. Both branches have the same $P_e$, $|\mathcal{C}_e|\le P_e$ and $\mathcal{V}_g=|\mathcal{C}_g|/(1-P_e)$, so

`<a id="eq:conditional"></a>`{=html} $$|\mathcal{V}_g-\mathcal{V}_T|\leq\frac{2P_e}{1-P_e},
 \qquad 1-\mathcal{V}_g\sim1-\mathcal{V}_T.
\tag{29}$$

A detector found in its ground state still leaves the leading soft-pair record in the field.

Gaussian pulse {#sec:gauss}
--------------

For $\chi(s)=\mathrm{e}^{-s^2/2}$ both time integrals in Eq. [(15)](#eq:F) can be done. With the Faddeeva function $w(z)=\mathrm{e}^{-z^2}\operatorname{erfc}(-\mathrm{i}z)$, $z=\Omega T$ and $\delta=(k-p)T/2$,

`<a id="eq:gaussianF"></a>`{=html} $$F_T(k,p)=-\frac{\pi T^2}{2}\mathrm{e}^{-(k+p)^2T^2/4}
 [w(-z+\delta)+w(-z-\delta)].
\tag{30}$$

This keeps the full gap dependence and checks the soft expansion directly, for any of the spatial profiles above. Here $\widehat h(q)=\sqrt\pi\mathrm{e}^{-q^2/4}$, and

`<a id="eq:gauss4"></a>`{=html} $$\mathcal{K}[\chi]=8\pi,\qquad
 v_4(T)\sim\frac{d^2}{60\pi^3\Omega^2T^4}.
\tag{31}$$

Laplace expansion of Eq. [(12)](#eq:v2) gives, for comparison,

`<a id="eq:gauss2"></a>`{=html} $$v_2(T)\sim\frac{d^2}{32\pi\Omega^4T^6}\mathrm{e}^{-\Omega^2T^2}.
 
\tag{32}$$

The one-quantum channel is exponentially suppressed and the pair channel is not. The final pair energy $k+p$ can be arbitrarily small, because $\Omega$ is the energy of an intermediate state and places no lower bound on the energy left in the field.

For this pulse a slower growth of $T$ also works, $\Omega T=\sqrt{a\log(1/\lambda)}$ with $a>2$. Then $\|\psi_1(T)\|^2=O(T^{-2}\mathrm{e}^{-\Omega^2T^2})$, both the excitation bound and the remainder stay negligible against $\lambda^4T^{-4}$, and the conclusions of Sec. [5](#sec:joint) hold unchanged.

Interpretation and scope
------------------------

The energy of the pair is paid by the switching. Smooth switching removes high-frequency transients, but a massless field always has modes slower than the pulse, and a virtual detector transition couples them in pairs. Once the coupling is off, their branch-dependent state persists, and common free evolution afterwards leaves the overlap unchanged. An active quantum eraser could still undo it.

The loss of coherence still tends to zero in the limit [(25)](#eq:jointscale). What changes is its rate and its channel. The excitation probability can be exponentially small while the visibility loss is only algebraically small, so exponentiating the second-order response would miss the effect. A gapped quantum detector does not act like a prescribed linear source, whose radiation would be a coherent state.

The gap moves the first algebraic contribution to fourth order, where $\widehat{\chi^2}$ takes over from $\widehat\chi$, and Eq. [(19)](#eq:main) needs $\Omega T\gg1$, so the gapless limit cannot be taken in it. The field is massless, the separation and detector size are fixed, and the whole pulse is stretched as $\chi(t/T)$. Lengthening a holding time with fixed switching ramps is a different limit, and moving paths, thermal fields, charged particles in quantum electrodynamics and fixed-coupling adiabatic theorems are outside the present analysis. The dependence on $\widetilde f(0)$ alone does not license removing the spatial regulator from higher-order vacuum terms.

In operational terms, a final internal measurement can find the detector in its ground state while the field carries the leading path record. Equations [(19)](#eq:main), [(26)](#eq:joint) and [(29)](#eq:conditional) quantify how much.

Bounds and limits {#app:bounds}
-----------------

### Soft-frequency limit under the integral

Define

$$A(q,r)=\int\mathrm{d}s\,\mathrm{e}^{\mathrm{i}qs}\chi(s+r/2)\chi(s-r/2).
\tag{33}$$

It is a Schwartz function of $(q,r)$ and is even in $r$. Writing $M=\Omega T$, $q=a+b$, and $\delta_0=(a-b)/2$, Eq. [(15)](#eq:F) becomes

`<a id="eq:rescaledF"></a>`{=html} $$F_T(a/T,b/T)=-T^2\int_0^{\infty}\mathrm{d}r\,
 \mathrm{e}^{-\mathrm{i}Mr}A(q,r)\cos(\delta_0r).
\tag{34}$$

For fixed $a,b$, endpoint integration by parts gives Eq. [(20)](#eq:softF), since $A(q,0)=\widehat h(q)$ and $\partial_r A(q,0)=0$.

Uniform control follows by splitting at $q=M$. For $q\leq M$, the two phases have frequencies $M\pm\delta_0\geq M/2$. Integration by parts and the Schwartz bounds on $A$ imply

$$\left|\frac{\Omega}{T}F_T(a/T,b/T)\right|
 \leq C_N(1+q)^{-N}.
\tag{35}$$

For $q>M$, direct integration gives the bound $C_NM(1+q)^{-N}$. Also,

$$0\leq T^2[1-\operatorname{sinc}(ad/T)\operatorname{sinc}(bd/T)]
 \leq\frac{d^2}{6}(a^2+b^2).
\tag{36}$$

One way to see the last inequality is to average $1-\cos[(a\bm n+b\bm m)\cdot\bm d/T]\leq[(a\bm n+b\bm m)\cdot\bm d/T]^2/2$ over independent unit vectors. Since $\widetilde f$ is bounded, the rescaled integrand is dominated on $q\leq M$ by an integrable function. The $q>M$ tail is bounded by a constant times $M^2\int_M^{\infty}\mathrm{d}q\,q^5(1+q)^{-2N}$ and vanishes for sufficiently large $N$. This proves Eq. [(22)](#eq:limitintegral) without an unregulated exchange of limits.

### Higher-order remainder

Let

$$B_f^2=\int\mathrm{d}^3\bm k\,|b(k)|^2<\infty,
 \qquad z=2|\lambda|B_fT\|\chi\|_1.
\tag{37}$$

After $n$ interaction vertices, at most $n$ field quanta are present. The creation and annihilation bounds on each particle sector, followed by the ordered time integrals, give

`<a id="eq:dysonbound"></a>`{=html} $$\|\lambda^n\psi_n(T)\|\leq\frac{z^n}{\sqrt{n!}}.
\tag{38}$$

The detector monopole has operator norm one. As $D_{\bm d}$ is bounded by two and only even total orders survive, the terms of total order at least six in Eq. [(7)](#eq:momentum) are $O(z^6)$ as $z\to0$. This also keeps $\mathcal{C}_T$ positive in the regime used in Eq. [(26)](#eq:joint).

Equation [(38)](#eq:dysonbound) gives $\|\psi_3\|=O(T^3)$. The first-order norm decreases faster than every inverse power by the same Fourier bound as Eq. [(13)](#eq:super). Cauchy-Schwarz then proves Eq. [(17)](#eq:pairdominates). Along Eq. [(25)](#eq:jointscale), $z=O(\lambda^{1-\beta})\to0$ and $\lambda^6T^6=o(\lambda^4T^{-4})$. For the excited sector, the sum of odd orders starting at three has norm $O(z^3)$. Applying $\|u+v\|^2\leq2\|u\|^2+2\|v\|^2$ proves Eq. [(27)](#eq:noexcitation).

AI assistance {#ai-assistance .unnumbered}
-------------

AI tools assisted with writing, mathematical derivations, literature review, and numerical code. Some claims in this working paper remain to be independently checked.

References {#references .unnumbered}
----------

1.  `<a id="ref-Foo2020"></a>`{=html} Joshua Foo, Sho Onoe, and Magdalena Zych. Unruh--deWitt detectors in quantum superpositions of trajectories. *Phys. Rev. D*, 102(8):085013, 2020.

2.  `<a id="ref-Gooding2026"></a>`{=html} Cisco Gooding, Taylor Cey, and Robert Mann. Testing superpositions of detector trajectories, 2026.

3.  `<a id="ref-Unruh2000"></a>`{=html} William G. Unruh. False loss of coherence. In Heinz-Peter Breuer and Francesco Petruccione, editors, *Relativistic Quantum Measurement and Decoherence*, volume 559 of *Lecture Notes in Physics*, pages 125--140. Springer, Berlin, Heidelberg, 2000.

4.  `<a id="ref-GundhiBassi2023"></a>`{=html} Anirudh Gundhi and Angelo Bassi. Motion of an electron through vacuum fluctuations. *Phys. Rev. A*, 107(6):062801, 2023.

5.  `<a id="ref-Gundhi2024"></a>`{=html} Anirudh Gundhi. Decoherence due to the Casimir effect? *Phys. Rev. D*, 110(11):116001, 2024.

6.  `<a id="ref-GundhiUlbricht2025"></a>`{=html} Anirudh Gundhi and Hendrik Ulbricht. Measuring decoherence due to quantum vacuum fluctuations. *Phys. Rev. Lett.*, 135(2):020402, 2025.

7.  `<a id="ref-Souza2018"></a>`{=html} Reinaldo de Melo e Souza, François Impens, and Paulo A. Maia Neto. Microscopic dynamical Casimir effect. *Phys. Rev. A*, 97(3):032514, 2018.

8.  `<a id="ref-LoLaw2018"></a>`{=html} Lezhi Lo and C. K. Law. Quantum radiation from a shaken two-level atom in vacuum. *Phys. Rev. A*, 98(6):063807, 2018.

9.  `<a id="ref-Farias2019"></a>`{=html} M. Belén Farías, C. D. Fosco, Fernando C. Lombardo, and Francisco D. Mazzitelli. Motion induced radiation and quantum friction for a moving atom. *Phys. Rev. D*, 100(3):036013, 2019.

10. `<a id="ref-Dalvit2000"></a>`{=html} Diego A. R. Dalvit and Paulo A. Maia Neto. Decoherence via the dynamical Casimir effect. *Phys. Rev. Lett.*, 84(5):798--801, 2000.

11. `<a id="ref-Sinha2021"></a>`{=html} Kanupriya Sinha, Adrián Ezequiel Rubio López, and Yiğit Subaşı. Dissipative dynamics of a particle coupled to a field via internal degrees of freedom. *Phys. Rev. D*, 103(5):056023, 2021.

12. `<a id="ref-Jakubec2026"></a>`{=html} Clemens Jakubec, Aaron Bartleson, Peter W. Milonni, and Kanu Sinha. Decoherence of spatial superpositions along stationary worldlines, 2026.

13. `<a id="ref-Hummer2016"></a>`{=html} Daniel Hümmer, Eduardo Martín-Martínez, and Achim Kempf. Renormalized Unruh--DeWitt particle detector models for boson and fermion fields. *Phys. Rev. D*, 93(2):024019, 2016.
