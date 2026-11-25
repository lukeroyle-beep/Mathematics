# Infinite full digit-sum survivors at seven-adic depth four

This is an ordinary proof, independently reconstructed from the supplied
post-PR-11 prompt. It establishes infinitely many actual bounded positions
passing the full digit sum and `7^4`. It does not establish a full witness.
The finite arithmetic is reproduced by `checks_family.py`, including a
separate evaluation of the decimal word by concatenating its four blocks.

Put

```text
c=898129, d=56133=3^6*7*11,
a=193+1470t (t>=0), S=c*3^a, L=(S+4)/7,
F(L,i)=7*10^L-18*10^i-25.
```

For every such `t`, there is an integer `i` in the **open** interval
`41L/100 < i < 42L/100` for which

```text
225*7^4*S divides F(L,i).
```

The equivalent assertion about the original decimal word is
`25*7^4*S | n`, where `n=F/9`. A full witness would instead require
`225*7^(L-2)*S | F`.

## Length and fixed-prime congruences

Exact integer arithmetic at `a=193` gives

```text
(S+4) mod 7=0,
L mod d=11248, L mod 294=97.
```

These identities persist throughout the exponent progression. Indeed

```text
7*lcm(d,294)=3^6*7546,
3^1470=1 mod 7546.
```

Since `a>=193`, both `c*3^a` and its increment as `a` is increased by
1470 are divisible by `3^6`, and the increment is divisible by 7546.
The length numerator therefore changes by a multiple of
`7*lcm(d,294)`. This also proves integrality at every subsequent step.
All lengths are odd, because `c*3^a+4` and 7 are odd.

Impose the exponent classes

```text
i=11337 mod d,       i=1635 mod 2058.
```

For the first class the exact residues are

```text
10^d=1 mod c,
10^11248=508973 mod c,
10^11337=597101 mod c,
7*508973-18*597101-25=0 mod c.
```

Thus `c | F`. Primality of `c` is not needed for this inference. The
identity `10^d=1 mod c` suffices to reduce the nonnegative exponents.
In fact the order is exactly `d`: the residues of `10^(d/p)` for
`p=3,7,11` are respectively `66723,631165,615263`, all different from
one. These are all the prime divisors of `d`, so no proper divisor
of `d` can be the order.

For the second class,

```text
10^97=2159 mod 2401, 10^1635=1105 mod 2401,
10^294=1 mod 343, 10^2058=1 mod 2401,
7*2159-18*1105-25=-4802=-2*2401.
```

The length exponent only needs its period modulo 343, since its term
has coefficient 7. Therefore `L=97 mod 294` and
`i=1635 mod 2058` imply `7^4 | F`.

## The full power of three, including the factor nine

The integer `(7*10^L-25)/9` is well-defined since its numerator is
`7-25=-18=0 mod 9`. Define the following residue modulo `3^a`:

```text
u=((7*10^L-25)/9)*2^(-1) mod 3^a.
```

Only 2 is inverted. Integer division by 9 occurs before reduction. The
identity

```text
F/9=(7*10^L-25)/9-2*10^i
```

proves the exact equivalence

```text
3^(a+2) | F  <=>  10^i=u mod 3^a.                 (1)
```

For every positive integer `m`, elementary lifting of the exponent gives
`v_3(10^m-1)=2+v_3(m)`. For example, induction on powers of 3 and
factorization of `x^3-1` prove the power-of-three case; the remaining
factor coprime to 3 contributes no additional valuation. Consequently
10 has order `3^(a-2)` modulo `3^a`, for `a>=2`. Its powers are precisely
the `3^(a-2)` units congruent to 1 modulo 9.

Here membership and the necessary overlaps follow from a stronger fixed
congruence. Since `7L=c*3^a+4` and `a>=193`,

```text
L=4687 mod 6561,
10^4687=42427 mod 59049,
10^402=49303 mod 59049,
7*42427-18*49303-25=0 mod 59049.
```

The order of 10 modulo `59049=3^10` is `3^8=6561`, so these relations
apply to the actual length. Dividing the last congruence by 9 as an
integer divisibility statement and inverting 2 gives

```text
u=10^402 mod 3^8.
```

In particular `u=1 mod 9`. There is therefore exactly one exponent class
`r_a mod 3^(a-2)` satisfying (1); its reduction modulo the order of 10
modulo `3^8`, namely 729, is `402 mod 729`.

## CRT compatibility and the actual position bound

The first two exponent moduli have greatest common divisor 21, and

```text
11337=1635=18 mod 21.
```

The overlaps with `3^(a-2)` are 729 and 3 respectively. They agree:

