"""Run with PYTHONPATH=<finite-math-kernels>/tools python -m unittest discover -s tests.

Uses the shared checker; mutations run only in disposable repository copies.
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from claim_governance.policy import load_policy
from claim_governance.runner import run

ROOT = Path(__file__).resolve().parents[1]


class ClaimSurfaces(unittest.TestCase):
    def test_baseline_and_normalization(self):
        policy = load_policy(ROOT / 'claim_governance.toml')
        self.assertEqual(run(policy, ROOT, []), ())
        shared = {'README.md', 'docs/roadmap.md', 'research/candidates.json'}
        dossier = {'KATZ-AKN-C1': 'docs/research/katz-akn-c1-local-completeness.md',
                   'KATZ-AKN-PERFECT': 'docs/research/katz-akn-c1-local-completeness.md',
                   'AKN-ATLAS-PERIODIC': 'docs/research/akn-vertex-atlas-periodic-approximant.md'}
        self.assertEqual({claim.name for claim in policy.ledger}, set(dossier))
        for claim in policy.ledger:
            self.assertEqual({s.path for s in claim.surfaces}, shared | {dossier[claim.name]})
        for label, status in policy.status.synonyms.items():
            self.assertEqual(policy.status.classes_in(label), frozenset({status}))
        for status in policy.status.classes:
            self.assertEqual(policy.status.classes_in(status), frozenset({status}))
        self.assertEqual(policy.status.classes_in('reopened non-open candidatehood'), frozenset())

    def test_each_status_surface_rejects_drift(self):
        policy = load_policy(ROOT / 'claim_governance.toml')
        for claim in policy.ledger:
            for surface in claim.surfaces:
                with self.subTest(claim=claim.name, path=surface.path):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        for path in {s.path for c in policy.ledger for s in c.surfaces}:
                            target = root / path
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copyfile(ROOT / path, target)
                        target = root / surface.path
                        lines = target.read_text().splitlines(keepends=True)
                        hits = [i for i, line in enumerate(lines) if surface.anchor in line]
                        self.assertEqual(len(hits), 1, 'anchor must identify a unique claim')
                        start = hits[0]
                        end = start + surface.window_lines + 1
                        region = ''.join(lines[start:end])
                        self.assertEqual(policy.status.classes_in(region), frozenset({claim.status}))
                        other = 'candidate' if claim.status == 'open' else 'open'
                        self.assertEqual(region.count(claim.status), 1)
                        lines[start:end] = [region.replace(claim.status, other, 1)]
                        target.write_text(''.join(lines))
                        findings = run(policy, root, ['consistency'])
                        self.assertTrue(any(f.path == surface.path and f.rule == claim.name
                                            and 'surface shows' in f.message for f in findings), findings)


if __name__ == '__main__':
    unittest.main()
