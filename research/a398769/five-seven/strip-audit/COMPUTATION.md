# Exhaustive modular certificate for the exact line

**Verdict: the modular certificate and all five submitted numerical values
are verified.** Two standalone standard-library Python implementations
discover the same sole exponent class. Neither starts with the submitted
representative, root, or a previously computed lift. Each compares its
completed discovery against the submitted values only afterward.

## Algebra and the required modulus

The integer equation `12i-5L=-1` first gives `L=5 (mod 12)` and hence

```
L=12u+5, i=5u+2, S=84u+31.
```

`L>=5` gives `u>=0`, and `i>=3` rules out `u=0`; conversely every integer
`u>=1` gives odd `L>=17`, `i>=7`, and `L-i=7u+3>0`. Thus this is exactly
the admissible line, including both parities of the position. Substitution
in the original expression gives the integer identity

```
F/25 = (7*10^5/25)*(10^u)^12 - (18*10^2/25)*(10^u)^5 - 1
     = P(10^u),
P(X) = 28000X^12 - 72X^5 - 1.
```

A full witness requires `7^(L-2)|F`; here `L-2>=15>=10`. Since 25 is a
unit modulo seven, the necessary condition `7^10|P(10^u)` follows.
No assumption about `9S|F` or a Fermat test is used in this certificate.

## First computation: all polynomial roots and an independent discrete log

[modular_roots.py](modular_roots.py) evaluates P at **all seven** residues
modulo seven. The root list is `[5]`. Algebraically,
`P(X)=-2X^5-1 (mod 7)`, zero is not a root, and in the group of order six
`X^5=X^(-1)`; the equation forces `X=5`. Its derivative is

```
P'(X)=336000X^11-360X^4,   P'(5)=1 (mod 7).
```

Hensel's simple-root lemma gives exactly one root modulo each successive
power of seven. Every root at a higher power must reduce to a lower root,
so this proves exhaustiveness, including exclusion of other root branches.
The checker explicitly tries all seven lifts of every retained root at
each stage and checks uniqueness and the derivative again.

The powers of ten modulo seven for exponents 0 through 5 are
`[1,3,2,6,4,5]`; consequently the order is exactly six. Also
`10^6-1=7*142857`, with `142857=1 (mod 7)`. Thus

```
v_7(10^6-1)=1,
v_7(10^(6m)-1)=1+v_7(m)   (m>=1),
ord_(7^k)(10)=6*7^(k-1).
```

The middle equality is odd-prime LTE. Conversely any exponent giving one
modulo `7^k` is divisible by six already modulo seven, so the equality
proves the minimal order, not just an upper bound. This order is the full
unit-group size, so every unit, in particular the unique root, has exactly
one exponent class. At every computed depth the program also checks the
period power and each quotient of the proposed order by its distinct
prime divisors (2, 3, and, when present, 7); none of those quotient powers
is one. Those exact tests separately certify the minimal order.

An exhaustive baby-step/giant-step search then recovers the discrete log
of the final root, using block width 15,561. It enumerates every possible
block of `[0,242121642)` and retains all matches, rather than stopping at
the first match. The relation `u=a*15561+b` for `0<=b<15561` proves its
coverage. It returns the singleton `[185987897]`. This discrete-log route
does not lift exponents or import the other checker.

## Second computation: all exponent classes, original F only

[modular_exponents.py](modular_exponents.py) does not construct or evaluate
P. It starts with **all six** exponents `0,1,2,3,4,5` and evaluates

```
(7*pow(10,12*u+5,7^k) - 18*pow(10,5*u+2,7^k) - 25) mod 7^k.
```

It discovers the order modulo seven by trying exponents 1 through 6.
At each next depth it independently tries all multipliers 1 through 7 of
the old order and chooses the first giving one. This is exhaustive:
the new order is a multiple of the old order by reduction; the binomial
theorem shows that seven times the old order is a period at the next
depth. Each observed growth factor is seven.