```text
11337=402 mod 729, 1635=402=0 mod 3.
```

The generalized Chinese remainder theorem thus supplies exactly one
class modulo

```text
W=lcm(d,2058,3^(a-2))=7546*3^(a-2).
```

Let `r` be its least nonnegative representative. A completely explicit
bounded choice is

```text
i=r+W*(floor((41L-100r)/(100W))+1).                 (2)
```

This is the first member of the class strictly above `41L/100`.
Moreover

```text
W/L=7*7546*3^(a-2)/(9c*3^(a-2)+4)
   < 7*7546/(9c)=52822/8083161 < 1/100.
```

Thus the distance in (2) above the lower endpoint is at most `W`,
strictly less than the interval width, and `i<42L/100`. This is the
needed bounded-position argument; unrestricted CRT compatibility alone
would not suffice.

The four integers `c,3^(a+2),7^4,25` are pairwise coprime: `c` is
coprime to 3, 5, and 7. For `i>=3` and `L>i`, both power-of-ten terms
in `F` are divisible by 25. Combining the congruences therefore gives

```text
c*3^(a+2)*7^4*25 = 225*7^4*S divides F.
```

## Retained restrictions

Every constructed pair has `L>10,000,000`, `i>=417`, and `L-i>=396`.
The exponent congruences give `(L mod 6,i mod 42)=(1,39)`, in particular
`i=3 mod 6`. The five inherited forbidden factors of `S` are
`5,11,13,37,101`; none divides `c*3^a`, since none divides `c` and none
is 3. This proves all five corresponding length restrictions for every
`t`, rather than only for the sample.

The entire interval `(41/100,42/100)` lies strictly outside all seven
proportional exclusion strips recorded in the merged coverage note.
For instance `abs(5i-2L)>L/20`, `abs(L-2i)>4L/25`, and the other
strip comparisons have similarly positive fixed margins. The midpoint
difference also exceeds 179 at these lengths. This only says that the
construction survives these necessary restrictions; it does not say
that it survives every conceivable additional test.

## Reproducible sample

At `a=193`, (2) gives exactly

```text
L=15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553
i=6477065490626893175017379503058848761317334778884442403179846853582090755525695000140054741394429
F mod (9S)=0,
F mod 16807=9604=4*2401.
```

Thus this particular pair has `v_7(F)=4` exactly and is **not** a full
witness. The infinite theorem gives only `v_7(F)>=4`; it does not claim
an upper bound for all its positions.

The independent decimal evaluation concatenates
`7...(L-i-1 digits), 5, 7...(i-1 digits), 5` modulo the specified divisor.
It computes repunits by reducing `10^m` modulo nine times the divisor
and then dividing the resulting integer minus one by 9. It verifies
`n mod (25*7^4*S)=0` and the same exact valuation, without allocating
an enormous decimal string. Small literal decimal words check that
this block implementation agrees with direct construction.

## What a variable-c, variable-depth extension must establish

For a proposed `S=c*3^a`, assume `c>1`, `a>=2`, `gcd(c,30)=1`, and that
`L=(c*3^a+4)/7` is an integer. The three-adic class must first exist;
for `a>=8` the preceding membership argument applies. Modulo `c`, the
full sum equation is `18*10^i=7*10^L-25 mod c`. Invertibility of 18
and subgroup membership must be checked; if it holds, it gives a class
modulo `d_c=ord_c(10)`. Modulo `7^k`, the target is a unit and the
primitive-root property of 10 gives one class modulo `T_k=6*7^(k-1)`.
All pairwise overlaps of these three classes must agree.

When they do, put

```text
J=lcm(d_c,T_k), g=gcd(J,3^(a-2)),
W=J*3^(a-2)/g.
```

Then `W/L < 7J/(9cg)`, so `700J <= 9cg` is a sufficient spacing
condition for every target interval of width `L/100`. The exact
necessary-and-sufficient test is still to compute the least compatible
representative `r`, take (2), and check its strict upper endpoint.
A spacing condition that fails is **not** a proof of nonexistence.

For the fixed `c,d` in the present theorem and `k>=4`, this becomes

```text
W_k=22*7^(k-1)*3^(a-2),
W_k/L < 154*7^(k-1)/(9c).
```

The useful spacing ratio increases by seven at each new depth. The
uniform interval-width guarantee holds at depth four and already fails
at depth five. One cannot infer arbitrary depth merely by taking `a`
larger, because the limiting ratio is independent of `a`. A uniform
extension would need compatible choices of `c,k` with proved size and
order control, or a new argument placing the least representative in
the interval despite the larger spacing. Neither follows from this
infinite family alone.
