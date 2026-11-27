# Fixed-position index lifting and the remaining ternary obstruction

**Verdict.** The proposed difference identity, permutation statement and
depth-three control are valid. They supply an exact single residue class
at every fixed position and depth. They do not force the actual ternary
position to miss that class. The first missing implication is still a
uniform mismatch by depth `L-2` for each actual candidate remaining after
the common-factor theorem. No effective cutoff is obtained here.

## 1. Depth two, retaining the length division by seven

Write `a_u=31+6u`, `L_u=(3^a_u+4)/7`. Every `L_u=1 mod6`, so

```
F(L_u,s)=21-18*10^s-25 mod49.
```

Ten has order 42 modulo 49: its order modulo seven is six, and
`v7(10^6-1)=1`. Solving the displayed equation gives `10^s=27 mod49`,
whose unique exponent class is `s=39 mod42`. Thus, for all nonnegative s,

```
49 | F(L_u,s)  iff  s=39 mod42.                       (1)
```

Now fix any such s. For distinct indices, assume `u>v` without loss of
generality and put `h=u-v`. The exact identity is

```
L_u-L_v = 3^31*729^v*(729^h-1)/7.
```

Since `729-1=728=7*104`, LTE gives

```
v7(729^h-1)=1+v7(h),
v7(L_u-L_v)=v7(h).                                   (2)
```

**The division by seven removes one valuation.** The length difference
is divisible by six, as both lengths are one modulo six. Applying LTE
to `10^6`, and then retaining the coefficient seven in F, gives

```
F(L_u,s)-F(L_v,s)=7*10^L_v*(10^(L_u-L_v)-1),
v7(F(L_u,s)-F(L_v,s))=2+v7(u-v).                      (3)
```

The cancellation makes (3) independent of s; condition (1) is needed
only to divide each individual F by 49 integrally.

## 2. A permutation at every depth, with an explicit digit lift

Set `H_s(u)=F(L_u,s)/49`. Equation (3) says exactly

```
v7(H_s(u)-H_s(v))=v7(u-v).
```

It proves both well-definedness and injectivity on classes modulo `7^j`.
There are `7^j` classes on either side, so the map is a permutation. In
particular, for each `m>=2` exactly one class

```
r_m(s) mod7^(m-2)
```

satisfies `7^m | F(L_u,s)`. The classes are compatible as m increases.
This is an exact result on all nonnegative integer indices, not a density
heuristic or a statement limited to enumerated indices.

There is a particularly simple digit formula. Set `r_2=0`, `R=7^(m-2)`.
For `0<=c<=6`, binomial expansion or LTE at the next digit gives

```
[L_(r+cR)-L_r]/(6R)=3c mod7,
[F(L_(r+cR),s)-F(L_r,s)]/7^m=2c mod7.                (4)
```

For clarity, `3^31=3 mod7`, `729=1 mod7`, and
`(729-1)/7=104`; thus the first coefficient is
`3*104/6=3 mod7`. Also `(10^6-1)/7=1 mod7` and
`10^L_r=3 mod7`, giving the second coefficient `3*3=2 mod7`.
The divisions in (4) are exact integer divisions before reduction.

If `r=r_m` and `z_m=F(L_r,s)/7^m mod7`, the unique next digit is

```
c_m=-4*z_m mod7,
r_(m+1)=r_m+c_m*7^(m-2),                             (5)
```

because four is the inverse of two modulo seven. The implementation
checks (5) against all seven children, not merely the selected child.

For a direct depth-three derivation, `L_0=7 mod42` and
`L_(u+1)-L_u=18 mod42`. Hence

```
7*10^L_u-25=192+98u mod343.
```

Writing `s=39+42h`, use `10^39=223 mod343` and `10^42=50=1+49 mod343`:

```
F(L_u,s)=49*(-1+2u-3h) mod343.
```

It vanishes exactly when `h=2+3u mod7`, or

```
343 | F(L_u,s)  iff  s=123+126u mod294.               (6)
```

## 3. Substitute the actual ternary position

The inherited constant is
`kappa=log(C)/log(10)`, `C=(7theta-25)/18`,
`theta^7=10^4`, `theta in 1+9 Z_3`. Let `d=3^(a-2)` and let s be
the unique odd representative of kappa modulo d in `[0,2d)`.
An actual candidate still requires `3<=s<L` and **9S|F at this s**.
The common-factor result removes `q^4<=L`, where
`g=gcd(L,s)`, `p=s/g`, `q=L/g`. It does not say the other candidates
have large seven-adic valuation; most finite controls already fail at
depth two.

Since `qs=pL` and `7L=9d+4`, one obtains exactly

```
7q*kappa=4p mod d.                                   (7)
```

