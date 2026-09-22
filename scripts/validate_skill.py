#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "README.md",
    "references/orchestration-protocol.md",
    "references/cleanup-policy.md",
    "references/knowledge-preservation.md",
    "references/partitioning-policy.md",
    "references/risk-policy.md",
    "references/verification-policy.md",
    "prompts/explorer.md",
    "prompts/worker.md",
    "prompts/integrator.md",
    "prompts/verifier.md",
    "schemas/finding.schema.json",
    "schemas/worker-result.schema.json",
    "schemas/integration-result.schema.json",
    "schemas/cleanup-plan.schema.json",
    "schemas/verification-result.schema.json",
]


def main() -> int:
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        print("Missing required files:")
        for p in missing:
            print(" -", p)
        return 1

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        print("SKILL.md is missing YAML frontmatter")
        return 1
    if "name: repomeld" not in skill or "description:" not in skill:
        print("SKILL.md frontmatter is missing name/description")
        return 1

    for schema in (ROOT / "schemas").glob("*.json"):
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Invalid JSON schema {schema.name}: {exc}")
            return 1

    print("RepoMeld skill bundle validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
