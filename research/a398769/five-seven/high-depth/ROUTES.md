# Attempted routes and their first unproved steps

**Outcome: no closing advance.** This investigation did not prove the
all-length `{5,7}` exclusion, find a full witness, or obtain a global
effective valuation bound. The order-stabilization lemma in
[PROOF.md](PROOF.md) is a new elementary diagnostic refinement. It removes
no remaining pair from the all-length problem by itself. It must not be
advertised as control of the long zero-lift run.

## Single high-depth position

The candidate `r_K(L)`, with `K` the first depth for which
`6*7^(K-1)>L`, is well-defined for every length and is the only possible
actual position of a full witness. This was independently reconstructed,
including `K<=L-2`, the lift formula, the factor nine, and rejection of the
whole length when this position is absent or fails `9S | F`.

The research question was whether **passing the full digit sum** forces a
nonzero lift before the witness threshold. The new arithmetic input is

```
v_7(ord_(7L-4)(10)) <= K(L)-1.
```

It follows from `S=3 mod7`, oddness, and the prime factor that carries
the largest seven-power in the order. Thus the gcd governing the
unrestricted full-sum/seven-power exponent CRT has already stabilized at
K. Once r_K passes the full digit sum, this unrestricted CRT remains
compatible at every later depth. It cannot provide a later incompatible
level to force escape. This is a proved statement about a particular
proposed mechanism, not a theorem that the digit-sum condition cannot
help through another argument.

The first unproved step is still to bound

```
v_7(F(L,r_K(L))) <= L-3
```

uniformly over all remaining lengths whose r_K is actual and passes
`9S | F`. The exact candidate and zero-run criterion restate this
obligation. The new lemma explains why a further gcd-compatibility test
alone does not discharge it.

The bounded experiment in [README.md](README.md) tests this formulation
inside the inherited finite interval. It is not an arbitrary extension
of the search and is not an effective cutoff. The absence of full-sum
starting candidates in that finite experiment gives no empirical test of
a zero-run bound *on surviving full-sum candidates*. An arithmetic
positive control with several zero lifts fails the full digit sum and is
labelled accordingly.

## Effective valuation bound

The exact full-sum factor improves the elementary size bound only to

```
7^v <= F/(225S) < 7*10^L/(225S).
```

This gives leading coefficient `log(10)/log(7)>1`, so does not exclude
`v>=L-2` uniformly. No rounding or endpoint adjustment changes that
coefficient.

The inherited two-logarithm applications are audited in
[the edge proof](../settlement/EDGE_BOUNDS.md),
[the midpoint proof](../effective/ROUTE_A.md), and
[the proportional proof](../proportional/AUDIT.md). They expose the
heights contributed by i, L-i, or a varying rational-centre offset.
The proposed new ingredient here would have been that the exact full-sum
condition reduces those heights or forces the position into one of their
controlled regions. The order-stabilization lemma supplies no such
restriction. Treating `(7*10^L-25)/18`, `(18*10^i+25)/7`, or an exact
quotient as a fixed-height logarithm base would hide dependence on the
varying pair.

No external theorem is newly applied in this note; those earlier
applications and their primary-source/hypothesis records are reused with
unchanged scope. The known uniform qualitative `v_7(F)=o(L)` remains
[ineffective in its starting length](../effective/QUALITATIVE.md).
Neither a finite exceptional-set count nor a finite number of exceptional
subspaces provides the missing largest exceptional height. No constants
`c<1,C,L0` or numerical cutoff B have been obtained, so there is no new
finite interval `(10,000,000,B)` claimed to have been discharged.

## Exact quotient candidates

Retain

```
A=9*7^(L-2)*S, H=25A, X=7*10^L/H,
m=(L+1)/2, J=10^m/25,
q_1=floor(X), q_2=(-A^(-1) mod J).
```

The notation J avoids confusing this inverse modulus with the depth K.
The [two-quotient reduction](../global/TWO_QUOTIENTS.md) and
[adjustable split](../effective/ROUTE_B.md) already retain the full
varying sum. They are not missing a factor that the new representative
criterion restores. The equivalent high-depth position can be checked
against either exact candidate, but uniqueness of each does not reject
its value.

The first missing statement in the low branch is a uniform exclusion of

```
7*10^L-H*q_1 = 18*10^i+25
```

at its recovered actual position. The first missing statement in the
high branch is a proof that the small inverse representative fails the
size check, its required 2- and 5-adic valuations, or the full equality.
The available bound `q<X=343*(10/7)^L/(225S)` permits cofactor height
proportional to L; it does not prove an actual lower bound for that height.
Factoring out S improves this upper estimate by order log L, not by an
established uniform sufficient saving.

The [fixed-modulus obstruction](../global/FIXED_MODULUS.md) concerns an
existential modular quotient and remains valid. It is not an impossibility
result for every argument about these two particular exact quotients.
No new arithmetic property uniformly rejecting either exact value was
obtained, so unchanged quotient computations were not repeatedly rerun.

## Rational centres and coverage

The inherited [coverage obstruction](../proportional/COVERAGE.md) defeats
the stated uniform degree-and-height envelope: the degree cost and the
coefficient-span height prevent density of rational centres from giving
a cover. The explicit rounded family used there is only a survivor of
named filters, not a full-sum family or witness.

A useful improvement would require a smaller actual algebraic degree,
a sharper root height, a different estimate, or a new full-sum restriction
that covers the omitted family and all other omitted pairs. The present
order bound does none of those things. Accordingly this route was not
pursued by adding more fixed centres or by treating the gap interval
`(41/100,42/100)` as the only remaining domain. All six residual ratio
intervals, and all relevant discrete restrictions, remain in the
self-contained baseline in [README.md](README.md).

## Status of the obligation

Each length is decidable by an exact finite procedure, but no uniform
rejection, effective global cutoff, or complete finite exception list
has been proved. The already established infinite exact-maximum-depth
families choose their depth first and then let lengths grow. They cannot
be substituted at the diagonal depth `L-2`, and they rule out a uniform
absolute constant bound on all maxima.

The consecutive certificate remains lengths **1 through 10,000,000
inclusive**. The earlier isolated length, the two PR #14 appendix lengths,
and the infinite fixed-depth whole-length families retain their separate
coverage. No new Lean theorem or Lean build is claimed. The `{5,7}`
subclass and the wider A398769 digit-1 conjecture remain unresolved.