Here `3` does not divide L or q, so this is a three-adic approximation
to the *fixed* kappa by `4p/(7q)`. It does not provide an upper bound on q.
For example, the inherited explicit logarithm estimate can be applied
to the fixed independent bases `10,C`, now with positive exponents
`4p,7q`. The global degree is seven, local field is Q_3, and height
parameters are `log A1=3`, `log A2=4`, as verified in
[the inherited individual analysis](../power-three/INDIVIDUAL.md#5-an-effective-logarithm-estimate-at-three-and-its-direction).
Because an actual position has `0<p<q`,

```
b'=(4p)/(7*4)+(7q)/(7*3)=p/7+q/3<q,
v3(C^(7q)-10^(4p))=2+v3(7q*kappa-4p)>=a.
```

Nonvanishing follows from the same multiplicative independence. The
same explicit coefficient then yields only

```
a < 1037232*max(log(q)+1,10)^2.                       (8)
```

This is a **lower size constraint on q**, consistent with arbitrarily
large q. It is especially unhelpful after `q^4>L`, which already forces
exponential growth of q in a. Neither (7) nor (8) imposes a seven-adic
condition on `r_m(s)`. Promoting (8) into an upper bound on q or a would
reverse its direction.

For a full witness, the precise remaining condition is

```
u = r_(L-2)(s_a) mod7^(L-4).                         (9)
```

The modulus is indeed much greater than `u=(a-31)/6`. Therefore, with
the least nonnegative representative, (9) says simply
`r_(L-2)(s_a)=u`. A permutation has a preimage for zero; it can be this
small u. Neither the uniqueness of that preimage nor the size of its
modulus rules out equality. The required missing estimate would prove
some `r_m(s_a) != u mod7^(m-2)` with `m<=L-2`, for every remaining actual
candidate. A mismatch first occurring at depth `L-1` is too late:
valuation exactly `L-2` already qualifies as a full witness after the
other factors pass.

The ternary representative changes with u, so the fixed-s permutation
theorem cannot be reapplied as a statement that `u -> H_(s_a)(u)` is
itself a permutation. Its proof uses cancellation of *the same* `10^s`
in (3); moving s removes that cancellation. No bound controlling this
additional term at the growing threshold has been proved here. The
pair theorem remains compatible with an isolated full witness whose
neighbours fail. The inherited ineffective qualitative finiteness
statement supplies neither an explicit last exponent nor the finite
verification needed to close this gap.

## 4. Exact finite checks and nonzero positive controls

[`index_lift.py`](index_lift.py) imports no research arithmetic. To
evaluate F modulo `7^m` it computes `3^(31+6u)` modulo
`7*(6*7^(m-2))` **before** dividing the numerator by seven. This retains
the exponent precision needed by the coefficient `7*10^L`. Direct
exponentiation constructs the exact L for the finite controls and is a
separate comparison path.

For ternary controls it finds theta by a modular inverse exponent,
forms C with the required two ternary digits of division, and recovers
the discrete logarithm by testing all three digits at every step. It
imports neither the inherited Newton/log implementation nor the new
original-decimal implementation. It checks `9S|F` and (7) on the exact
reconstructed s. The resulting exact L, s, g, p and q are retained in
[`index_lift.json`](index_lift.json).

The deterministic receipt records:

- 14,406 direct depth-two/depth-three iff controls: all `0<=u<49` and
  `0<=s<294`.
- 4,200 reduced-versus-direct exponentiation comparisons through depth
  eight, and 4,950 distinct-index exact-valuation checks.
- All classes for 21 permutations: seven s values at each of
  `j=1,2,3`, with digit roots compared against full direct enumeration.
- All seven children at every lift through depth ten for fixed positions
  39, 123 and 291; the controls include surviving classes, not only misses.
- Independently recovered ternary controls at a=97, 1231, 1573 and 1579.

In particular, **a=1231, u=200 is an actual candidate with g=1**:
`r_3=4 mod7`, `r_4=4 mod49`, and `r_5=249 mod343`. Thus this actual
small u survives through depth four, then misses at depth five because
`200 !=249 mod343`. Direct F residues are zero through `7^4` and
`12005 mod7^5`. The original-word value is checked independently in the
individual certificates. This is a positive control for the surviving
side of the index test, not a full witness.

At a=1573 the joint representative is a **class miss**, although
`s=123 mod126`; its algebraic index test would also miss at depth three
(`u=257=5 mod7`, `r_3=2`). It is not evaluated as an actual decimal word.
At a=1579 the representative is actual but `s=3 mod42`, so it fails
before the fixed-s permutation applies: `F=28 mod49`, equivalently
`n=14 mod49`. These are finite exclusions, not a universal moving-position
bound.

From the repository root, both modes reproduce the retained receipt:

```sh
pt=research/a398769/five-seven/power-three-individual
PYTHONDONTWRITEBYTECODE=1 python3 "$pt/index_lift.py" > /tmp/index-lift.json
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pt/index_lift.py" > /tmp/index-lift-O.json
cmp /tmp/index-lift.json /tmp/index-lift-O.json
cmp /tmp/index-lift.json "$pt/index_lift.json"
```

All checks use explicit exceptions and remain active under `python3 -O`.
The receipt binds the exact source SHA-256. No new Lean verification is
claimed, and this work extends no consecutive whole-length interval.
