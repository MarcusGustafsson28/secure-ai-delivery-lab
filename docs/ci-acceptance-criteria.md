CI ACCEPTANCE CRITERIA FOR MVP

Status: implemented and verified on GitHub; tests pass on ubuntu-24.04.

WORKFLOW BEHAVIOR

The workflow runs on pushes and pull requests.
It does not use the pull_request_target event.
It uses a GitHub-hosted runner, not a self-hosted runner for pull requests.
It has a timeout so a stuck job cannot run indefinitely.

PERMISSIONS AND DEPENDENCIES

The workflow grants the GITHUB_TOKEN contents read permission only.
The MVP does not use write permissions, secrets, publishing, or deployment.
Every GitHub Action is pinned to a verified full commit SHA.
A comment records which version each SHA represents.
The Python demo uses only the standard library in the MVP.
Any later external dependency must have a documented version and review process.

CHECKS

The workflow runs python -m unittest discover -s tests -v.
A failed test makes the CI job fail.
CI does not make automatic changes, merges, or releases.
Changes to GitHub workflow files receive manual review.

SOURCE

GitHub Secure use reference:
https://docs.github.com/en/actions/reference/security/secure-use
