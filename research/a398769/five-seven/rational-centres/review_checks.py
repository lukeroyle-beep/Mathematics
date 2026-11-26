#!/usr/bin/env python3
"""Independent review binding and deliberate-corruption checks.

This verifies retained evidence and rejection behavior, not the full search.
The separately documented reviewer also reran both original b=289 searches.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
REVIEWED_COMMIT = "9eaa913f515e62667dbf706ec723043c5b0a193c"
VERIFICATION_SHA256 = "59a9ebbe2c3a59ed5aef3a9a7961452a653f557b532f7413c3b8f405045073fc"


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    require(sha(HERE/"verification.json") == VERIFICATION_SHA256,
            "reviewed implementation receipt differs")
    receipt = json.loads((HERE/"verification.json").read_text())
    for path, expected in receipt["artifact_sha256"].items():
        require(sha(HERE/path) == expected, "review binding mismatch: " + path)
    spec = importlib.util.spec_from_file_location("reviewed_verifier", HERE/"verify.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    bands, control, digest = verifier.audit(HERE/"receipts/primary", HERE/"receipts/independent")
    require(digest == receipt["ordered_partition_pair_digest"], "review aggregate differs")
    rejected = []
    with tempfile.TemporaryDirectory(prefix="a398769-review-corruption-") as directory:
        root = Path(directory)
        primary, independent = root/"primary", root/"independent"
        shutil.copytree(HERE/"receipts/primary", primary)
        shutil.copytree(HERE/"receipts/independent", independent)
        target = primary/"K15-b102.json"
        original = target.read_bytes()

        def rejects(label):
            try:
                verifier.audit(primary, independent)
            except (RuntimeError, KeyError, TypeError):
                rejected.append(label)
                return
            raise RuntimeError("corrupted evidence accepted: " + label)

        target.unlink()
        rejects("missing_partition")
        target.write_bytes(original)
        duplicate = primary/"duplicate.json"
        duplicate.write_bytes(original)
        rejects("duplicate_partition")
        duplicate.unlink()
        for field, value in (("b", 103), ("lo", 1000002000003),
                             ("source_sha256", "0"*64), ("compatible_lines", 7233),
                             ("pairs13_sha256", "0"*64), ("pairs13", 2660),
                             ("survivors22", [[1, 0, 3, 2]])):
            changed = json.loads(original)
            changed[field] = value
            target.write_text(json.dumps(changed))
            rejects(field)
            target.write_bytes(original)
        verifier.audit(primary, independent)
    print(json.dumps({
        "status": "PASS", "reviewed_implementation_commit": REVIEWED_COMMIT,
        "verification_sha256": VERIFICATION_SHA256,
        "implementation_artifact_bindings": len(receipt["artifact_sha256"]),
        "partitions_per_engine": sum(row["partitions"] for row in bands),
        "control_pairs13": control["pairs13"],
        "ordered_partition_pair_digest": digest,
        "deliberate_corruptions_rejected": rejected,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
