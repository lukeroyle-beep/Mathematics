#!/usr/bin/env python3
"""Independent original-word checker reused, with all 256 classes solved afresh.

No primary arithmetic is imported. The inherited implementation is explicitly
hash-bound; this adapter extends its declared range, not its mathematics.
"""
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'sum-position-escape'/'independent.py'


def main():
    spec = importlib.util.spec_from_file_location('decimal_blocks_independent', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    controls = module.controls()
    control = module.case(25)
    cases = [module.case(31+6*u) for u in range(256)]
    result = dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  inherited_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                  method='independent original decimal blocks and fresh ternary lifts',
                  specified_exponents=dict(first=31, step=6, count=256, last=1561, next=1567),
                  class_misses=sum(r['i'] is None for r in cases),
                  actual_candidates=sum(r['i'] is not None for r in cases),
                  valuation_histogram=dict(sorted(Counter(str(r['t']) for r in cases if r['i'] is not None).items())),
                  control_a25=control, controls=controls, cases=cases)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
