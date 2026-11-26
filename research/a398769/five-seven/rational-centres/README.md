# All-length exclusion of the reduced K²-centre subfamily

26 November 2026. **No full witness in the residual two-five family admits
any reduced `0<a<b<=K(L)^2` with `|bi-aL|<=K(L)^2`, at any length.**
This follows from the audited analytic reduction, two fresh exhaustive
enumerations of all three remaining bands, and a fresh reproduction of
the original b=289 control. No full witness was found.

The whole-length endpoint remains **B=1,000,002,000,000 inclusive**.
This is a position-restricted all-length result: no theorem puts every
residual position into these rational-centre bands. The unrestricted
`{5,7}` subclass and the wider digit-1 conjecture remain open. The work
consists of ordinary proofs and exact computations; no new Lean
formalization or Lean build was performed.

## Baseline and exact predicate

Freshly fetched main was `81dce203b1eecc61ec9fda36bc812095e2c89724`,
exactly the final merge of PR #24. Git ancestry confirms it includes the
integration commit `d56df00ef26e24b0e3f1c7e2200b9885adf949e6`.
There were no later commits on main at the start. Work uses a separate
clone and branch, `research/a398769-rational-centre-bands`.
[baseline.json](baseline.json) records these identities and inherited
source hashes. The named reduced-centres audit ZIP was unavailable in the
workspace and Downloads; its claims were reconstructed and tested, with
no credit assigned to unmerged evidence or the earlier 43-centre sample.

For odd L, `3<=i<L`, fives occupy decimal positions 0 and i from the
units digit, and all other digits are seven. Define

```
S=7L-4, F=7*10^L-18*10^i-25, n=F/9,
P=25*7^(L-2), K=min{k>=1:6*7^(k-1)>L}.
```

The full witness predicate is `P*S|n`, equivalently
**`225*S*7^(L-2)|F`**. Both programs preserve the full factor nine in
`9S|F`, including when `3|S`, and all conditions refer to the same
actual `(L,i)`. Necessary conditions are `i=3 mod6`, `5∤S`, and
`7^(L-2)|F`. Since `L-2>22` throughout the fresh search, failure at
depth 22 excludes a full witness.

## Fresh exhaustive results

Every endpoint below is inclusive. Lengths are odd. Counts of actual pairs
retain `(a,h)` labels, where `h=bi-aL`; overlaps between different centres
are not removed and are not presented as distinct unlabelled pairs.

| K | b | Odd length interval | Partitions | Raw lines | Compatible lines | Actual pairs at depth >=13 | With 5∤S | Exact digit-sum passes | Pairs at depth >=22 |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
|15|102–225|1,000,002,000,001–4,069,338,437,093|124|5,540,084|2,314,738|627,952|502,186|0|0|
|16|143–256|4,069,338,437,095–28,485,369,059,657|114|7,072,218|2,945,860|5,224,597|4,180,553|0|0|
|17|227–288|28,485,369,059,659–78,999,999,999,999|62|5,624,406|2,343,851|6,665,416|5,333,261|0|0|
|17 control|289|28,485,369,059,659–199,397,583,417,605|1|157,488|61,180|562,262|449,824|0|0|

The three bands contain exactly **300 partitions, 18,236,708 labelled
lines and 7,604,449 compatible lines** before further pruning. All
supplied counts were recomputed independently. Each reduced numerator
uses every integer h in `[-K²,K²]`, including zero and both endpoints.
The separate original control has exactly 272 reduced numerators and
matches every supplied count. Its depth-13 stream SHA-256 is
`c004ba62c00d37dd59ecd56318a349c16a26ce9a9c0878f5492c5dcd3bbf8928`.

All 301 denominator receipts agree between the two implementations on
counts and deterministic hashes of the complete actual-pair streams.
The ordered partition/pair-digest manifest has SHA-256
`acc8b323b03462dba377b4c3606ad48c2ae900419706c781aa22c8f3c731dda9`.
Every depth-22 stream is empty. **There are no unresolved survivors and
no outstanding search partitions.**

## Why this covers all lengths in the stated subfamily

[ANALYTIC.md](ANALYTIC.md) proves the nearest-rounding span bound,
checks the polynomial/root change when q increases, and applies the
actual-degree Bugeaud–Laurent Theorem 4 entry `(15,10,18)`. It retains
the singular derivative cases, multiplicative independence, height
floors and every logarithm branch. All six requested endpoint rows pass
exact rational checks using the first 91 exponential-series terms.
The endpoint comparison propagates to all allowed denominators and
all later lengths in its K-band; the degree-dependent branch is handled
separately.