If `T_k=ord_(7^k)(10)`, the original F expression is periodic in u with
period `T_k`. Every class modulo `T_(k+1)=7T_k` above a surviving class u
is exactly `u+d*T_k`, `0<=d<7`. A solution at the next depth must survive
the previous depth. The checker tests **all** these lifts, saving every
candidate and its original-F residue. Induction from the complete six
initial classes therefore proves completeness. No representative from the
polynomial computation is shared or used as a seed.

Both independent lift histories are:

| k | 7^k | Unique P root | Order of ten | Sole u class |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 7 | 5 | 6 | 5 |
| 2 | 49 | 26 | 42 | 11 |
| 3 | 343 | 271 | 294 | 263 |
| 4 | 2401 | 1643 | 2058 | 263 |
| 5 | 16807 | 4044 | 14406 | 6437 |
| 6 | 117649 | 4044 | 100842 | 35249 |
| 7 | 823543 | 356991 | 705894 | 337775 |
| 8 | 5764801 | 356991 | 4941258 | 3161351 |
| 9 | 40353607 | 11886593 | 34588806 | 13043867 |
| 10 | 282475249 | 213654628 | 242121642 | 185987897 |

Consequently the congruence is equivalent to

```
u = 185987897 (mod 242121642).
10^185987897 = 213654628 (mod 282475249).
```

The reported representative is positive, while subtracting the period
gives a negative integer. It is therefore the least positive u satisfying
this necessary congruence, and the least possible corresponding length is

```
L = 12*185987897+5 = 2231854769.
```

This is the first length **permitted by this modulus**, not a witness.
Indeed the original F at that representative has residue `282475249`
modulo `7^11`, so its exact seven-adic valuation is ten, far below `L-2`.
The modulus alone excludes every admissible line position with
`17<=L<2231854769`, and hence all such positions with `L<10^9`.

The complete lower-depth table also gives a bounded stronger consequence.
For each `k=2..10`, its least positive class `u_k` has
`12u_k+5>T_k`. If `K(L)=k`, then `L<T_k`, so the line position fails
depth k and has `v_7(F)<K(L)`. At lengths from `T_10` up to (but not
including) 2231854769, `K(L)>=11` and the depth-ten failure suffices.
Thus every admissible line position with `L<2231854769` satisfies the
conclusion of (E), without a sum hypothesis. The aggregate verifier
checks the nine finite comparisons. This remains a bounded position
statement and adds no whole-length or broad all-position (E) interval.

## Reproduction and controls

From the repository root, with standard-library CPython (observed version
3.14.4 on Darwin arm64):

```sh
python3 research/a398769/five-seven/strip-audit/modular_roots.py > /tmp/a398769-strip-roots.json
python3 -O research/a398769/five-seven/strip-audit/modular_roots.py > /tmp/a398769-strip-roots-O.json
cmp /tmp/a398769-strip-roots.json /tmp/a398769-strip-roots-O.json
cmp /tmp/a398769-strip-roots.json research/a398769/five-seven/strip-audit/modular_roots.json
python3 research/a398769/five-seven/strip-audit/modular_exponents.py > /tmp/a398769-strip-exponents.json
python3 -O research/a398769/five-seven/strip-audit/modular_exponents.py > /tmp/a398769-strip-exponents-O.json
cmp /tmp/a398769-strip-exponents.json /tmp/a398769-strip-exponents-O.json
cmp /tmp/a398769-strip-exponents.json research/a398769/five-seven/strip-audit/modular_exponents.json
```

All runs and comparisons pass; the two `observed` result objects also
agree exactly. Receipts record each checker's SHA-256. There are no
`assert` statements or optional dependencies. Essential failures raise
explicit exceptions, and intentional negative guard controls confirm that
the failures execute in both ordinary and optimized modes.

The controls are nonvacuous: `u=5` has exact depth one, with original
`F mod49=7`; the final representative has exact depth ten as above; adding
one to it fails the modulus with residue `187638593`; adding the full
period passes the modulus. Perturbing the recovered polynomial root by
one gives residue `114585479`, and `P(0)=-1`. These distinguish actual
positive depth, exact depth, true periodicity, and rejection. No check
constructs enormous decimal powers at the final representative.

The computations certify the finite modular statement. The independent
valuation argument and their combined all-length consequence are recorded
in [PROOF.md](PROOF.md); no modular residue is treated as a full witness.
