---
title: No Private Randomness in Empty de Sitter Space?
description: A working note on modular guessing and private randomness in de Sitter space.
date: 2026-11-25
permalink: /notes/empty-de-sitter-private-randomness/
math: true
---

<header class="article-header">
  <h1>No Private Randomness in Empty de Sitter Space?</h1>
  <p class="byline">
    <strong>Javier Blanco-Romero</strong><br>
    Researcher at Universidad Carlos III de Madrid<br>
    <time datetime="2026-11-25">25 November 2026</time>
  </p>
</header>

*What follows is mostly irrelevant for practical cryptography*, but I think it is interesting nonetheless if we are curious about "how fundamental" concepts like "privacy" may be in quantum field theory and quantum gravity.

A quantum random number generator (QRNG) that observes/measures the vacuum in a bounded region cannot signal a spacelike separated observer, and, at the same time, that external observer cannot influence said bit. However, if we take into account that the vacuum is entangled across regions, it turns out that the spacelike observer can still try to guess the outcome. In my ["spacelike guessing"](https://fj-blanco.github.io/research/spacelike-quantum-randomness/) draft, I have been exploring (with the help of Fable 5.2 and GPT-6 Astra) how well an eavesdropper confined to the causal complement $\mathcal{M}'$ of a source algebra $\mathcal{M}$ (where the QRNG lives) can predict a fair bit produced by a binary measurement $E_\pm = \frac{1}{2}(\mathbf{1} \pm Z)$. Using Tomita–Takesaki theory we can show that the mirror observable $JZJ \in \mathcal{M}'$ guesses the outcome with probability

$$P_{\text{mirror}} = \frac{1 + C_Z}{2}, \qquad C_Z = \Vert{}\Delta^{1/4} Z \Omega\Vert{}^2,$$

where $\Delta$ is the modular operator of the source algebra $\mathcal{M}$ and $\Omega$ is the vacuum vector as usual, so no measurement anywhere in $\mathcal{M}'$ can do better than $\frac{1}{2}(1 + \sqrt{C_Z})$.

In flat-space quantum field theory, the local algebra $\mathcal{M}$ is a Type $\mathrm{III}_1$ algebra and the modular operator $\Delta = e^{-K}$ is non-trivial (for example, for a Rindler wedge $K$ is $2\pi$ times the boost generator). It seems that this non-trivial modular spectrum is precisely what makes privacy possible, because the components of $Z\Omega$ with large positive modular energy are suppressed by $\Delta^{1/4}$, keeping $C_Z$ small. There are further ways of suppressing $C_Z$ (and hiding the bit), like moving the source away from the wedge edge or perhaps choosing a better readout function.

But in a universe with gravity and a positive cosmological constant this is no longer true. Here an observer only has causal access to a de Sitter static patch bounded by a cosmological horizon. In the Chandrasekaran–Longo–Penington–Witten framework ([arXiv:2206.10780](https://arxiv.org/abs/2206.10780)), "switching on" perturbative gravity is equivalent to dressing local observables to a physical clock carried by the observer (this is like an algebraic version of the Page–Wootters idea). This is done by adjoining such a clock using the crossed product with the modular flow (and additionally imposing that the clock's energy is bounded below), which implies that we now have a Type $\mathrm{II}_1$ algebra instead of a Type $\mathrm{III}_1$! One interesting difference is that, unlike Type $\mathrm{III}$ algebras, Type $\mathrm{II}_1$ algebras admit a finite trace and a unique maximum-entropy state $\tau$, which corresponds to empty de Sitter space.

What makes this state $\tau$ special is that it is *tracial* (this means that $\tau(AB) = \tau(BA)$ for any two observables $A$ and $B$, like in the normalized trace of a matrix, where the order of operators doesn't matter). Thanks to this symmetry the modular operator collapses to the identity, $\Delta = \mathbf{1}$ (so $K = 0$). Plugging this directly into the modular overlap formula we derived, the modular suppression vanishes, and we get

$$C_Z = \Vert{}\Delta^{1/4} Z \Omega\Vert{}^2 = \Vert{}Z \Omega\Vert{}^2 = q.$$

where $q = \langle \Omega, Z^2 \Omega \rangle \in [0, 1]$ is the second moment of $Z$ (which measures how much of the randomness actually comes from the field).

In a sharp measurement ($Z^2 = \mathbf{1}$, in which all the randomness comes from the field rather than from an "internal coin"), we have $q = 1$, which immediately gives $C_Z = 1$ and $P_{\text{mirror}} = 1$. So **in the maximum-entropy state of de Sitter space, every sharp fair measurement is perfectly correlated with its mirror observable behind the cosmological horizon!** No choice of smearing profile or readout function can lower $C_Z$ ($\Delta$ has no spectrum left to exploit). Getting $q < 1$ requires mixing in an unsharp measurement or an independent "internal coin" (moving the randomness out of the field).

In some way I think this is simply the "infinite-dimensional version" of measuring one half of a maximally entangled finite-dimensional state. But still the physical consequence is quite interesting.

In non-gravitational QFT (because this applies to QFT in external curved spacetime as well), spacelike separation and the vacuum are enough to extract private randomness, but when gravity enters the picture and you consider a static patch gravitating in a de Sitter space, causality alone is no longer enough to engineer privacy out of the field. At the equilibrium state ($\Delta = \mathbf{1}$) unconditional privacy from field measurements disappears. To get $C_Z < 1$ from a sharp measurement, the state $\rho$ has to sit away from the equilibrium $\tau$, which means "paying a nonzero entropy debt" $D(\rho \Vert{} \tau) = S_{\max} - S(\rho) > 0$ (this is the relative entropy between $\rho$ and $\tau$, which simply measures how far $\rho$ sits below the maximum entropy $S_{\max}$). **Just as thermal equilibrium leaves you with no free energy to do work, gravitational equilibrium in de Sitter space leaves you with no way to generate a secret from the field**.

This is just a quick sketch and there may be a lot of subtleties worth considering, but I think this opens an interesting question: is there any kind of "Second Law" for privacy?