Inherited certificates close `L<=B` and the entire `b<=4K` subfamily.
The inherited polynomial-versus-exponential induction closes `K>=20`.
The new endpoint rows close K=18 and K=19 entirely, and remove the
stated initial denominators for K=15,16,17. The K=17,c=289 row closes
all its denominators above 79 trillion. The original b=289 control and
the three fresh finite enumerations close precisely what remains.

[SEARCH.md](SEARCH.md) proves periodic coverage, the two independent
line parameterizations, all-child singular lifting, bounded actual-pair
expansion and the exact sum arithmetic. The primary continues bounded
lifts to depth 22; the independent implementation expands at depth 13
and directly checks each actual pair modulo `7^22`. Independent decimal
arithmetic and nonzero controls check both engines. Source-bound compact
receipts are in [receipts/primary](receipts/primary) and
[receipts/independent](receipts/independent).

The old whole-length certificates and earlier analytic theorems are
**inherited** and hash-bound, not newly rerun in full. The six-row audit,
all 602 denominator computations, all new controls and the receipt
comparisons are **fresh**. No sample is promoted to whole-denominator
coverage, and no finite zero digit-sum count is made into an unrestricted
fixed-depth theorem.

## Reproduce and resume

Requirements: Python 3 (standard library) and a C++17 compiler supporting
unsigned 128-bit arithmetic. This run used Python 3.14.4 and Apple clang
21.0.0. From the repository root, verify all retained evidence:

```sh
rc=research/a398769/five-seven/rational-centres
python3 "$rc/analytic_checks.py" > /tmp/centres-analytic.json
python3 -O "$rc/analytic_checks.py" > /tmp/centres-analytic-O.json
cmp /tmp/centres-analytic.json /tmp/centres-analytic-O.json
cmp /tmp/centres-analytic.json "$rc/analytic-checks.json"
python3 "$rc/controls.py" > /tmp/centres-controls.json
python3 -O "$rc/controls.py" > /tmp/centres-controls-O.json
cmp /tmp/centres-controls.json /tmp/centres-controls-O.json
cmp /tmp/centres-controls.json "$rc/controls.json"
c++ -O3 -std=c++17 "$rc/independent.cpp" -o /tmp/centres-independent
python3 "$rc/independent_controls.py" --binary /tmp/centres-independent > /tmp/centres-independent-controls.json
python3 -O "$rc/independent_controls.py" --binary /tmp/centres-independent > /tmp/centres-independent-controls-O.json
cmp /tmp/centres-independent-controls.json /tmp/centres-independent-controls-O.json
cmp /tmp/centres-independent-controls.json "$rc/independent-controls.json"
python3 "$rc/verify.py" > /tmp/centres-verification.json
python3 -O "$rc/verify.py" > /tmp/centres-verification-O.json
cmp /tmp/centres-verification.json /tmp/centres-verification-O.json
cmp /tmp/centres-verification.json "$rc/verification.json"
```

For **fresh full arithmetic**, use empty output directories. These same
commands resume safely after interruption, reusing only complete receipts
with matching source and bounds. The two output trees are independent.

```sh
rc=research/a398769/five-seven/rational-centres
repro=$(mktemp -d)
python3 "$rc/run_primary.py" --jobs 2 --output "$repro/primary"
python3 "$rc/independent_runner.py" --output "$repro/independent"
python3 - "$rc" "$repro" <<'PY'
import importlib.util, pathlib, sys
source, result = map(pathlib.Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location('centres_verify', source/'verify.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
bands, control, digest = module.audit(result/'primary', result/'independent')
print('PASS', bands, control, digest)
PY
```

To resume the retained output location, use `python3 "$rc/run_primary.py"`
and `python3 "$rc/independent_runner.py"`; already complete partitions are
checked and skipped. `--verify-only` on the independent runner validates
its receipts without running its arithmetic engine. Stale source bindings,
wrong bounds or missing/extra partitions are errors, not silent exclusions.

The independent mathematical and computational review, including exact
revision bindings and disposition of findings, is recorded in
[REVIEW.md](REVIEW.md). This work is offered in a separate draft PR;
merging remains Luke's decision.
