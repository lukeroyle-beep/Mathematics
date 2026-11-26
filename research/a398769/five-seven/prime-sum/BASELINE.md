# Source baseline and evidence boundaries

The task began in an isolated clone under `prime-sum-audit`; existing
Mathematics checkouts were preserved. No applicable `AGENTS.md` was found.
Current main was fetched from the explicitly requested repository on
26 November 2026:

```
origin: https://github.com/lukeroyle-beep/Mathematics.git
starting main: b991c97a3d3e91b8339e25c8932ae8072f8c4a09
PR #21 merge: b991c97a3d3e91b8339e25c8932ae8072f8c4a09
PR #21 head: 3ba607050ae72b1ad87f907b3ff1d507659aebf7
```

`git merge-base --is-ancestor b991c97a3d3e91b8339e25c8932ae8072f8c4a09 HEAD`
succeeded at setup. The GitHub PR metadata independently confirmed the
closed, merged PR and its exact merge SHA. The required trillion-witness
report and `STRUCTURE.md`, `effective/QUALITATIVE.md`, and
`uniform-bound/{LIFTS,ANALYTIC}.md` were read. The supplied Space root,
handoff and archive recovery page were read through their connected tools.
The exact recovered archive and report are retained here. No attached
Mathematics-Codex-Pack was used; its older snapshot did not replace main.

| Result | Provenance in this audit |
| --- | --- |
| Whole lengths 1–10,000,000 | Inherited repository baseline; not rerun here |
| Whole lengths 1–10^12 | Recovered archive identity, proof/code completeness audit, both full enumerations freshly run, new independent decimal verifier |
| `10^12<L<=1,000,002,000,000` | Inherited PR #21 complete adjacent interval; all 35 artifact bindings checked, arithmetic scan not rerun |
| PR #21 sampled bands / 32 family lengths | Retained historical exclusions, not newly searched |
| Reported broad `(E)` through odd 1,694,851,493 | Archive present, but that separate search and proof not re-audited; not claimed newly certified |
| All-length prime-sum exclusions | New independent ordinary proofs, finite-field controls and fresh review |
| All-length signed power saving | New explicit proof, independent constants review and finite controls; insufficient exponent |
| All-length `{5,7}` exclusion or verified witness | Neither established |

The old PR #21 statements that the archive was unavailable remain accurate
as history. This audit resolves that evidence gap without rewriting old
receipts. Connecting the two certified finite intervals now gives the
documented consecutive endpoint 1,000,002,000,000. It does not certify any
additional length beyond the union of those intervals.

No Lean source was changed and no Lean build was run. No new open-ended
search was launched above the inherited intervals. The finite root checks
test the new theorem's algebra; they are not empirical density proofs.
