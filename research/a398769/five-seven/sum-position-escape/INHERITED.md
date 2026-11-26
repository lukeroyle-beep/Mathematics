# Inherited evidence and baseline audit

The starting `main` is **`9d958f86fc81188de68af97909614e23a186df9f`**,
the merge of PR #26. A fresh isolated clone supplied this commit; Git
ancestry confirms the requested merge is included. The remote tracking
`origin/main` and initial `HEAD` both name it, and there are no later main
commits at the initial fetch. Work branches from that commit. No tracked
`AGENTS.md` exists in this checkout. Publication-time remote state must be
reported separately if it changes.

[`baseline-inputs.json`](baseline-inputs.json) binds **706 existing files**
by repository-relative path and SHA-256. Every bound file was also compared
with the corresponding `git show <starting_main>:<path>` blob. This binds
all five requested starting texts, the relevant quotient and coverage
manifests and their referenced files, and the inherited `a=25` control.
It does not modify or regenerate any inherited evidence.

Seven inherited manifest maps contain **712 references** in total,
including duplicates. All except one match current bytes. The exception is
the old rational-centres manifest's root README: PR #26 subsequently added
its navigation entry. That older hash was verified against the actual
README blob at PR #25 merge `0e4dbdf9244c6b7f743d7e90ce04c91ea3d38675`;
its binding and reason are explicit in `historical_bindings`. The current
root README matches the PR #26 manifest. No mathematical source or receipt
exception is concealed by this historical documentation change.

## Consecutive whole-length coverage

The inherited, documented complete exclusion is **every length from 1
through B=1,000,002,000,000 inclusive** for the `{5,7}` subclass. It has two
adjacent components:

| Inclusive lengths | Repository evidence | Inherited arithmetic |
|---|---|---|
| 1–1,000,000,000,000 | [`prime-sum/ARCHIVE_AUDIT.md`](../prime-sum/ARCHIVE_AUDIT.md), [`prime-sum/verification.json`](../prime-sum/verification.json) | Both complete archived enumerators were independently rerun in PR #22; their 74,601 depth-22 pairs agree. An independent original-decimal checker gives maximum exact valuation 27; 182 literal words cover the short residual lengths. |
| 1,000,000,000,001–1,000,002,000,000 | [`trillion-witness/verification.json`](../trillion-witness/verification.json), [`independent/contiguous_stream.json`](../trillion-witness/independent/contiguous_stream.json) | PR #21 scanned all 1,000,000 odd lengths, ending at 1,000,001,999,999; its independent stream checker checked every representative and original-digit arithmetic for every actual position. The inherited parity reduction covers the even lengths, including B. |

PR #21 itself reported the earlier archive unavailable. That historical
gap was resolved by the later merged PR #22: the actual archive is now
retained at [`prime-sum/evidence/trillion-evidence.zip`](../prime-sum/evidence/trillion-evidence.zip),
SHA-256 `b657f158d6362c77c570b87c3c193fe54c6f3c385889379edf5bf79b71f05c0a`.
The raw enumeration commands, successful exit codes and output identities
are recorded in [`enumeration-runs.json`](../prime-sum/evidence/enumeration-runs.json).
Thus the current union is consecutive; an outdated statement about the
missing archive must not be used to remove the subsequently established
coverage.

The fresh audit here checks **19 prime-sum and 35 trillion-witness artifact
bindings**. It does **not** rerun the trillion enumerators, the million odd
length scan, its million-row arithmetic stream verification, or the 74,601
archive candidate computations. Their coverage and arithmetic remain
inherited evidence, not fresh searches in this task. Hashes establish
identity and preservation, not a replacement proof of enumeration
completeness.

## Quotient and position results inherited above B

The PR #26 proof gives, for a hypothetical full witness at one actual
position with `L>B`,

```
q=n/(PS), q0=q/7^v7(q), A=9S*q0,
ln(A)>L/10^9,
q0>exp(L/10^9)/(9S)>L^35.
```

The assertion is a necessary lower bound on the seven-free quotient. It
does not prove that all possible quotients are smaller, nor exclude an
unrestricted witness. The inherited all-length exclusion applies to the
subfamily `q0<=L^35`. The exact full divisor remains
`225S*7^(L-2)|F`, with `9S|F` at the same position, including `3|S`.

PR #25 excludes the reduced rational-centre subfamily
`0<a<b<=K^2`, `|bi-aL|<=K^2` at every length. Its retained **602 receipts**
represent 301 partitions per independently implemented engine, including
one control partition. The current audit reruns the deterministic receipt
validation and exact line counts, but not the historical full partition
enumerations. This is a position-restricted result; it does not extend the
consecutive whole-length endpoint.

The required initial texts agree on the remaining issue: increasing joint
spacing gives at most one actual position, while stabilized CRT
compatibility concerns unrestricted exponents. Neither supplies the
missing bound on the least bounded representative by depth `L-2`. The
first nonzero lift digit must occur by index `L-3`; index `L-2` is too late.

## Prior pure-power family control and fresh verification scope

The known pure-power control is inherited from
[`global/independent.json`](../global/independent.json):

```
a=25, S=3^25=847288609443,
L=121041229921, i=40582608819,
n mod S=0, n mod49=0, n mod343=294.
```

Hence it passes the complete digit-sum condition and has exact `t=2`.
It is not a witness. The general consecutive interval already excludes
this length and all admissible pure-power lengths with `a<=25`. No
previous result for a different `c*3^a` family is credited as coverage of
the new 128 specified pure-power lengths.

The following commands were freshly run and returned PASS in this task:

```sh
python3 research/a398769/five-seven/five-adic-quotient/verify.py
python3 -O research/a398769/five-seven/five-adic-quotient/verify.py
```

Each invocation checks the inherited coverage bindings and rational-centre
receipts, and freshly reproduces all three PR #26 arithmetic checkers both
normally and with `-O`, comparing their retained outputs byte for byte.
These are the small quotient, decimal and obstruction control suites;
the commands do not launch the historical large searches. The first run
and optimized run printed identical PASS summaries.

All new pure-power arithmetic and its exact finite scope are reported in
this directory's own receipts. No new Lean theorem, formalization or
Lean build was performed in this audit. The unrestricted `{5,7}` status
and the wider A398769 digit-1 conjecture remain open unless independently
settled by new evidence; none of the inherited statements alone settles
them.
