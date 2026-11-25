# Bounded representative experiment

This is a diagnostic of the proposed high-depth route, wholly inside the
inherited exclusion interval. It is **not** a new global bound, a witness,
or an extension of consecutive coverage. No unchanged ten-million search
was rerun for this experiment.

## Questions and exact method

The stated question is whether passing the full digit sum distinguishes
actual least representatives after their seven-adic period exceeds the
length, and how long zero lifts can occur without that sum condition.

[checks.py](checks.py) computes the least positive K with
`T_K=6*7^(K-1)>L`, using integers only. Starting with `r_1=3`, it computes
one lift at a time. At depth k put `m=7^k`, `T=6*7^(k-1)`,

```
c=(10^T mod 7m - 1)/m,
y=18*(10^r mod 7m),
b=7*(10^L mod 7m)-25.
a_k=((b-y)/m)*(y*c)^(-1) mod 7.
```

Every division is checked exact; the inverse is of a unit. The program
checks both incoming and outgoing congruences. The next least
representative is `r+a_k*T`. Exact-order checks at depths 1 through 13
verify the period and its prime-divisor reductions; these finite controls
support implementation, not the all-k order proof.

For every odd `5<=L<=100001`, it computes `r_K`. If `3<=r_K<L`, it
computes the full `F mod(9S)`, and finds the first nonzero residue modulo
`7^(d+1)`. Together with divisibility by `7^d`, this proves exact depth d.
It verifies all lifts from K through d-1 have digit zero, and the next
lift has a nonzero digit and a representative at least L. A resource guard
at depth 64 fails the program if exhausted; it cannot produce an exclusion.

## Coverage and result

The 49,999 odd lengths are exactly `5,7,...,100001`, with no residue filter
on L. All actual representatives are examined, including those with
`5|S`; that case remains excluded by the inherited decimal suffix argument.

| Category | Count |
|---|---:|
| `r_K` outside `3<=i<L` | 21,628 |
| Actual `r_K`, `5|S` | 5,658 |
| Actual `r_K`, `5` does not divide S, fails `9S|F` | 22,713 |
| Actual `r_K`, `5` does not divide S, passes `9S|F` | 0 |

These counts partition all 49,999 lengths. Counts by K are respectively
1, 18, 126, 882, 6,174, and 42,798 for K=1,...,6.
No full-sum positive control at depth K was found in this declared window;
no enlargement was made to seek one. This does **not** imply that no such
representative occurs above this window, or above ten million.

For all actual representatives, the zero-run histogram is

| Zero lifts after K | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Count | 24,334 | 3,450 | 500 | 73 | 10 | 3 | 1 |

In particular `(L,i)=(97127,89265)` has K=6 and exact depth 12. Its six
zero lift digits are followed by `a_12=2`, sending the representative to
23,728,010,181. The nonzero next residue is 83,047,723,206 modulo `7^13`.
Here `5|S`, so this is a broader arithmetic control outside the residual
five-free sum domain; it also fails the full sum, `F mod(9S)=815265`.

Inside `5` not dividing S, the longest run in the same window is
`(L,i)=(69489,40323)`, with S=486419, K=6 and exact depth 11. Its five
zero lifts are followed by `a_11=4`, sending the representative to
6,779,446,299; `F mod(7^12)=9886633715` proves the exact depth. It too
fails the full sum, with `F mod(9S)=2218743`.

These are positive controls for the lifting implementation and show that
a bounded actual representative alone does not force the next lift digit
nonzero. They say nothing about a universal bound on zero runs and are
not full-sum survivors.

The receipt hashes one ordered ASCII line for **every** length:

```
L:K:r_K:T_K:depth:F_mod_9S\n
```

The last two fields are `-` outside the actual interval. Its SHA-256 is
`a54ad76ea69a6db88927613cfab5da3db41189fbeb5b7b81ebbef6d62247eab7`.
This digest is reproducibility evidence for the specified run, not an
independent proof of its coverage.

## Regressions and boundaries

Literal decimal construction covers all 9,900 pairs at odd lengths
5 through 201 and **all** positions `3<=i<L`, including both parities.
It checks `9n=F`, actual product and sum, the exact full-divisor condition,
and the separated test when `5` does not divide S. It compares 39,598
small-depth congruences with literal words and checks the sole depth-K
representative at each length. Seventy-four pairs pass the full sum.

* `(L,i)=(13,12)`, S=87, passes `9S|F` and tests a positive full-sum case
  with `3|S`. It need not pass the seven-adic witness condition.
* `(L,i)=(151,8)`, S=1053, has `F mod S=0` but `F mod(9S)=8424`.
  It detects the incorrect loss of the extra nine. Its even position is
  intentional: the full-sum test is defined before imposing depth.
* At each `T_k` for k=1,...,8, K is checked at `T_k-1`, `T_k`, and
  `T_k+1`. The strict inequality changes K at equality, including when
  the boundary length is even. In particular K(5)=1.
* For all 79 coprime sums at odd lengths 5 through 201, an independently
  iterated order `d=ord_S(10)` satisfies `v_7(d)<K`. The largest seven part
  in these controls is `v_7(d)=2`; `(L,S,d,K)=(85,591,98,3)` is one control.
  These finite checks support the separate ordinary saturation lemma;
  they do not prove it for arbitrary L. Separate exact order controls
  `(L,S,d,e,K)=(13,87,28,1,2),(85,591,98,2,3),(589,4119,686,3,4)`
  attain `e=K-1`; they are not full-sum survivors at depth K.

All essential checks use explicit exceptions. Normal Python and
`python3 -O` produce byte-identical output. The source SHA-256 is embedded
in [checks.json](checks.json).

## Reproduction

From the repository root:

```sh
python3 research/a398769/five-seven/high-depth/checks.py > /tmp/high-depth-checks.json
python3 -O research/a398769/five-seven/high-depth/checks.py > /tmp/high-depth-checks-optimized.json
cmp /tmp/high-depth-checks.json /tmp/high-depth-checks-optimized.json
cmp /tmp/high-depth-checks.json research/a398769/five-seven/high-depth/checks.json
```

The independent implementation and review are indexed by this directory's
README. No statement here depends on treating finite diagnostics as an
all-length theorem. No Lean code was added or validated by this computation.
