# Decimal height versus seven-adic valuation

26 November 2026. **The proposed global inequality remains unproved and
unrefuted.** This note verifies its exact premise and payoff, proves
effective subdomains, and identifies the missing assertion at the actual
sum-compatible position. All results here are ordinary mathematics and
exact arithmetic, not new Lean formalizations.

## Domain, integer cofactor, and conditional payoff

Let `B=1000002000000`. The requested domain is every odd integer `L>B`
and every integer `3<=i<L` such that

```
S=7L-4, F=7*10^L-18*10^i-25, 5 does not divide S, 9S divides F.
```

There is no prime-S assumption. Let `t=v7(F)` and `D=225S`. The stronger
elementary size bounds

```
5*10^L < 52*10^(L-1)-25 <= F < 7*10^L                 (1)
```

hold already for `L>=5`. Also `F=-25 mod125` since `i>=3`, so `v5(F)=2`.
As `gcd(25,9S)=1`, the hypotheses `25|F` and `9S|F` give `D|F`.
Thus `H=F/D` is a positive integer. Since `S=3 mod7`, `7` does not
divide D and **`v7(H)=t`**. This remains valid when `3|S`: we combine
coprime factors 25 and **9S**, and never cancel nine against S.

For clarity, the original decimal word has fives at positions 0 and i
from the right and sevens elsewhere. It is

```
n=7*(1+10+...+10^(L-1))-2-2*10^i=F/9,
digit sum S=7L-4, digit product P=25*7^(L-2).
```

Consequently `PS|n` is exactly `225S*7^(L-2)|F`, or, on the stated
sum-compatible domain, `t>=L-2`. A failure of the proposed inequality
alone would not establish this stronger divisibility.

If the proposed inequality `10^t<=10^12 H` held at a full witness,
then

```
225S*10^(L-2) <= 225S*10^t <= 10^12 F < 7*10^(L+12),
225*(7L-4) < 700000000000000,
1575L < 700000000000900.
```

The largest integer allowed by the strict last inequality is exactly
`444444444445`: multiplication by 1575 gives `700000000000875`,
whereas the next integer gives `700000000002450`. The allowed endpoint
is odd. It is below B, so the certified consecutive exclusion through B
and the proposed inequality **would** close the `{5,7}` subclass. This
is a conditional implication, not proof of its premise.

## Exact decimal threshold, including equality

Let d be the number of decimal digits of the positive integer H, so
`10^(d-1)<=H<10^d`. Then

```
10^t <= 10^12 H  iff  t <= d+11.                       (2)
```

Indeed `t<=d+11` implies `10^t<=10^(d+11)<=10^12 H`.
If `t>=d+12`, then `10^t>=10^(d+12)>10^12 H`. These are exact
integer comparisons; no rounded logarithm is involved. Equality is
allowed at the lower decimal boundary. Failure is precisely

```
t>=d+12  iff  7^(d+12) divides F.                      (3)
```

Here d depends on the same actual pair `(L,i)`; it is not an independent
length parameter. Statements (2)--(3) require the proved integrality of H.

For computation set `q=digits(D)`. In our domain `L>=q`, and (1) gives

```
d in {L-q+1, L-q+2}.
d=L-q+2  iff  F>=D*10^(L-q+1).                         (4)
```

Here `L>=q` follows, for example, from `D<10^L` at L=5 and induction
(the right side multiplies by ten while D grows linearly).
The smaller alternative applies otherwise. Equivalently, the comparison
in (4) is the sign of

```
(7*10^(q-1)-D)*10^(L-q+1)-18*10^i-25.
```

Similarly the target is the sign of `10^12 F-D*10^t`. These sparse
signed decimal expressions need only a few coefficients and integer
exponents, even when the decimal word itself cannot be allocated.
[checks.py](checks.py) uses exact coefficient dominance and short-gap
merging; it tests exact cancellation and powers-of-ten endpoints against
ordinary integers on affordable inputs.

Since `L>B`, `D>7*10^14`. Thus `H<10^(L-14)` and

```
d<=L-14, hence d+11<=L-3.                              (5)
```

The strict upper decimal bound is essential: it gives at most `L-14`
digits, not `L-13`. At larger lengths the proposed deadline can be
earlier still. The target is stronger than merely rejecting full witnesses.

## Low valuation and the actual representative

Put `T_k=6*7^(k-1)` and `K=min{k>=1:T_k>L}`. Order six modulo seven
and `v7(10^6-1)=1` imply by binomial lifting

```
ord_(7^k)(10)=T_k,
10^T_k=1+7^k*c_k with c_k=1 mod7.
```

