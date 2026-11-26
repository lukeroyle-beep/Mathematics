# Prime digit sums: exact half and two-thirds exclusions

These are whole-length exclusion theorems for the **prime digit-sum
subclass**, not an all-length theorem for `{5,7}`. The algebra and
finite-field controls below were derived independently before comparing
with the recovered Space archive. Ordinary proofs are supplied; no Lean
formalization is claimed.

## 1. Necessary polynomials

Use the already reduced domain

```
L odd, L>=5, 3<=i<L,
S=7L-4, F=7*10^L-18*10^i-25.
```

A full witness needs `9S|F` and `v7(F)>=L-2`, with `5` not dividing S.
Modulo seven the second condition implies `10^i=-1`, so `i=3 mod6`.
Now suppose `p=S` is prime. Thus `p=3 mod7` and `p>=31`.
Since `7L=p+4=(p-1)+5`, Fermat gives

```
(10^L)^7 = 10^(p+4) = 10^5 mod p.                 (1)
```

The exponent seven is coprime to `p-1`, so there is exactly one
`y in F_p` with `y^7=10^5`; necessarily `y=10^L`.
Put `X=10^((i-1)/2)`. The necessary congruence `p|F` yields
`7y=180X^2+25`, hence

```
H(X)=(180X^2+25)^7-7^7*10^5 = 0 mod p.            (2)
```

There is a stronger condition. Write `i=6m+3`; then

```
B=(7y-25)/18000 = (10^m)^6 mod p.                 (3)
```

All divisions here are in F_p. Thus absence of a square root of
`A=(7y-25)/180`, or absence of a sixth root of B, excludes **every**
position at that length. Because `A=100B`, the sixth-power test includes
the square test. Passing either test is only necessary: the root must
still be a power of ten with the correct actual exponent, the full
factor nine must pass, and the growing seven-power must pass.

## 2. Splitting fields, good primes, and conjugation

Let `alpha=10^(5/7)` be the positive real root, `zeta=zeta_7`,
`Y_j=alpha*zeta^j` for `j in F_7`, and

```
E=Q(alpha,zeta),  A_j=(7Y_j-25)/180,
B_j=(7Y_j-25)/18000,  D=7^7*10^5-25^7=76250784375.
```

The field Q(alpha) has degree seven: if `theta=10^(1/7)`, then
`alpha=theta^5` and `theta=alpha^3/100`, and `x^7-10` is Eisenstein at
2. Over Q(zeta), a valuation above 2 gives `v(10^5)=5`, whereas
seventh powers have valuation divisible by seven (2 is unramified in
the cyclotomic field). Therefore `10^5` is not a seventh power there.
As Q(zeta) contains the seventh roots of unity, the binomial splits
after adjoining any one root and has degree seven. Consequently

```
Gal(E/Q) = { j -> a*j+b : a in F_7^*, b in F_7 },
|Gal(E/Q)|=42.                                    (4)
```

One can also obtain the degree from the coprime degrees seven and six
and the explicit conjugates. For a prime `p=3 mod7`, Frobenius has
`a=3`. All seven maps `g_b:j->3j+b` are conjugate: conjugation by the
translation `j->j+c` replaces b by `b-2c`. Each has one fixed index
`j=-b/2`; on the other six indices it is a six-cycle, since 3 has
order six in `F_7^*`.

Here is a sufficient uniform good-reduction condition:

```
p does not divide 2*3*5*7*D.                       (5)
```

The splitting field E is unramified outside 2,5,7, as follows from the
discriminant of `x^7-10^5`. Moreover
`product_j(7Y_j-25)=D`. At a prime satisfying (5), every `A_j` and
`B_j` is a local unit and all denominators are units. Adjoining their
square or sixth roots is unramified there: `x^d-u` has invertible
derivative at every root when `d=2,6` and u is a unit; its root algebra
is finite etale over the local unramified ring. Adjoining roots of
unity of order six adds no ramification outside 2,3. The corresponding
polynomials (2) and `(18000 Z^6+25)^7-7^7*10^5` are separable modulo
these primes: a repeated root would force either p to divide a listed
coefficient, `Y_j=0`, or `7Y_j-25=0`, all excluded by (5).

