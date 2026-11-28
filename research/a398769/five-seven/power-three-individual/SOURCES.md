# Sources and provenance

The branch starts from current main
`a9edeb0a96bd56d55f3c96767f5154e69cb8ceda`, fetched on 27 November 2026.
Git ancestry and GitHub's PR #29 metadata independently identify this as
the requested merge. No later main commit existed at the starting read.
`baseline.json` binds all 1,067 files in that exact Git archive.

The required project inputs were read from this base:

- `../power-three/INDIVIDUAL.md`
- `../power-three-pair/PAIR.md`
- `../power-three-pair/LOGARITHMS.md`
- `../power-three-pair/INDIVIDUAL.md`
- `../rational-centres/ANALYTIC.md`

The prior adjacent-pair theorem strengthens the earlier three-member
obstruction but leaves isolated witnesses possible. Its individual
certificate adds a=1567 to the 256 inherited rows. Both prior 256-row
receipts are cross-compared by the new verifier; the two next rows are
recomputed independently. Historical consecutive whole-length coverage
is inherited, with its exact base-file hashes preserved. Neither the
trillion archive nor its adjacent million-odd-length scan is rerun here.

## Primary logarithm source

Y. Bugeaud and M. Laurent, *Minoration effective de la distance p-adique
entre puissances de nombres algébriques*, [author-hosted PDF](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
Corollary 2 is on **printed page 5**, with the definitions of local and
global degree, height, exponents and b' on printed pages 2–4.

The primary text was reopened through the web tool during this audit.
Printed page 5 was also rendered and visually inspected from the retained
local PDF. Its bytes were freshly hash-checked:

```text
SHA-256 554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d
271382 bytes
```

This is a fresh local hash verification of the previously downloaded
PDF, not a claim of a fresh raw-byte network download. The PDF is not
copied into this repository. Both the common-factor substitution and
the moving-position three-adic substitution retain the source's actual
degree parameter and every branch of its maximum.

## Fresh versus inherited verification

Four new programs produce source-bound deterministic receipts. The
primary individual path explicitly reuses `../power-three/individuals.py`;
the decimal-block and index-lift paths import no research arithmetic.
The common-factor finite remainder uses inherited exact rows and fresh
modular readback, while both new individual programs reconstruct those
twelve classes from their definitions.

Before modifying the root README, these inherited commands passed in
both ordinary and optimized Python:

```sh
pp=research/a398769/five-seven/power-three-pair
python3 "$pp/verify.py" --run
python3 -O "$pp/verify.py" --run
python3 "$pp/review_check.py"
python3 -O "$pp/review_check.py"
```

The historical source-bound review must be reproduced at its original
tree (PR #29 merge or recorded implementation), because its root README
hash correctly changes with this new entry. New verification does not
alter historical receipts to conceal that change. No Lean command was
run for this task, and no new formal verification is claimed.
