# Independent review and retained evidence

25 November 2026. The starting commit is the verified merge of PR #11,
`5f262828091f50039da1605f660a98b85c121f5c`.

Two separate reviewers checked the new work. The final content hashes and
individual validation outcomes are retained in [review.json](review.json).
Every substantive file in the final manifest was rehashed before commit;
these review records are the only files subsequently added.

- The prime/filter reviewer independently checked the family proof,
  bounded CRT argument, complete isolated-length enumeration, scope of
  the README claims, and all arithmetic receipts. All four new checkers
  were rerun both normally and with `python3 -O`; their outputs matched
  one another and the retained outputs.
- The family reviewer cross-reviewed the prime-filter proof and its
  independent checker, both READMEs, the bounded-depth note, and the
  independent complete isolated-length checker. The prime checker passed
  normally and under optimization, and the exhaustive sample checker
  under optimization matched its retained receipt.
- The root investigator also checked the mathematical reductions and
  arithmetic, reproduced both original ten-million certificates, and
  verified the retained certificate comparisons. The lifting receipt
  differs only in elapsed runtime; the fixed-modulus receipt matches
  every field. The original programs and receipts are unchanged.

One earlier sentence could be read as promoting a ratio-only scan into
an entire-length exclusion. That wording was corrected. The final
entire-length claim is supported by the separate exhaustive computation
of all 14,997 full-sum positions and independent decimal construction at
every position, rather than by the regional scan. The variable-c
statement explicitly assumes `c>1` so its multiplicative-order notation
has no modulus-one ambiguity.

**No must-fix findings remain.** The reviewed claims are an infinite
family at depth at least four, eight new forbidden prime divisors, an
exact bounded-position criterion, and exclusion of one additional isolated
length. Complete consecutive coverage stays 1 through 10,000,000 inclusive.
The for-every-fixed-k construction, uniform regional rejection at the
required growing power, and global effective cutoff remain unproved.

These are ordinary mathematical proofs and exact computations. No new
Lean theorem or build is represented. Review approval here is a research
and code assessment; it is not a proof of the unresolved conjecture and
does not authorize merging. The requested draft pull request is left for
the owner.
