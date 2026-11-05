import json
import unittest
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


if __name__ == "__main__":
    unittest.main()
