"""Automated, fail-closed AKN finite-research cycle.

Discover -> enumerate -> independently check -> compare registered baseline ->
retain reproducible evidence -> propose next obligation. No mathematical claim
is promoted and no PR is merged by this driver.

Output always includes a machine-readable run record (even on exceptions).
A capped search is *inconclusive*, not evidence against missing chambers.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import traceback

AKN = Path(__file__).resolve().parent
MANIFEST = AKN / "atlas_chamber_full_manifest.json"


def _hash(path: Path):
    return sha256(path.read_bytes()).hexdigest()


def _invoke(script: str, args: list[str], output: Path):
    completed = subprocess.run(
        [sys.executable, str(AKN / script), *args],
        capture_output=True, text=True, check=False,
    )
    output.write_text(completed.stdout, encoding="utf-8")
    if completed.returncode:
        raise RuntimeError(
            f"{script} exited {completed.returncode}: {completed.stderr[-4000:]}"
        )
    return json.loads(completed.stdout)


def assess(packet: dict, replay: dict, baseline: dict):
    """Pure state-transition logic; tested independently of expensive jobs.

    Never confuse 'no counterexample found' with an exhaustive classification.
    """
    unknown = [leaf for leaf in packet["leaves"]
               if leaf.get("kind") == "classified"
               and leaf.get("orbit_class") == -1]
    if unknown:
        return "counterexample_candidate", (
            "Verify the exact unknown-star witness and independently derive its class."
        )
    if packet["frontier_count"] > 0:
        return "frontier_inconclusive", (
            "Resume or increase exact open-chamber search until frontier is empty."
        )
    if not packet.get("search_exhausted") or not replay.get(
            "coverage_verified_generic", False):
        return "verification_failed", (
            "Reconcile independent enumerator and verifier disagreement."
        )
    failures = []
    if replay["independently_counted_regions"] != baseline[
            "independent_exact_2d_slice_arrangement_region_count"]:
        failures.append("region count")
    if replay["exact_witnessed_distinct_chambers"] != baseline[
            "enumerated_full_dimensional_chambers"]:
        failures.append("witness count")
    if replay["slice_region_counts_sha256"] != baseline[
            "independent_105_slice_region_counts_sha256"]:
        failures.append("independent planar-slice digest")
    if not replay.get("exactly_existing_24_orbits"):
        failures.append("24-orbit equivalence")
    if replay.get("stabilizer_subgroup_conjugacy_types") != baseline[
            "stabilizer_subgroup_conjugacy_types"]:
        failures.append("conjugacy classification")
    if failures:
        return "baseline_disagreement", (
            "Audit exact mathematical change before registering claims: "
            + ", ".join(failures)
        )
    return "generic_candidate_verified", (
        "Automate singular-stratum membership under an explicit boundary-selection "
        "convention; separately review claim-governance promotion."
    )


def drive(out: Path, max_nodes: int, max_depth: int, require_full: bool):
    out.mkdir(parents=True, exist_ok=True)
    baseline = json.loads(MANIFEST.read_text(encoding="utf-8"))
    record = {
        "schema": "AKN-AUTOMATED-RESEARCH-RUN-1",
        "phase": "exact-generic-chamber-atlas",
        "state": "running",
        "inputs": {"max_nodes": max_nodes, "max_depth": max_depth,
                   "require_full": require_full,
                   "baseline_sha256": _hash(MANIFEST)},
        "scope": "generic open chambers only; singular boundaries separate",
        "claim_promotion_automatic": False,
        "next_obligation": "exact evidence required",
    }
    target = out / "research-run.json"

    def persist():
        target.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")

    persist()
    try:
        packet_path = out / "chambers.json"
        generated = subprocess.run([
            sys.executable, str(AKN/"atlas_chambers.py"),
            "--max-nodes", str(max_nodes),
            "--max-depth", str(max_depth),
            "--out", str(packet_path),
        ], capture_output=True, text=True, check=False)
        (out/"enumerator-stderr.txt").write_text(
            generated.stderr, encoding="utf-8")
        if generated.returncode:
            raise RuntimeError(
                f"enumerator exited {generated.returncode}: "
                + generated.stderr[-4000:]
            )
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        if packet["frontier_count"] > 0:
            replay = _invoke(
                "atlas_chamber_check.py", [str(packet_path)],
                out/"independent-replay.json")
        else:
            replay = _invoke(
                "atlas_region_count.py", ["--packet", str(packet_path)],
                out/"independent-replay.json")

        state, next_obligation = assess(packet, replay, baseline)
        record.update({
            "state": state,
            "next_obligation": next_obligation,
            "evidence": {
                "packet_sha256": _hash(packet_path),
                "independent_replay_sha256":
                    _hash(out/"independent-replay.json"),
                "classified_chambers": packet["classified_count"],
                "remaining_frontier_prefixes": packet["frontier_count"],
                "distinct_star_orbits": len(
                    set(leaf["orbit_class"] for leaf in packet["leaves"]
                        if leaf.get("kind") == "classified")),
                "observed_new_class_candidates": sum(
                    leaf.get("orbit_class") == -1 for leaf in packet["leaves"]
                    if leaf.get("kind") == "classified"),
                "independent_checker": (
                    "strict-FM-prefix-tree" if packet["frontier_count"]
                    else "2D-slice-region-count"),
                "generic_coverage_verified":
                    bool(replay.get("coverage_verified_generic", False)),
                "singular_boundary_membership_verified": False,
            }
        })
    except Exception as exc:
        record.update({
            "state": "execution_or_verification_error",
            "next_obligation": "Inspect retained stderr and fix exact-head failure.",
            "error": f"{type(exc).__name__}: {exc}",
        })
        (out/"traceback.txt").write_text(traceback.format_exc(),
                                         encoding="utf-8")
    finally:
        persist()

    if record["state"] == "generic_candidate_verified":
        return 0
    if record["state"] == "frontier_inconclusive" and not require_full:
        return 0
    # Counterexample and baseline disagreement intentionally fail CI, but
    # artifacts remain: a failure must not erase mathematically useful data.
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-nodes", type=int, default=100000)
    parser.add_argument("--max-depth", type=int, default=15)
    parser.add_argument("--require-full", action="store_true")
    args = parser.parse_args()
    if args.max_nodes < 0 or not 0 <= args.max_depth <= 15:
        parser.error("max-nodes must be nonnegative and max-depth between 0 and 15")
    sys.exit(drive(args.out, args.max_nodes, args.max_depth,
                   args.require_full))


if __name__ == "__main__":
    main()
