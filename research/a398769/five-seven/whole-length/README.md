# Whole-length exclusions: proof and computation audit

25 November 2026. **All proposed claims verified**, with a separate
depth-one argument using the specific lift `i=9 mod42`.

Starting current `main` was exactly
`022e8120d0af98030b60bdda117b45fbfdba0543`, verified locally as a merge
with parents `2505f83c98fff9d11971c83f6a833740f7afadf6` and
`a6ec9cf084e7cd1388ad396b7098bc6a910a2dbc`. Live GitHub identified it
as the merge of [PR #13](https://github.com/lukeroyle-beep/Mathematics/pull/13).
Work uses a separate checkout and branch `research/a398769-whole-length-audit`.

## Verdicts

| Claim | Verdict | Reason |
|---|---|---|
| Full-sum spacing | Verified | All actual positions are exactly `i+h*ord_S(10)`, even when `3|S`. |
| Infinite maximum-depth family, fixed k>=2 | Verified | The exact-depth position is unique at depth at least two because `7d>L`. |
| Infinite maximum-depth family, k=1 | Verified | Density works for fixed `e=9 mod42`; all possible neighbours have exact depth one. |
| `S=3^164*17^41` | Entire length excluded | One compatible position; maximum depth four. |
| `S=3^103*898129^21` | Entire length excluded | 14,997 compatible positions, both parities; maximum depth seven. |

[PROOF.md](PROOF.md) proves the general spacing lemma and the stronger
whole-length theorem. For every fixed `k>=1` and every nonempty open
`I` inside `(0,1)`, infinitely many distinct odd lengths `L>k+2` have
maximum depth **exactly k over all full-sum-compatible actual positions**,
attained at an i with `i/L in I`. Since a witness needs depth `L-2`,
these entire lengths are excluded.

There is no failed claim to weaken. Two tempting shortcuts are invalid:
large spacing without a known actual position gives only at-most-one;
depth-two spacing alone does not control a depth-one base. The proof
checks the density construction for the specific e=9 lift and evaluates
every possible neighbour. Retaining the illustrative e=3 lift without
this check would leave a possible deeper neighbour. This is a new
strengthening, not a repair to the merged fixed-depth pair theorem.

## Exact appendix results

Both programs read the unchanged decimal i values directly from the
merged [SUBMISSION.txt](../fixed-depth/SUBMISSION.txt). Its SHA-256 is
`7e77aef5b8b5b3e4b7fff5357c1ef035571e447147f6381082f44909cd9e85ca`.
The complete decimal values of S, L, i, d, first/last positions, adjacent
out-of-range positions, and all order controls are recorded in
[checks.json](checks.json) and [blocks.json](blocks.json).

| S | exact d | signed h range in `3<=i+hd<L` | count | exact maximum |
|---|---|---|---:|---:|
| `3^164*17^41` | `16*3^162*17^40` | `0..0` | 1 | 4 |
| `3^103*898129^21` | `77*3^101*898129^20` | `-6195..8801` | 14,997 | 7 |

| S | valuation histogram (depth: count) |
|---|---|
| `3^164*17^41` | `{4:1}` |
| `3^103*898129^21` | `{0:7499, 1:0, 2:6427, 3:918, 4:131, 5:19, 6:2, 7:1}` |

In the second example all 7,499 even positions have depth zero. The
7,498 odd positions account for every positive-depth entry. The supplied
i is the unique maximum in each example. The sparse JSON histograms
omit the zero-count depth-one entry.

| example | k | `F mod(225S7^k)` | `F mod7^(k+1)` | independent `n mod(25S7^k)` | independent `n mod7^(k+1)` |
|---|---:|---:|---:|---:|---:|
| prime 17 | 4 | 0 | 2401 | 0 | 9604 |
| prime 898129 | 7 | 0 | 1647086 | 0 | 823543 |

The order at p=898129 is certified as `56133=3^6*7*11`, with
proper-divisor powers `66723,631165,615263`. The lift is certified by
`10^56133 mod p^2=681130256053=1+758388p`, giving order
`56133*p^20` at `p^21`. Trial division through 947 certifies primality.
Both composite orders are also checked directly at the order and at
the order divided by each distinct prime factor.

## Independent methods and validation

[checks.py](checks.py) evaluates F by direct modular powers at every
position, including the full `9S` modulus and a nonzero residue modulo
`7^12`. [independent_blocks.py](independent_blocks.py) imports no checker
or expected receipt. At **every** position it constructs the four decimal
blocks by binary concatenation modulo `25S*7^10`, without evaluating F
or dividing by nine. It checks `n mod25S=0` and requires a nonzero
residue modulo `7^10`, making every valuation exact.

Both methods give identical ordered position/depth SHA-256 digests:

```
prime 17:     b46ab68670fb74efb0d891b655f08c34f93f48d405e6b4212ba9b7780eaed867
prime 898129: 04c25b18c52358c9f400fb9c3666c97ffb37cadb1a6e24c91222679e3a5c0b6d
```

The primary check tests 31,840 literal decimal pairs at eligible odd
lengths 5..401, including 10,348 pairs with `3|S`; it compares complete
sum classes and nonempty joint-depth classes at k=1..4. A positive
three-divisible control is `L=13,S=87,d=28`, position 12. The independent
checker validates its block routine with 6,240 literal-word comparisons,
then tests the complete sum class at 199 eligible odd lengths through
501, including 22 qualifying lengths with `3|S`. These finite controls
validate the implementations; the infinite theorem rests on the proof.

Normal and optimized runs of both checkers reproduce their committed
receipts byte for byte. Every check uses explicit exceptions, so `-O`
does not remove it. Separate reviewer contexts independently verified
the proof and arithmetic, including a third scratch direct-power
enumeration. [REVIEW.md](REVIEW.md) records the review and limitation.
[verification.json](verification.json) records hashes and execution evidence.

## Reproduction

From repository root with Python 3.9+ (standard library only):

```sh
python3 research/a398769/five-seven/whole-length/checks.py > /tmp/whole-length-primary.json
python3 -O research/a398769/five-seven/whole-length/checks.py > /tmp/whole-length-primary-opt.json
cmp /tmp/whole-length-primary.json /tmp/whole-length-primary-opt.json
cmp /tmp/whole-length-primary.json research/a398769/five-seven/whole-length/checks.json
python3 research/a398769/five-seven/whole-length/independent_blocks.py > /tmp/whole-length-blocks.json
python3 -O research/a398769/five-seven/whole-length/independent_blocks.py > /tmp/whole-length-blocks-opt.json
cmp /tmp/whole-length-blocks.json /tmp/whole-length-blocks-opt.json
cmp /tmp/whole-length-blocks.json research/a398769/five-seven/whole-length/blocks.json
git diff --check
```

The block checker takes roughly two minutes per run on the audit host;
it rebuilds both long seven-blocks for every position. Successful `cmp`
and `git diff --check` commands are silent with exit status zero.
For semantic agreement between independently structured receipts:

```sh
python3 - <<'PY'
import json
from pathlib import Path
p = Path('research/a398769/five-seven/whole-length')
a = json.loads((p/'checks.json').read_text())['examples']
b = json.loads((p/'blocks.json').read_text())['appendix_examples']
keys = ('S','L','i','d','first_position','last_position',
        'valuation_histogram','parity_histograms','maximum_depth',
        'ordered_position_depth_sha256')
for x,y in zip(a,b):
    for key in keys:
        if x[key] != y[key]:
            raise SystemExit('mismatch: '+key)
    if (x['signed_h_min'], x['signed_h_max'], x['positions']) != (y['h_min'], y['h_max'], y['count']):
        raise SystemExit('endpoint/count mismatch')
print('Independent receipts agree on both complete position sets and depths.')
PY
```

Exact output:

```
Independent receipts agree on both complete position sets and depths.
```

Fresh inherited checks (C++17 compiler also needed for the first):

```sh
python3 research/a398769/five-seven/settlement/verify.py --output /tmp/whole-length-lifting.json
python3 research/a398769/five-seven/settlement/verify_fixed.py --output /tmp/whole-length-fixed.json
python3 research/a398769/five-seven/depth/checks_depth_samples.py > /tmp/whole-length-isolated.json
cmp /tmp/whole-length-fixed.json research/a398769/five-seven/depth/baseline_independent_rerun.json
cmp /tmp/whole-length-isolated.json research/a398769/five-seven/depth/depth_samples.json
```

The latter two receipts match byte for byte. Parsed lifting JSON matches
`depth/baseline_lifting_rerun.json` except only `elapsed_seconds`.

## Coverage and open obligations

| Result | Scope |
|---|---|
| Consecutive certificate | All lengths **1..10,000,000 inclusive**, unchanged. |
| Earlier isolated length | `(898129*3^193+4)/7`, 14,997 full-sum positions, maximum six. |
| First appendix length | `(3^164*17^41+4)/7`, one full-sum position, maximum four. |
| Second appendix length | `(3^103*898129^21+4)/7`, 14,997 full-sum positions, maximum seven. |
| Infinite family | For each fixed k and I, infinitely many whole lengths excluded with maximum exactly k attained in I. |

The earlier isolated length is exactly
`15582704697570091495948156638491914590405161120787807516829906317314612303918977615165179656913553`.
Its histogram is `{0:7499, 2:6427, 3:918, 4:131, 5:19, 6:3}`;
it is not the new depth-seven appendix length.

The [merged residual reduction](../settlement/README.md) excludes other
digit counts and parities and reduces possible `{5,7}` witnesses to
these two-five words. The new whole-length exclusions therefore apply
to that entire subclass at the stated lengths. The historical PR #13
wording that its pair computations did not exclude whole lengths was
correct about the evidence then recorded; this audit supplies the
missing exhaustive argument and computation.

No consecutive interval above ten million is certified here. The
**all-length `{5,7}` subclass remains open**: a proof must still reject
`225(7L-4)*7^(L-2) | F(L,j)` uniformly for every remaining admissible
length and position, or find a witness. Fixed k followed by unbounded
L does not settle that moving threshold. The full A398769 digit-1
conjecture remains unresolved as well. No Lean files changed and no
new Lean theorem or build is claimed. Delivery is a **draft PR for owner
review; merging remains with the owner**.
