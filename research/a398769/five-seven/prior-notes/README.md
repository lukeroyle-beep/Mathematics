# All-length A398769 subclass on digits 5 and 7

Investigated on 24 November 2026 after Stage 5 PR #6 was opened.

**Outcome:** an elementary all-length reduction to exactly two occurrences of
5 is proved below. No complete all-length exclusion or counterexample was
obtained. In particular, finite congruence checks are not a proof that the
remaining two-parameter family is empty.

Let n be positive, with every decimal digit in {5,7}, and suppose P(n)S(n)
divides n. Write L for its decimal length, c for its number of fives, and
R_L = (10^L - 1)/9. Position zero is the units position.

## Rigorous reductions

1. **L is odd.** Every digit and n itself are odd. Since S divides n, S is odd;
   its parity equals that of L.

2. **c <= 2.** If c >= 3, then 125 divides P and hence n. The eight possible
   three-place suffixes are 555, 557, 575, 577, 755, 757, 775 and 777. None is
   divisible by 125. Their residues are respectively 55, 57, 75, 77, 5, 7, 25
   and 27. Divisibility by 125 depends only on the final three places.

3. **c = 0 is impossible.** Here n = 7R_L, P = 7^L and S = 7L. The condition
   forces 7^L L to divide R_L, so in particular 7 divides R_L. Since 9 is
   invertible modulo 7 and the order of 10 modulo 7 is 6, this requires 6|L,
   contradicting odd L. This also covers L=1.

4. **c = 1 is impossible.** Since 5 divides n, the sole 5 is the units digit.
   Thus n = 7R_L - 2. If any 7 occurs, then 7 divides P but n is -2 modulo 7,
   a contradiction. The remaining case n=5 has P*S=25 and also fails.

5. **Exactly two 5s remain.** One is the units digit and the other has position
   i with 1 <= i < L. There is at least one 7, since L is odd. Therefore

       n = 7R_L - 2(10^i + 1)
         = (7*10^L - 18*10^i - 25)/9,
       P = 25*7^(L-2),
       S = 7L-4.

   Divisibility by 7 implies 10^i = -1 modulo 7, hence i = 3 modulo 6. In
   particular i >= 3, L >= 5 and i is odd.

These steps are elementary all-length arguments, not conclusions from the
finite Stage 5 search.

## Additional necessary congruences

- The final three digits are 775, so v_5(n)=2. Thus 5 does not divide S,
  equivalently L is not 2 modulo 5.
- Because L and i are odd, the numerator above is -14 modulo 11; division by
  9 gives n = 7 modulo 11. Thus L is not 10 modulo 11.
- The order of 10 modulo 13 is 6. Since i=3 modulo 6, 10^i=-1 modulo 13;
  the numerator becomes 7(10^L-1). Odd L is not divisible by 6, so 13 does
  not divide n. Thus L is not 8 modulo 13.
- Since L>=5, divisibility by 49 is necessary. Put i=3+6a. As 10^6=8 modulo
  49, 10^i=20+42a modulo 49. The numerator is therefore
  7(10^L+1-3a) modulo 49. This gives the following necessary restrictions:

  | L modulo 6 | i modulo 42 |
  |---:|---:|
  | 1 | 39 |
  | 3 | 3 |
  | 5 | 15 |

  In particular, 7 does not divide i.

## Exact remaining problem

For odd L>=5 and 3<=i<L with i=3 modulo 6, define

    F(L,i) = 7*10^L - 18*10^i - 25.

The integer represented has precisely the required two fives and all other
digits seven. It satisfies the full A398769 condition if and only if

    225 * 7^(L-2) * (7L-4) divides F(L,i).

A sufficient stronger route would prove v_7(F(L,i)) < L-2 throughout this
family. No such all-length bound was proved here. The congruences above are
necessary conditions only and cannot be treated as a settlement.

## Why one fixed power of seven cannot close the argument

Fix i=3. Then

    n = 7(10^L - 2575)/9.

The order of 10 modulo 7 is 6 and v_7(10^6-1)=1. Hence its order modulo 7^k
is 6*7^(k-1), the full size of the unit group. Every unit modulo 7^k,
including 2575, is a power of 10. The resulting exponent L is 3 modulo 6,
since 2575=-1 modulo 7. Thus for each fixed k there are arbitrarily large
odd L>3 for which 7^(k+1) divides n. They are legitimate two-five decimal
strings.

This does not make them counterexamples: the required exponent is L-2,
which grows with L, and the factor 7L-4 must also divide appropriately.
It does show why a fixed-modulus obstruction, or a uniformly bounded
7-adic valuation claim, cannot prove this remaining family empty.

## Formal proof status and reproduction

[FiveSeven.lean](FiveSeven.lean) proves `A398769.FiveSeven.atMostTwoFives`,
`notExactlyOneFiveWithSeven`, and the stronger `notExactlyOneFive`, using the
actual `Nat.digits 10 n`. The first requires `n > 0`; the latter excludes one
five without requiring a separate occurrence of seven. All three use only
`[propext, Classical.choice, Quot.sound]`; see [axioms.txt](axioms.txt).
These Lean results leave zero or two fives. The exclusion of zero fives and
the positional/algebraic reductions above are [independently reviewed](REVIEW.md) ordinary
mathematical proofs; they are not yet formalized in this file.

This local follow-up is separate from the clean Stage 5 branch and
[PR #6](https://github.com/lukeroyle-beep/Mathematics/pull/6), at commit
`da3c28701e44b30b801ffd27a13a88f83472ebf3`. It has not been published as a new
pull request. From the Stage 5 checkout, with the pinned toolchain on PATH:

```sh
lake env lean ../five-seven-follow-up/FiveSeven.lean
```

See [verification.json](verification.json) for the source hash and actual
elaboration result. There is no `sorry`, custom axiom or `native_decide`.

## Source check

The current [OEIS entry](https://oeis.org/A398769/internal) still states the
full conjecture. The [earlier Omega Institute attempt](https://github.com/the-omega-institute/trureturing/issues/26444#issuecomment-6629067008)
reports an all-length exclusion for complete repetitions of a shorter block,
with the general primitive-word case left unresolved. Neither establishes
the two-five exclusion required here. Targeted searches did not locate a
proof of this exact subclass; that limited search does not establish absence
of prior work. The reductions in this note were checked directly.
