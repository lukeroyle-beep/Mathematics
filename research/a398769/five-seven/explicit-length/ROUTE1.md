# Published effectivity audit and a seven-free-quotient subfamily

26 November 2026. This investigation obtains **no unconditional global
length bound**. It does obtain an explicit bound on the precisely defined
subfamily in section 4. The results are ordinary proofs, not Lean theorems.

## 1. The qualitative statement and the exact missing datum

For integers `L>=5, 3<=i<L`, put

```
F=7*10^L-18*10^i-25,
A=7*10^L/25, V=18*10^i/25, W=F/25,
x=(A,-V,-1,-W), Sigma={2,3,5,7}.
```

These are nonzero integers, `A=V+1+W`, and `W>0`. The common gcd is one.
Every nonempty subsum omitting A is negative; any proper subsum containing
A is positive, since its omitted complement is negative. Thus no proper
nonempty subsum vanishes. The primitive projective height is exactly A.
Only W contributes primes outside Sigma, so

```
product out_Sigma(x_j) = out_Sigma(W) <= W/7^t < A/7^t.
```

If `t>=L/2`, then `A<49^L` gives `out_Sigma(W)<A^(3/4)`.
Evertse's Corollary 1 therefore applies with `n=3,c=1,d=3/4`.
For general epsilon use `e=min(epsilon,1/2)` and
`d=1-e*log7/log10`. This proves uniform `t=o(L)`, since the tuple map is
injective. Neither the digit-sum condition nor primality of S is used.

The published input is J.-H. Evertse, *On sums of S-units and linear
recurrences*, Compositio Mathematica 53 (1984), 225--244,
[Corollary 1, p.227](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf).
Its proof uses Theorem 4 on p.231. After equation (22), p.232, the
induction constant depends on the coefficients of the exceptional
subspaces supplied by that theorem. Section 3, pp.234--235, uses this
constant to bound the height. Those coefficient heights are not bounded
effectively in this argument. This is the first loss of effectivity;
passing from a tuple height to L is elementary.

Specifically, an explicit upper bound `A<=H_*` for every exceptional
tuple would imply

```
L <= floor(log_10(25*H_*/7)).
```

No value for `H_*` is supplied by the qualitative proof. Taking the
maximum of the finitely many exceptional lengths merely names the
missing integer; it is not a computable expression for it. An explicit
upper bound on the number of exceptions would still allow an exception
of unknown height. The same issue persists even if there is only one.

## 2. Checks of proposed effective replacements

The following are primary-source checks, not claims that no other theorem
could ever settle this family.

