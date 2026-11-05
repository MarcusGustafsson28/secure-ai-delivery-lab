import unittest

from app.policy_guard import check_policy


class CheckPolicyTests(unittest.TestCase):
    def valid_policy(self):
        return {
            "name": "blue-team-demo",
            "tools": ["read", "grep", "glob", "find"],
            "spawns": [],
        }

    def test_accepts_read_only_policy(self):
        self.assertEqual(check_policy(self.valid_policy()), [])

    def test_rejects_shell_and_write_tools(self):
        policy = self.valid_policy()
        policy["tools"] = ["read", "bash", "write"]

        findings = check_policy(policy)

        self.assertIn("Tool is not allowed: bash", findings)
        self.assertIn("Tool is not allowed: write", findings)

    def test_rejects_subagents(self):
        policy = self.valid_policy()
        policy["spawns"] = ["helper"]

        self.assertIn(
            "Subagents are not allowed by this demo policy.",
            check_policy(policy),
        )

    def test_requires_read_tool(self):
        policy = self.valid_policy()
        policy["tools"] = ["grep"]

        self.assertIn(
            "The policy must include the read tool.",
            check_policy(policy),
        )

    def test_rejects_duplicate_tools(self):
        policy = self.valid_policy()
        policy["tools"] = ["read", "read"]

        self.assertIn("Duplicate tool: read", check_policy(policy))

    def test_rejects_unknown_fields(self):
        policy = self.valid_policy()
        policy["network"] = True

        self.assertIn("Unsupported field: network", check_policy(policy))

    def test_rejects_non_object_policy(self):
        self.assertEqual(
            check_policy(["not", "an", "object"]),
            ["Policy must be a JSON object."],
        )

    def test_rejects_tools_that_are_not_a_list(self):
        policy = self.valid_policy()
        policy["tools"] = "read"

        self.assertIn(
            "Field 'tools' must be a list.",
            check_policy(policy),
        )


if __name__ == "__main__":
    unittest.main()
