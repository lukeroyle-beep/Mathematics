# An individual-length increment test

All three proposed claims about `W` are true. The test does not assume
anything about the valuation, actuality, or failure of the preceding
length. Its last case is an exact reformulation of the remaining
moving-position question, not a proof of its exclusion.

## The word and the two ternary representatives

Let `a=31+6u`, `S=3^a`, and `L=(S+4)/7`. The decimal word with fives
at positions zero and `s` and sevens elsewhere has

```
n=7(1+10+...+10^(L-1))-2-2*10^s,
P=25*7^(L-2),  S=7L-4,
F(L,s)=9n=7*10^L-18*10^s-25.
PS | n  iff  225*S*7^(L-2) | F(L,s).
```

An actual position requires `3<=s<L`. Here `v5(F)=2`, and once
`9S|F` holds at this same position, the full predicate is exactly
`t=v7(F)>=L-2`. In particular, equality qualifies. Multiplication by
nine does not change the seven-adic valuation.

Use the fixed constant and exact precisions proved in
[`../power-three/INDIVIDUAL.md`](../power-three/INDIVIDUAL.md):

```
theta^7=10^4, theta in 1+9 Z_3,
C=(7theta-25)/18, kappa=log(C)/log(10), kappa=6 mod9,
9*3^a | F(L,s)  iff  s=kappa mod3^(a-2).
```

The necessary condition `7|F` gives `s=3 mod6`. Thus the sole possible
position is the least nonnegative **odd** representative `s_a` of kappa
modulo `3^(a-2)`, in `[0,2*3^(a-2))`; it is at least three.
The interval is longer than the length, so the representative may miss
the word entirely. A congruence solution outside `[3,L)` is not a word.

For `a>=37`, put `b=a-6`, `D=3^(b-2)`. Both `s_b` and `s_a` are odd,
and `s_a=s_b modD`. Therefore their difference is divisible by `2D`.
The ranges `0<=s_b<2D` and `0<=s_a<2*729D` prove uniquely that

```
s_a=s_b+2Dk,       0<=k<=728.
```

Use this `s_b` even when `s_b>=L_b`. No predecessor word or
predecessor seven-adic divisibility is needed.

Since `L=(6561D+4)/7`, define

```
K=floor((L-1-s_b)/(2D)).
```

An actual `s_a` is equivalent to `k<=K`: its lower bound is automatic.
Also `s_b>=3`, so

```
K <= floor((6561D-24)/(14D)) <= 468,
```

because `6561/14=468+9/14<469`. In fact `K` is nonnegative since
`s_b<=2D-1<L-1`. Both increment endpoints zero and 468 are retained.
The base `a=31` is the inherited independently certified exclusion;
it is not subjected to a recurrence requiring an uncertified predecessor.

## Exact valuation differences and unique classes

At the current length, for every nonnegative integer `j`, set

```
W(j)=F(L,s_b+2Dj).
```

All these algebraic evaluations are legitimate even when their
positions are outside the word. Since `3|D` and `s_b=3 mod6`, every
exponent `s_b+2Dj` is `3 mod6`, so `10^(s_b+2Dj)=-1 mod7` and

```
W(j)=18-25=0 mod7.                                  (1)
```

For `i>j`, exact subtraction gives

```
W(i)-W(j)=-18*10^(s_b+2Dj)*(10^(2D(i-j))-1).
```

The first factor is a seven-adic unit. Since `2D=6*(D/3)`,
`7` does not divide `D/3`, and `v7(10^6-1)=1`, LTE gives

```
v7(W(i)-W(j))=1+v7(i-j).                            (2)
```

The same equality holds with `i,j` interchanged. It does not involve
the preceding length.

By (1), `H(j)=W(j)/7` is integer-valued. By (2), for every `r>=0`,
it induces a well-defined injective map on the `7^r` residue classes
modulo `7^r`; hence it is a permutation. This proves that for every
`m>=1` there is exactly one class

```
j_m mod7^(m-1)  with  7^m | W(j_m).                 (3)
```

Choose least nonnegative representatives. They are compatible under
reduction, and `j_1=0`.

## The coefficient and the seven children

The exponent `b-3` is `4 mod6`, so

```
D/3=4 mod7,
(10^6-1)/7=1 mod7,
(10^(2D)-1)/7=4 mod7.
```

Let `G=10^(2D)`. For `m>=1`, `R=7^(m-1)`, and `0<=c<=6`, binomial
expansion gives

```
(G^(cR)-1)/7^m=4c mod7.
```

Here the equality is also valid for `c=0`, with zero numerator.
Because `-18*10^(s_b+2Dj)=18=4 mod7`, subtraction at a fixed j yields

```
(W(j+cR)-W(j))/7^m=2c mod7.                        (4)
```

If `j=j_m`, all seven quotients are integral. With
`z=W(j_m)/7^m mod7`, their residues are **all seven** values
`z+2c mod7`. Precisely one is zero. Since `2^(-1)=4 mod7`,

```
c_m=-4*z mod7,  0<=c_m<=6,
j_(m+1)=j_m+c_m*7^(m-1).                           (5)
```

Thus the requested coefficient is correct, including the first lift
from depth one. For a direct finite audit, compute
`W(j_m+c*7^(m-1)) mod7^(m+1)` separately by modular exponentiation for
each of the seven c, divide these multiples of `7^m`, and compare all
seven resulting residues with (4). Checking only the selected child
would give a weaker audit.

## Depth five and the precise deadline

At depth five the period in j is `7^4=2401>468>=K`. Therefore:

1. If `j_5>K`, no allowed increment passes `7^5`.
2. If `j_5<=K` but `j_5!=k`, the actual ternary increment fails `7^5`.
3. If `j_5=k`, the actual position survives depth five.

The k in this comparison must be recovered from kappa independently of
the seven-adic root. Choosing k to equal an in-range `j_5` would discard
the defining ternary condition. The first two cases exclude a full
witness since `5<=L-2` throughout the present family.

In the last case, the actual k is less than 2401. Every later addition
in (5) is nonnegative, and a positive addition is at least 2401.
Consequently

```
7^(L-2) | W(k)
  iff j_(L-2)=k
  iff c_m=0 for every 5<=m<=L-3.                   (6)
```

Let r be the first index at least five with `c_r!=0`, assuming
`j_5=k`. Then `j_r=k` and `W(k)/7^r` is a unit, so

```
t=v7(W(k))=r,
first failed seven-power depth = r+1.
```

The exclusion sought is exactly `r<=L-3`, equivalently a failure at
depth at most `L-2`. A first nonzero carry at `r=L-2` is too late:
it gives `t=L-2`, which already satisfies the witness threshold.
See [MOVING_BOUND.md](MOVING_BOUND.md) for what is and is not proved
about this last case.