Thus the usual Frobenius/root correspondence applies at every control
prime used below. Finite exceptions do not affect any stated density.
No assertion that the excluded set (5) is the minimal bad set is needed.

## 3. The half-density theorem

Let `M_2=E(sqrt(A_0),...,sqrt(A_6))`, a finite Galois extension of Q,
and `N_2=Gal(M_2/E)`. For an element g of (4) with multiplier three,
let j be its unique fixed index. Any lift sigma of g to M_2 acts on
the two square roots above `Y_j` either identically or by swapping
them. No root above any other `Y_k` can be fixed. Thus H has a root
modulo a good prime of this type exactly when sigma has positive sign
on that fixed fiber.

It remains to prove the signs are balanced, rather than assume this.
Direct exhaustive arithmetic gives:

| p | unique y | A | `A^((p-1)/2)` | roots of H |
| ---: | ---: | ---: | ---: | --- |
| 31 | 25 | 6 | 30=-1 | none |
| 59 | 32 | 27 | 1 | 26,33 |

For these primes `D mod p` is respectively 24 and 50, so both are good.
Choose Frobenius elements sigma_31 and sigma_59 in `Gal(M_2/Q)`.
Their restrictions to E are conjugate by (4). Lift a conjugator from
E to M_2 and conjugate one Frobenius element, so the two restrictions
are **equal**, say g. Conjugation preserves whether the two roots of
the unique fixed fiber are fixed or swapped. The ratio of these two
aligned elements lies in N_2 and swaps that fiber.

Therefore the homomorphism

```
N_2 -> {+1,-1},  tau -> tau(sqrt(A_j))/sqrt(A_j)
```

is surjective. Its fibers have equal cardinality. Multiplying any lift
of g by N_2 consequently makes its sign positive or negative equally
often. The same is true for every conjugate g (and all seven such g
are conjugate). The event of fixing a root is conjugacy invariant in
the full group.

