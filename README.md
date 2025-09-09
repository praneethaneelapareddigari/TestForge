# TestForge – Multi-Language Unit Test Generator and Reviewer

A scaffold for TestForge: generates unit test stubs across Python/Java/Go/TypeScript, runs mutation tests (via external tools), and enforces deterministic quality gates in CI. Includes a simple GitHub PR reviewer to post coverage/mutation summaries.

## Quickstart (local)
1. Create venv & install deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
