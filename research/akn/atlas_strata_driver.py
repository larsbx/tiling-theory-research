"""Run singular enumeration and independent replay with exact-head provenance."""
from __future__ import annotations

import argparse
from hashlib import file_digest
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def digest(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def drive(out, max_pairs):
    out.mkdir(parents=True, exist_ok=True)
    packet = out/"singular-strata.json"
    replay = out/"singular-replay.json"
    record = {
        "source_revision": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=HERE, text=True).strip(),
        "max_pairs": max_pairs,
        "state": "running",
    }
    record_path = out/"singular-run.json"
    def persist():
        record_path.write_text(json.dumps(record, indent=2, sort_keys=True)+"\n")

    persist()
    try:
        for script, args in (
            ("atlas_singular_strata.py",
             ["--out", str(packet), "--max-pairs", str(max_pairs)]),
            ("atlas_strata_check.py", [str(packet), "--out", str(replay)]),
        ):
            with (out/(script+".log")).open("w") as log:
                result = subprocess.run([sys.executable, str(HERE/script), *args],
                                        stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                record["state"] = "verification_failed"
                record["failed_script"] = script
                return 1
            if script == "atlas_singular_strata.py":
                record["packet_sha256"] = digest(packet)
                if max_pairs < 8505:
                    record["state"] = "frontier_inconclusive"
                    return 1
        record["replay_sha256"] = digest(replay)
        record["state"] = "verified_finite_singular_atlas"
        return 0
    finally:
        persist()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-pairs", type=int, default=8505)
    args = parser.parse_args()
    if args.max_pairs < 0:
        parser.error("--max-pairs must be nonnegative")
    sys.exit(drive(args.out, args.max_pairs))


if __name__ == "__main__":
    main()