Apply the natural-density version of Chebotarev to these conjugacy
invariant sets. For example, see J. S. Milne, *Algebraic Number Theory*,
[Definition 8.30 and Theorem 8.31](https://www.jmilne.org/math/CourseNotes/ANT.pdf),
printed page 147. Over Q it gives a union of conjugacy classes natural
density equal to its proportion of group elements. Exactly half of
the preimage of `a=3` has no fixed root. Hence

```
lim_(x->infinity)
 #{p<=x : p prime, p=3 mod7, H has no root modp}
 / #{p<=x : p prime, p=3 mod7} = 1/2.             (6)
```

The denominator prime set has density `1/6` among all primes, so the
absolute prime density of this exclusion set is `1/12`. Each such
prime p>=31 excludes the whole length `(p+4)/7`.

## 4. The two-thirds theorem and its denominator

Put `E_6=E(zeta_6)` and
`M_6=E_6(B_0^(1/6),...,B_6^(1/6))`. Both are finite Galois over Q.
The intersection `E intersect Q(zeta_6)` is Q: the latter is the
quadratic field Q(sqrt(-3)), ramified at 3, while E is unramified at 3.
Thus

```
Gal(E_6/Q)=Gal(E/Q) x {+1,-1},                    (7)
```

where the second component epsilon acts on sixth roots of unity by
`zeta_6 -> zeta_6^epsilon`. It is +1 for `p=1 mod3` and -1 for
`p=2 mod3`. These two base classes above `a=3` have equal size seven.

Let `N_6=Gal(M_6/E_6)`, choose `beta_j^6=B_j`, and fix an index j.
We first prove that the kernel character

```
chi_j:N_6 -> mu_6,  tau -> tau(beta_j)/beta_j       (8)
```

is surjective. Use the two good primes below, both `3 mod7` and
`1 mod3`:

| p | y | B | `B^((p-1)/6)` | order of this character |
| ---: | ---: | ---: | ---: | ---: |
| 199 | 169 | 119 | 107 | 6 |
| 283 | 63 | 158 | 1 | 1 |

At a prime above p with `p=1 mod6`, the multiplier on beta_j
reduces to `beta_j^(p-1)=B_j^((p-1)/6)`. Reduction is injective on
mu_6 at these good primes, so the finite-field character determines
its exact order in characteristic zero. The corresponding `D mod p`
values are 145 and 175. For 199, the squares and cubes of 107 are 106 and 198=-1, respectively, and
`107^6=1`; its order is six. For 283 the sixth-power character is one.
Their Frobenius restrictions to E_6 are conjugate: the affine pieces
are conjugate by translations and both act trivially on `zeta_6`.
Lift the conjugator to M_6 and align the restrictions to the same g.
Both now preserve the unique fixed fiber and its sixth roots of unity.
One acts on this fiber by a primitive sixth root, the other by 1.
Conjugation may invert the primitive sixth root, which preserves order
six; it cannot change an identity fiber action. Their ratio is in N_6
and has primitive value under (8). Thus (8) is onto for that fixed
index. Conjugating by translations proves the same for every index.

In particular this kernel-surjectivity statement holds also when
considering base elements with epsilon=-1; it is a property of N_6
and the fiber, independent of the chosen lift. It does not assume a
full independent `(Z/6)^7` Kummer group. That stronger assertion is
unnecessary here.

For either epsilon, write the action of a lift sigma on the six roots
`beta_j*zeta_6^k` of its unique fixed fiber as

```
k -> epsilon*k+c mod6.                          (9)
```

By (8), as sigma ranges over the lifts of a given base element, c is
uniform among the six residues. The two cases are different:

* epsilon=+1: (9) has a fixed root exactly when c=0. Pass fraction 1/6;
  exclusion fraction 5/6. These primes are `31 mod42`.
* epsilon=-1: a fixed root requires `2k=c mod6`, solvable exactly for
  even c. Pass fraction 1/2; exclusion fraction 1/2. These primes are
  `17 mod42`. Equivalently, sixth powers and squares agree in F_p^*
  when `p=2 mod3`.

These are counts of **group elements with a fixed root**, not counts
of their fixed roots. In the second case a passing element fixes two
roots, which does not double its weight. The two base classes have
equal size and every base element has `|N_6|` lifts. Chebotarev
therefore gives overall relative pass density

```
(1/2)*(1/6)+(1/2)*(1/2)=1/3,
```

and exact relative exclusion density **2/3 among primes `p=3 mod7`**.
The absolute density among all primes is `(1/6)*(2/3)=1/9`. The
conditional exclusion density in the `p=1 mod3` half is 5/6, not 2/3;
forgetting the action on sixth roots of unity gives the wrong denominator.

## 5. Scope and comparison with the Space result

For any p=S this is an explicit finite-field whole-length test. It
excludes infinitely many unbounded lengths. Its asymptotic proportions
are relative to primes in one residue class, not to all lengths.
Lengths with prime `7L-4` themselves have density zero among integers.
Thus neither (6) nor its sextic improvement proves a density-one set of
excluded lengths, and neither settles the composite-S cases.

The Space report separately claims natural density zero, **among all
lengths**, for lengths admitting even an unbounded exponent with
`S|F`. That uses prime divisors of composite S, orders, and character
sums; it is a different theorem with a different denominator. The
prime-S argument here neither supplies nor contradicts that broader
claim. Any reliance on that claim requires its own source/proof audit.
Even an audited density-zero exceptional set permits an isolated full
witness, and cannot replace a bound on the final surviving lift.

As concrete controls for the word "necessary", p=59 (L=9) passes the
square-root test, and p=283 (L=41) passes the sixth-root test. At neither
length does any admissible `i=3 mod6`, `3<=i<L`, satisfy `9S|F`.

## 6. Reproduction

`prime_density_checks.py` uses only the Python standard library. It
checks the four primes by exhaustive roots, the good-prime conditions,
the affine conjugations and fixed fibers, both actions (9), and all
prime-S cases up to p=10000 against exhaustive root sets. The finite
counts are regression evidence, **not** a numerical proof of either
asymptotic density. All required checks remain active with Python `-O`.

```
python3 research/a398769/five-seven/prime-sum/prime_density_checks.py
python3 -O research/a398769/five-seven/prime-sum/prime_density_checks.py
```
