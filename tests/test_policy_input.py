import json
import unittest
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from app.policy_guard import reject_duplicate_keys, resolve_policy_file


class PolicyInputTests(unittest.TestCase):
    def test_rejects_duplicate_json_keys(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            json.loads(
                '{"name":"first","name":"second"}',
                object_pairs_hook=reject_duplicate_keys,
            )

    def test_rejects_policy_outside_project(self):
        project_root = Path(__file__).resolve().parents[1]

        with TemporaryDirectory() as directory:
            outside_policy = Path(directory) / "policy.json"
            outside_policy.write_text('{"name":"outside"}', encoding="utf-8")

            with self.assertRaisesRegex(
                ValueError, "inside the project directory"
            ):
                resolve_policy_file(outside_policy, project_root)

    def test_cli_rejects_malformed_json(self):
        project_root = Path(__file__).resolve().parents[1]
        app = project_root / "app" / "policy_guard.py"

        with TemporaryDirectory(dir=project_root / "examples") as directory:
            policy_file = Path(directory) / "malformed.json"
            policy_file.write_text('{"name":', encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(app), str(policy_file)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stdout.startswith("ERROR: "))
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
