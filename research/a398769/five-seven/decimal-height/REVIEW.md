# Independent mathematical and arithmetic review

26 November 2026. **PASS for the stated investigation. No unresolved
must-fix finding.** The proposed global inequality remains unproved and
unrefuted; passing this review does not prove it.

The independently reviewed implementation is exactly
`574cd7a28357e7d4e94f1f47aae749732eb51078`. Its ancestor
`aab83fc4ed706cd4aca4d51dc6e533d60cb87477` is the local merge commit for
PR #22. The implementation and root README were inspected by a separate
review agent after implementation. The reviewer did not edit implementation
files, make Git commits, publish a PR, or merge. These review artifacts
are subsequent additions. Publication and unmerged draft status remain
the publishing agent's separate verification responsibility.

The [independent receipt](independent-review.json) binds the examined
implementation files and root README to their exact hashes.
[independent_review.py](independent_review.py) also reads those files from
the named Git commit and refuses a binding mismatch.

## Mathematical findings

| Obligation | Result and basis |
| --- | --- |
| Domain and cofactor, including composite S and `3|S` | PASS. `v5(F)=2`, `gcd(25,9S)=1`, and `S=3 mod7` give positive integral `H=F/(225S)` with `v7(H)=t`. No cancellation of nine against S occurs. |
| Original digit product and sum | PASS. The two-fives decimal word is `n=F/9`, has sum S and product `25*7^(L-2)`. Its full divisibility is exactly `225S*7^(L-2)|F`. |
| Conditional cutoff | PASS. The strict integer bound is exactly `L<=444444444445`, below B. The next integer fails, and the allowed endpoint is odd. This remains conditional on the proposed inequality. |
| Decimal threshold | PASS. For integral positive H, the target is exactly `t<=d+11`; failure is exactly `t>=d+12`. Equality at the lower decimal boundary is retained. |
| Actual representative and lift deadline | PASS. Primitive-root order gives a unique `r_K`; `t>=K` forces `i=r_K`. The first nonzero lift digit is `a_t`, not `a_(t+1)`. The unresolved inclusive deadline is `[K,d+11]`, with `d+11<=L-3` above B. |
| Exact initial remaining band | PASS. For `B<L<=3301587301587`, `d=L-14`. The endpoint coefficients are 1375 and -200 at the next integer. Consequently failure equals the full-witness condition in this band; no absence in the band is inferred. |
| Low-depth replacement | PASS. The elementary induction yields `10^t<F/(225S)` for `t<K`, with explicit small bases. It supplies all-position coverage at a sampled length when combined with its sole actual high-depth representative. |
| Exact sum and CRT | PASS. Working with n avoids division by 18 modulo a multiple of three. The order argument gives `v7(ord_S(10))<=K-1`; the common CRT modulus stabilizes. It establishes no bounded-position escape deadline. |
| Effective position criterion and strip | PASS. The integer criterion follows from the inherited quadratic estimate and `log(10)<3`. The normalized midpoint estimate bridges to `d+11` with exact margin `8712828/25` at `L=10^7`, increasing thereafter. |
| Finite inherited target conclusion | PASS as an inherited consequence. Maximum valuation 27 through `10^12`, maximum 21 for actual depth-K representatives in the adjoining interval, and the low-depth bound imply the target for sum-compatible odd `5<=L<=B`. The literal checks cover the small endpoint cases. |
| Qualitative and effective global replacements | PASS. The uniform qualitative `t=o(L)` implies eventual target validity, without a computable starting length. PR #22's explicit signed bound has a coefficient greater than one and does not supply the missing decimal threshold. |
| Global verdict | PASS as reporting. The precise missing universal assertion is stated without assuming it in pruning. The inequality, `{5,7}` subclass, and wider conjecture remain open. |

The parameter substitution was checked against Bugeaud--Laurent's
[Corollary 1, printed p. 4](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf):
the global degree factor, local degree one, height conditions, positive
exponents, independence, and normalized coefficient are retained.
Evertse's [Corollary 1, printed p. 227](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf)
was checked, including its exact formula in a rendered primary-source
page. The tuple `(U,-V,-1,-W)` has common gcd one and no proper zero
subsum; only W contributes outside the fixed prime set. This gives
finiteness, without an effective last exception.

## Fresh verification and limits

Both `checks.py` and `proof_checks.py` were freshly run normally and with
`python3 -O`. Each output was byte-identical to its committed receipt.
The revised endpoint proof checks were rerun after the final implementation
commit. The independent review program also passed in both modes, with
byte-identical outputs.

The independent arithmetic uses signed carries from small to large decimal
exponents, rather than the implementation's coefficient dominance and
short-gap merging. Modular words use a repunit evaluated modulo `9m`
followed by exact division of its representative by nine, rather than run
concatenation. Actual high-depth representatives are recovered by testing
all seven children, without using the explicit lift coefficient or seeding
the recorded representative.

- 5,012 independent signed-carry controls passed, including enormous
  exponents and exact cancellation.
- All 22,350 original decimal words for odd `5<=L<=301` were independently
  reconstructed. There are 46 five-free sum-compatible pairs, including
  34 with `3|S`; all satisfy the target.
- The exact scattered set contains 201 lengths above B, with 74 actual
  high-depth representatives and greatest exact valuation 64. None of
  those 74 passes the full sum condition. The low-depth theorem and these
  representative checks together cover all positions at each listed
  length; they do not cover intervening lengths.
- The six giant sum-positive controls occur at three distinct lengths and
  have exact valuations `4,7,0,6,6,6`. Every one has `3|S`, has `t<K`,
  satisfies the target, and fails the full-witness condition. They are
  nonvacuous sum controls, but none tests the unresolved joint high-depth
  premise positively.
- The original archive checker was freshly rerun in its default
  `not_rerun` mode. Its full receipt matches `baseline.json`: 74,601
  retained candidates were arithmetically checked, with 27 internal hashes
  and source bindings verified. All 35 PR #21 artifact bindings were also
  checked. The PR #21 scanner's treatment of all actual representatives
  was inspected.

The full archived enumerators and PR #21 million-length arithmetic scan
were **not rerun** in this review. Their completeness remains inherited
from the authenticated prior certificates. Neither fresh retained-candidate
verification nor matching hashes independently proves enumeration
completeness. No density argument was audited, and no Lean build or new
Lean theorem is claimed.

To reproduce the independent controls from the repository root:

```sh
python3 research/a398769/five-seven/decimal-height/independent_review.py > /tmp/height-independent-review.json
python3 -O research/a398769/five-seven/decimal-height/independent_review.py > /tmp/height-independent-review-O.json
cmp /tmp/height-independent-review.json /tmp/height-independent-review-O.json
cmp /tmp/height-independent-review.json research/a398769/five-seven/decimal-height/independent-review.json
```

The research obligation remains to prove the nonzero lift within
`[K,d+11]` for every actual full-sum-compatible representative above B,
or produce a pair satisfying that exact premise and violating the bound.
This review supplies neither result and finds no claim that it does.