Ten generates the entire unit group modulo `7^k`. Hence the unit
`(7*10^L-25)/18` has one exponent `r_k in [0,T_k)`. It satisfies
`r_k=3 mod6` and `7^k|F(L,r_k)`.

There is a particularly simple explicit size discharge. For every odd
`L>=9`,

```
T_((L-1)/2)>L,  D<10^((L+1)/2),
H>10^((L-1)/2),  K<=(L-1)/2.                          (6)
```

The first two inequalities hold at L=9 (`2058>9`, `13275<100000`).
Increasing L by two multiplies the first left side by seven and the
second right side by ten; `D(L+2)=D(L)+3150<10D(L)` for `L>=9`.
Thus induction proves both. The bound on H follows from `F>10^L`.
In particular **every pair with `t<=floor(L/2)` already has `10^t<H`**.
This includes every `t<K`, with no unverified finite gap on `L>B`.

The low-depth conclusion alone extends to all integer `L>=5`, without
sum compatibility. For `L>=9`, two-step induction at L=9,10 gives
`D<10^(floor(L/2)+1)`; induction at L=5,6 gives `K<=ceil(L/2)`.
Hence `F/D>10^(ceil(L/2)-1)>=10^(K-1)`. The four lengths 5,6,7,8
are checked directly with `F>=52*10^(L-1)-25` and `K=1,2,2,2`.

For `t>=K`, congruence `i=r_K mod T_K`, together with `0<=i<L<T_K`,
forces **`i=r_K`**. There is at most one actual high-depth position
per length. A full-sum check at some other exponent is irrelevant.

The lifted residues obey

```
r_(j+1)=r_j+a_j*T_j,  0<=a_j<=6,
a_j=5*(F(L,r_j)/7^j) mod7.                            (7)
```

This follows by expanding `10^(a_j*T_j)` modulo `7^(j+1)` and using
`18*10^r_j=3 mod7`. Once `j>=K`, a nonzero digit sends the representative
above L permanently. Until then `r_j=i`. The first nonzero digit is
`a_t`, with **exact** valuation t; the preceding `t-K` digits are zero.
Positivity of F guarantees this first nonzero digit eventually exists.

Consequently the requested assertion on the remaining domain is exactly:

> Every actual `r_K in [3,L)` passing `5∤S` and `9S|F(L,r_K)` has a
> nonzero lift digit at some **inclusive** index `K<=j<=d+11`.

This is the **first unsupported global assertion**. Formula (6) ensures
`K<=d+11`; (5) ensures its upper endpoint is at most `L-3`. A first
nonzero digit at `d+12` is too late for the inequality. A first nonzero
digit at `L-2` is too late to reject a full witness. Neither endpoint
can be silently shifted by one.

## What the exact sum divisor contributes

During the constant-representative part of the lift, for `K<=j<=t`,
`D=225S=3 mod7` turns (7) into

```
a_j = H/7^j mod7.                                    (8)
```

Thus the missing assertion is a restriction on the trailing base-seven
zeros of this particular integer cofactor relative to its decimal
length. Extracting the exact divisor preserves, rather than reduces,
its seven-adic valuation. Positive size alone gives only `7^t<=H`.
It does not justify replacing seven by ten with the prescribed constant.
For example the abstract integers `H=7^100`, `t=100` violate the proposed
comparison, by exact powering. They are **not** claimed to arise from
any `(L,i)` and are not counterexamples to the research target.

The full sum also defines an exponent class, including when `3|S`.
If `n_i` and `n_s` both vanish modulo S, their difference is
`-2*(10^i-10^s)`. Since `gcd(2,S)=1`, full-sum exponents are exactly
one class `s mod o`, where `o=ord_S(10)`, when any exist. This argument
uses n, avoiding the invalid cancellation of 18 modulo a multiple of 3.

Let `e=v7(o)`. The inherited order argument gives `e<=K-1`:
if `e>=1`, some prime `p|S` has `7^e|p-1`; parity and compositeness of
`2*7^e+1` force `p>=4*7^e+1`. Also `S/p` is positive odd and `3 mod7`,
so `S/p>=3`. Hence `L>=12*7^(e-1)+1=2T_e+1`, contradicting `T_K>L`
if `e>=K`. For all `j>=K`, therefore,

```
gcd(o,T_j)=gcd(o,6)*7^e
```

is constant. If `r_K` passes the exact sum, unbounded exponent CRT
compatibility persists at every later depth. It cannot force a later
incompatibility. The shared exponent may be outside `[3,L)`; controlling
that bounded representative is precisely the missing step. This is an
obstruction to this CRT argument, not a claim that the sum condition
can never help by a different method.

## Effective and qualitative replacements

Besides (6), the following proved subdomains do establish the target.
They hold for composite and prime S alike, whenever H is integral.

