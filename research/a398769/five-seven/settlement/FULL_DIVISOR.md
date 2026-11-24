# Conditions contributed by the full digit sum divisor

These are ordinary elementary proofs on the audited residual domain:
odd `L >= 5`, `3 <= i < L`, `i=3 (mod 6)`,

```text
n = 7*R_L - 2*(1+10^i), R_L=(10^L-1)/9,
P=25*7^(L-2), S=7L-4, F=9n.
```

They are not new Lean statements. The 5, 11 and 13 arguments preserve
the hypotheses of [the prior notes](../prior-notes/README.md); the 37 and
101 conditions extend that list.

## Exact factorization of the full test

The suffix is 775, so `n=25*(31+40a)` for some integer `a`, giving
`v_5(n)=2`. A full solution therefore has `5` not dividing `S`, or
equivalently `L != 2 (mod 5)`. Also `S=-4 (mod 7)` never has a factor 7.
Consequently, after the length filter, `gcd(P,S)=1` and `25 | n`.

Thus on this filtered domain the full test can equivalently be separated
into

```text
7^(L-2) | F             and             S | n.
```

The latter condition is **`9*S | F`**, not merely `S | F`, because
`F=9n`. Without first imposing the 5 filter, the coprimality deduction
would be invalid. At every stage the universally valid exact test remains

```text
225*7^(L-2)*(7L-4) | F.
```

## Modulo 11

Both `L` and `i` are odd. Since `10=-1 (mod 11)`,
`F=-7+18-25=-14 (mod 11)`, and division by the unit 9 gives
`n=7 (mod 11)`. Hence `11` cannot divide `S`, so
`L != 10 (mod 11)`.

## Modulo 13

The order of 10 modulo 13 is 6 and `10^3=-1 (mod 13)`.
Therefore `10^i=-1 (mod 13)` and
`F=7*(10^L-1) (mod 13)`. If `13 | n`, then `6 | L`, contrary
to oddness. Thus `13` cannot divide `S`, so `L != 8 (mod 13)`.

## Modulo 37: an additional full-divisor filter

The identities `10^3=1 (mod 37)` and `R_3=111=0 (mod 37)` imply
that `R_L` has residues `0,1,11` when `L` is respectively `0,1,2`
modulo 3. Also `3 | i`, so `10^i=1 (mod 37)`. It follows that

| L modulo 3 | n modulo 37 |
|---:|---:|
| 0 | -4 |
| 1 | 3 |
| 2 | -1 |

None is zero. A full solution therefore requires `37` not dividing
`S=7L-4`, equivalently

```text
L != 27 (mod 37).
```

## Modulo 101: a second additional full-divisor filter

Since `10^2=-1 (mod 101)`, every odd power of 10 is either 10 or -10.
Both exponents `L,i` are odd. Thus `F` is congruent to one of

```text
7*10-18*10-25   = -135,
7*10+18*10-25   = 225,
-7*10-18*10-25  = -275,
-7*10+18*10-25  = 85
```

modulo 101. None is zero, so `101` cannot divide `n` or `S`.
Since `7*15-4=101`, this excludes `L=15 (mod 101)`.

These length filters exclude infinite families using the full divisor.
They do not exclude every length. A finite computation that rules out
the weaker 7-power condition may omit these filters to retain broader
coverage; it must not claim that doing so tested the full divisor on a
weak survivor.
