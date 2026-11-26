# All-length exclusion of small seven-free quotients

26 November 2026. **No full {5,7} witness has q0<=L^35 at any length**,
where `q=n/(digit product * digit sum)` is the exact integer quotient
of a full witness and `q0=q/7^v7(q)`. There is no position restriction.
Both proposed deductions pass an independent primary-source audit:

```
L>B => ln(9*(7L-4)*q0)>L/10^9,
q0>exp(L/10^9)/(9*(7L-4))>L^35,
B=1,000,002,000,000.
```

The [proof](PROOF.md) uses the exact five-adic valuation forced by the
decimal word and Bugeaud--Laurent Corollary 1. Combined with the
inherited interval through B, it closes this quotient subfamily at
every length, including positions outside PR #25's rational-centre bands.
It removes the enormous unchecked finite remainder in PR #24's cutoff
for this subfamily. It does not bound q0 above for arbitrary witnesses.

The **whole-length endpoint remains 1,000,002,000,000 inclusive**.
The **unrestricted {5,7} subclass remains open**. The **wider A398769
digit-1 conjecture remains open**; even a complete {5,7} exclusion would
leave other digit families. A full {5,7} witness would refute that conjecture.
No full witness was found. No new Lean formalization or build was performed.

## Baseline and inherited evidence

Freshly fetched main was exactly the requested PR #25 merge,
`0e4dbdf9244c6b7f743d7e90ce04c91ea3d38675`. Work uses a separate
checkout and branch `research/a398769-five-adic-quotient`.
[baseline.json](baseline.json) records base identity, primary source and
inherited artifact hashes. The existing proofs and historical receipts
remain unchanged. The earlier whole-length arithmetic and PR #25's
large searches are inherited, not rerun in this task. Their retained
receipt bindings are checked separately from the fresh arithmetic here.

The principal inherited inputs are [rational-centres](../rational-centres/README.md),
[proportional](../proportional/README.md),
[ROUTE1](../explicit-length/ROUTE1.md),
[ROUTE2](../explicit-length/ROUTE2.md), and
[SOURCES](../uniform-bound/SOURCES.md). The strict units-end bound is
re-audited in the new proof and its constants independently recalculated.

## Remaining obstruction

[OBSTRUCTION.md](OBSTRUCTION.md) compares the lower bound with
`A<(343/25)*(10/7)^L`. The logarithmic interval still has width
`ln(343/25)+(ln(10/7)-10^-9)*L`, whose linear coefficient exceeds
0.3566749429. At the first length above B its width is between
356,675,656,291 and 356,675,656,292.

The exact digit-sum condition and the complement of the certified centres
have not supplied a contradictory upper bound or a proof that an actual
sum-compatible position must escape its lifts by index L-3. A first
change at L-2 is too late. The new lower quotient bound is the advance;
no global cutoff or universal escape theorem is claimed.

## Fresh validation and reproduction

Only Python 3's standard library is required. From the repository root:

```sh
fq=research/a398769/five-seven/five-adic-quotient
python3 "$fq/checks.py" > /tmp/five-adic-checks.json
python3 -O "$fq/checks.py" > /tmp/five-adic-checks-O.json
cmp /tmp/five-adic-checks.json /tmp/five-adic-checks-O.json
cmp /tmp/five-adic-checks.json "$fq/checks.json"
python3 "$fq/independent_checks.py" > /tmp/five-adic-independent.json
python3 -O "$fq/independent_checks.py" > /tmp/five-adic-independent-O.json
cmp /tmp/five-adic-independent.json /tmp/five-adic-independent-O.json
cmp /tmp/five-adic-independent.json "$fq/independent-checks.json"
python3 "$fq/obstruction_checks.py" > /tmp/five-adic-obstruction.json
python3 -O "$fq/obstruction_checks.py" > /tmp/five-adic-obstruction-O.json
cmp /tmp/five-adic-obstruction.json /tmp/five-adic-obstruction-O.json
cmp /tmp/five-adic-obstruction.json "$fq/obstruction-checks.json"
python3 "$fq/verify.py"
python3 -O "$fq/verify.py"
git diff --check
```

The primary constants use a rational atanh series with a bounded tail;
the independent checker uses rational exponential series. Literal decimal
words exercise exact identities, the full original divisor, nonzero sum
passes including `3|S`, and factor-nine negatives. Their seven-free
cofactor is labelled C; it is not called `9S*q0` for nonwitnesses.
The sparse obstruction checks demonstrate sum/centre-complement
compatibility without pretending their low valuations satisfy `i=r_K`.
All checks use explicit exceptions and remain active under `python3 -O`.

[verification.json](verification.json) binds the checks and reproduction
results. [REVIEW.md](REVIEW.md) records fresh independent mathematical
and computational review and the reviewed revision. This is a separate
draft pull request; merging remains Luke's decision.