1. **An exact computable position criterion.** For odd `L>=5`, the
   inherited [quadratic-root estimate](../effective/ROUTE_A.md) is
   `t<=504*(|L-2i|+2)*max(log L+2,20)^2`. Let `m=digits(L)` and
   `U=max(3m+2,20)`. Since `log10<3`, it suffices on `L>B` that

   ```
   504*(|L-2i|+2)*U^2 <= L-q+12,  q=digits(225S).       (9)
   ```

   Equations (4) and (9) give `t<=d+11` by integer arithmetic.
   The valuation estimate starts at five; (9) is a checked condition
   at the actual position, so there is no omitted finite interval.

2. **A fixed positive-width midpoint strip.** The stronger normalized
   application in [proportional/AUDIT.md](../proportional/AUDIT.md),
   equation (C), gives, on `|L-2i|<=L/60000` and odd `L>=10000000`,

   ```
   t <= (58989/62500)*L + 2831472/25.                 (10)
   ```

   This implies the present target on the whole requested strip,
   not merely witness rejection. To see this explicitly, for `L>=1000`
   put `h=floor(L/100)>=10`. Then
   `D<157500(h+1)<10^h`; the second inequality holds at h=10 and
   persists by induction. Therefore `q<=h<=L/100`. By (4),
   `d+11>=L-q+12>=(99/100)L+12`. Subtracting (10) leaves

   ```
   (2886/62500)*L - 2831172/25,
   ```

   positive already at `L=10000000`, with positive slope. Thus every
   sum-compatible pair in this closed strip above B satisfies the target.
   Positions with `i!=3 mod6` have t=0 and are immediate. There is no
   new finite gap, no assertion that this strip covers every actual r_K,
   and no conversion of a position strip into an all-length theorem.

3. **Inherited finite valuation coverage.** The PR #22 archive certificate
   bounds t by 27 for every odd `5<=L<=10^12` and every actual position;
   PR #21's adjoining interval bounds every actual depth-K representative
   by 21, with K=15. For odd `L>=31`, (6) gives `d+11>=27`, so these
   inherited bounds imply the present target. The literal checks through
   301 include every smaller pair. Thus the target is also certified on
   every sum-compatible odd `5<=L<=B`. This is a consequence of inherited
   valuation certificates, not of witness exclusion alone. The fresh
   rerun checks all 74,601 retained archive candidates; enumeration
   completeness and the adjacent interval are inherited, with source
   and artifact bindings checked. Neither large enumeration is claimed
   as freshly executed in this investigation.

The published input to both estimates is Bugeaud--Laurent,
[Corollary 1, printed p.4](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
The repository derivations check multiplicative independence, the local
degree one and global degree at most two, root height, and all numerical
constants. The normalized bound uses height parameter `L/60000+2`,
degree-two maximum at most `10.6`, and coefficient `504*(10.6)^2`;
the degree-one case is smaller. The source and these hypotheses were
rechecked for this application; no arbitrary cofactor is treated as a
fixed algebraic base.

The inherited [uniform `t=o(L)` theorem](../effective/QUALITATIVE.md)
implies the target for **all sufficiently large L**, since eventually
`t<L/2` and (6) applies. This is the strongest global asymptotic
replacement here, but its starting length is ineffective. It follows
from [Evertse's Corollary 1](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf),
which supplies no computable exceptional-height endpoint in this
application. In particular the possible failure set above B is finite,
but neither its emptiness nor its maximum is established.

PR #22's effective signed bound, valid for all `L>=5,3<=i<L`, is
`7^t<25F^(1-1/(3*10^16))`. It gives a valuation coefficient
`(1-1/(3*10^16))*log10/log7>1`, whereas here the needed threshold is
`L-O(log L)`. The coefficient exceeds one because the exponent exceeds
`9/10` and `7^10<10^9`. Thus the explicit bound does not prove (2).
An ineffective stronger asymptotic and an effective weaker bound do not
jointly supply the missing effective starting length.

## Outcome and remaining obligation

No pair in the requested domain violating the inequality was found.
No full witness was found. The bounded checks in [README.md](README.md)
are evidence only on their declared inputs. The global missing assertion
is the nonzero digit in `[K,d+11]` at every actual full-sum-compatible
representative. It is neither assumed for pruning nor inferred from
generic cofactor size, CRT compatibility, or the qualitative theorem.

The **inequality is open** on the full requested domain. The **`{5,7}`
subclass is open**, with its inherited consecutive exclusion through B.
The **wider A398769 digit-1 conjecture is open** independently of this
subclass. A proof of the inequality would settle this subclass; it would
still leave the other digit families. Density questions are outside
this investigation.