* **Quantitative Subspace Theorem.** Evertse--Ferretti,
  [*A further improvement of the Quantitative Subspace Theorem*](https://annals.math.princeton.edu/wp-content/uploads/annals-v177-n2-p04-p.pdf),
  Annals 177 (2013), Theorem 2.1, p.520, bounds the number of covering
  subspaces. Theorem 2.3, p.522, is stronger: outside an effectively
  computable exceptional subspace, it confines the height parameter to
  finitely many intervals `[Q_j,Q_j^omega)`. The numbers of intervals and
  omega are explicit; their locations `Q_j` are not. An explicit lower
  threshold for these intervals is not an upper endpoint. Neither result
  supplies the missing `H_*`.

* **An effectively computable exceptional subspace.** Evertse,
  [*On the Quantitative Subspace Theorem*](https://arxiv.org/pdf/1008.2268),
  Theorem C, pp.8--9, and the discussion on pp.10--11, distinguish the
  effectively determined subspace `U0` from the finitely many solutions
  outside it. On p.11 the paper explicitly says the latter cannot be
  determined effectively by this result. Thus identifying `U0`, even
  when it consists of vanishing-subsum conditions incompatible with our
  tuple, does not bound the exceptional solutions. Theorem 3.1 there
  again leaves the interval locations unspecified.

* **Effective multi-term S-unit equations.** Bajpai--Bennett,
  [*Effective S-unit Equations Beyond 3 Terms: Newman's Conjecture*](https://arxiv.org/pdf/2308.05162),
  Theorem 1, printed p.2, requires fixed coefficients, S-unit variables,
  and at most three places including the infinite places. In our
  equation the residual factor `F/7^t` is unrestricted. Putting its
  primes into S makes S vary; absorbing it into a coefficient makes the
  coefficient height vary. Even the fixed supports of 10 and 7 require
  `{infinity,2,5,7}`, four places. These are failed hypotheses, not
  missing numerical substitutions.

* **Fixed recurrence results.** Bugeaud--Evertse,
  [*S-parts of terms of integer linear recurrence sequences*](https://pub.math.leidenuniv.nl/~evertsejh/16-LinRecBuEv.pdf),
  Theorem 1.2, printed p.4, gives an effective power saving for a fixed
  recurrence with a dominant root. Fixing a rational slope and both
  offsets does produce such a recurrence. Varying them changes the
  recurrence data and its constants. In addition, a positive saving
  alone need not exceed `1-log7/log10`. It does not provide a uniform
  closing bound on our two-exponent domain.

* **Ordinary three-digit integers.** Bugeaud,
  [*On the digital representation of integers with bounded prime factors*](https://arxiv.org/pdf/1609.07926),
  Theorem 1.2, p.3, requires ordinary nonnegative base digits. F has
  negative coefficients and decimal borrowing creates long runs. Its
  auxiliary logarithm estimates, Theorems 2.2 and 2.3, pp.4--5, do
  apply after the separate signed reduction below. They yield an
  explicit but insufficient global saving, not the requested global U.

The 2026 paper Adiceam--Shirandami,
[*Probabilistic effectivity in the Subspace Theorem*](https://link.springer.com/article/10.1007/s40993-025-00692-0),
Introduction section 1.1 and Theorem 1.6, estimates proportions of
coefficient systems. It is not a pointwise height theorem for this fixed
coefficient system; no probabilistic exclusion is substituted here.

## 3. An applicable signed estimate, with its constants retained

Here we independently check the useful intermediate form of the signed
argument in [prime-sum/GLOBAL.md](../prime-sum/GLOBAL.md). For every
`L>=5, 3<=i<L`, set `M=F/7^t`, `a=log(max(M,25))`. If `t>=L/2`, then

```
L < 10^16*a.                                             (1)
```

For completeness, `10^L<F<7*10^L`, `2L<log F<3L`, and `t<2L`.
The signed reductions and all source parameters are as follows. Both
forms are nonzero, since their displayed expressions are nonzero.

If `i<=L/2`, use Theorem 2.2 with rational bases `(7,10,M/7)`, integer
exponents `(t,-L,1)`, and height bounds `(7,10,max(M,25))`. All bases
are positive and the height floors are met, including for reduced M/7.
Then

```
Lambda = 7^t*10^(-L)*(M/7)-1
       = -(18*10^i+25)/(7*10^L),
log|Lambda| < -L/2,
B_source <= max(1,4L/a).
```

The source coefficient `8*30^6*3^(9/2)<10^12`, and `log7*log10<6`.
Consequently for `x=L/a>=1`,

```
x < 12*10^12*(1+log(4x)).                              (2)
```

The function `x/(1+log(4x))` increases for `x>=1`. At `x=10^16`,
`log(4x)<42`, using `log10<5/2` and `log4<2`, while
`12*10^12*43<10^16`. Thus (2) forces `x<10^16`; `x<1` is immediate.

If `i>=L/2`, use Theorem 2.3 with `p=2`, rational bases `(7,-M/25)`,
exponents `(t,1)`, heights `(7,max(M,25))`, and `B_source=t,B_n=1`.
Negative rational bases are allowed by this theorem. F and M are odd,
so both bases are two-adic units. The exponent 1 has minimal two-adic
valuation, and `t>=L/2` implies `t>=3`. We have

```
Lambda = 7^t*(-M/25)-1
       = -10^i*(7*10^(L-i)-18)/25,
v2(Lambda)>=i>=L/2.
```

If `a/t>1/2`, then `a>L/4`. Otherwise set `delta=a/t` in the theorem;
it lies in `(0,1/2]`. The auxiliary quantity is
`T=16*exp(51)*log7*(t/a)`, whence `log T<60+log(2L/a)`.
The leading coefficient is below `2*10^12`:

```
(16e)^6*2^(3/2)*(log4)^2*2/(log2)^2
 < 48^6*3*4*8 < 2*10^12.
```

Both entries of its maximum are at most `2a*log T`. Thus, for `x>=1`,

```
x < 8*10^12*(60+log(2x)).                              (3)
```

The ratio `x/(60+log(2x))` increases for `x>=1`. At `x=10^16`,
`log(2x)<41` and `8*10^12*101<10^16`. This proves (1) in both cases.
The elementary logarithm bounds used here can be certified by the
positive exponential series; no rounded decimal logarithm is required.

Equation (1) implies the inherited global bound
`7^t<25*F^(1-1/(3*10^16))`, with starting length 5. Its coefficient of
L after taking logarithms is
`(1-1/(3*10^16))*log10/log7>1`: the saving exponent exceeds `9/10`,
whereas `log7/log10<9/10` follows from `7^10<10^9`. There is therefore
no contradiction with `t>=L-2`, however large L becomes.

## 4. New explicit cutoff when the quotient's seven-free part is small

Fix any integer `d>=0`. For a **full witness**, define the positive
integer quotient and its seven-free part by

```
q = n/(P*S) = F/(225*S*7^(L-2)),
q0 = q/7^v7(q).
```

The following is unconditional on the stated subfamily:

> If `q0<=L^d`, then `L<=U_d=10^18*(d+1)^2-1`.

There is no restriction on the prime divisors of q0. In particular q0
is not assumed to be an S-unit in a fixed group. The additional
hypothesis is its size, not its prime support. This differs from the
elementary restriction `q<=L^d`: q may have an arbitrarily large
seven-power factor.

Proof. Since `7` does not divide `225S`, exact valuation gives
`t=L-2+v7(q)` and

```
M=F/7^t=225*S*q0.
```

The factor 225 is retained even when `3|S`. Also `M>=225*31>25`.
The witness condition gives `t>=L-2>=L/2`, so (1) applies. If `m=d+1`,
then `M<1575*L^m` and

```
L < 10^16*log M < 10^16*(10+m*log L),                (4)
```

using `1575<10^4` and `log10<5/2`.
Set `X=10^18*m^2`. For `m>=1`, `log m<=m`, and hence

```
log X < 45+2m,
10^16*(10+m*log X)
 < 10^16*(10+45m+2m^2)
 <= 57*10^16*m^2 < X.
```

For `L>=X`, the derivative of `L-10^16*(10+m*log L)` is
`1-10^16*m/L>=1-1/(100m)>0`. Thus (4) fails for every `L>=X`.
Since L is integral, `L<=X-1`, proving the assertion. This is uniform
in i and covers composite S without factoring it.

Two completely instantiated examples are

```
q0=1:       U_0   = 999999999999999999,
q0<=L^100:  U_100 = 10200999999999999999999.
```

These cutoffs exceed the inherited consecutive endpoint
`B=1000002000000`. They do not settle either subfamily: the respective
odd lengths `B<L<=U_d`, subject to the other already proved exclusions,
remain a finite checking obligation. No enumeration of that immense
remainder is claimed here. Nor has `q0<=L^d` been proved for all
witnesses for any fixed d. Without that extra theorem, these U_d are
not global U for the original subclass.

## Sources and reproduction

Primary source statements above were reopened online on 26 November
2026. Retained local primary PDFs were hashed and matched the existing
repository source receipts:

| PDF | SHA-256 |
|---|---|
| Evertse 1984 | `5b02e0e31c546f7f8c6c34071b2caa4d7137be24f16d11d483cdcc65377b2f6d` |
| Bugeaud arXiv:1609.07926v1 | `eb88ba3dcecf7e56066a11124368f8f2013ee6def488785729b6fdef85212ab7` |
| Bajpai--Bennett arXiv:2308.05162v1 | `be15d92f9e0edd914b2525f4c9c888e3d83859028a03ccba3596b8feba9b91be` |

The published theorem statements and the substitutions, rather than
the historical hashes, are the mathematical evidence. The explicit
arithmetic can be reproduced without floating point:

```sh
python3 - <<'PY'
from fractions import Fraction as Q
from math import factorial
def require(ok):
    if not ok: raise ArithmeticError('failed comparison')
# e<3 follows from the factorial series and geometric tail; e>2 is immediate.
# exp(5/2)>10 and exp(1)<3 prove the log bounds used above.
require(sum(Q(5,2)**j/factorial(j) for j in range(8)) > 10)
require(sum(Q(1,2)**j/factorial(j) for j in range(7))
        + (Q(1,2)**7/factorial(7))/(1-Q(1,16)) < 2)
require((8*30**6)**2*3**9 < 10**24)
require(48**6*3*4*8 < 2*10**12)
require(12*10**12*43 < 10**16)
require(8*10**12*101 < 10**16)
require(57*10**16 < 10**18)
require(7**10 < 10**9)
print({'U_0': 10**18-1, 'U_100': 10**18*101**2-1})
PY
```

The first unproved implication in route 1 remains a computable upper
bound on the exceptional heights, or a different estimate strong enough
to yield one uniformly. The exact subfamily theorem above supplies
neither the missing height bound nor a bound on q0 for arbitrary
witnesses.
