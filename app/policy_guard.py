import argparse
import json
from pathlib import Path

ALLOWED_TOOLS = {"read", "grep", "glob", "find"}
EXPECTED_FIELDS = {"name", "tools", "spawns"}


def check_policy(policy: object) -> list[str]:
    if not isinstance(policy, dict):
        return ["Policy must be a JSON object."]

    findings = []
    unexpected_fields = sorted(set(policy) - EXPECTED_FIELDS)

    for field in unexpected_fields:
        findings.append(f"Unsupported field: {field}")

    name = policy.get("name")
    if not isinstance(name, str) or not name.strip():
        findings.append("Field 'name' must be a non-empty string.")

    tools = policy.get("tools")
    if not isinstance(tools, list):
        findings.append("Field 'tools' must be a list.")
    else:
        seen_tools = set()

        for tool in tools:
            if not isinstance(tool, str) or not tool:
                findings.append("Every tool name must be a non-empty string.")
                continue

            if tool in seen_tools:
                findings.append(f"Duplicate tool: {tool}")
                continue

            seen_tools.add(tool)

            if tool not in ALLOWED_TOOLS:
                findings.append(f"Tool is not allowed: {tool}")

        if "read" not in seen_tools:
            findings.append("The policy must include the read tool.")

    spawns = policy.get("spawns")
    if not isinstance(spawns, list):
        findings.append("Field 'spawns' must be a list.")
    elif spawns:
        findings.append("Subagents are not allowed by this demo policy.")

    return findings


def reject_duplicate_keys(pairs):
    result = {}

    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key.")
        result[key] = value

    return result


def resolve_policy_file(value: Path, project_root: Path) -> Path:
    candidate = value.expanduser()

    if not candidate.is_absolute():
        candidate = project_root / candidate

    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(project_root)
    except (OSError, ValueError) as error:
        raise ValueError(
            "Policy file must exist inside the project directory."
        ) from error

    if not resolved.is_file() or resolved.suffix.lower() != ".json":
        raise ValueError("Policy file must be a JSON file.")

    return resolved


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Check a JSON agent policy against a read-only allowlist."
    )
    parser.add_argument(
        "policy_file",
        nargs="?",
        type=Path,
        default=Path("examples/agent-policy.json"),
        help="JSON policy path relative to the project directory.",
    )
    args = parser.parse_args()

    try:
        policy_file = resolve_policy_file(args.policy_file, project_root)
        with policy_file.open(encoding="utf-8") as handle:
            policy = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")
        return 2

    findings = check_policy(policy)

    if findings:
        print("DENY: policy did not pass.")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("PASS: policy uses allowed tools and has no subagents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
