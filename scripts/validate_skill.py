#!/usr/bin/env python3
"""Validate the RepoMeld skill bundle: required files, frontmatter, subskill
numbering, schema sanity, and cross-file reference integrity."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "README.md",
    "README.en.md",
    "references/orchestration-protocol.md",
    "references/cleanup-policy.md",
    "references/knowledge-preservation.md",
    "references/partitioning-policy.md",
    "references/risk-policy.md",
    "references/verification-policy.md",
    "references/worked-example.md",
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

SUBSKILL_NUMBERS = ["01", "02", "03", "04", "05", "06", "07"]

# Files whose relative references (schemas/*.json, references/*.md) must resolve.
DOC_FILES = [
    ROOT / "SKILL.md",
    *(ROOT / "prompts").glob("*.md"),
    *(ROOT / "references").rglob("*.md"),
]

SCHEMA_REF = re.compile(r"schemas/([\w.-]+\.json)")
REFERENCE_REF = re.compile(r"references/([\w./-]+\.md)")


def main() -> int:
    errors: list[str] = []

    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    errors.extend(f"missing required file: {p}" for p in missing)

    sub_dir = ROOT / "references" / "subskills"
    if sub_dir.is_dir():
        found = sorted(p.name[:2] for p in sub_dir.glob("*.md"))
        if found != sorted(SUBSKILL_NUMBERS):
            errors.append(f"subskill numbering mismatch: found {found}, expected {sorted(SUBSKILL_NUMBERS)}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        errors.append("SKILL.md is missing YAML frontmatter")
    elif "name: repomeld" not in skill or "description:" not in skill:
        errors.append("SKILL.md frontmatter is missing name/description")

    schema_dir = ROOT / "schemas"
    schema_texts: dict[str, str] = {}
    for schema in schema_dir.glob("*.json"):
        try:
            data = json.loads(schema.read_text(encoding="utf-8"))
            schema_texts[schema.name] = json.dumps(data)
        except Exception as exc:
            errors.append(f"invalid JSON schema {schema.name}: {exc}")
            continue
        if "$id" not in data:
            errors.append(f"{schema.name}: missing $id (relative $ref needs an id base)")

    for name, text in schema_texts.items():
        for ref in re.findall(r'"\$ref":\s*"([\w.-]+\.schema\.json)"', text):
            if not (schema_dir / ref).is_file():
                errors.append(f"{name}: $ref target {ref} not found in schemas/")

    for doc in DOC_FILES:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8")
        rel = doc.relative_to(ROOT).as_posix()
        for ref in SCHEMA_REF.findall(text):
            if not (schema_dir / ref).is_file():
                errors.append(f"{rel}: references missing schema schemas/{ref}")
        for ref in REFERENCE_REF.findall(text):
            if not (ROOT / "references" / ref).is_file():
                errors.append(f"{rel}: references missing file references/{ref}")

    if errors:
        print("RepoMeld skill bundle validation: FAILED")
        for e in errors:
            print(" -", e)
        return 1

    print("RepoMeld skill bundle validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
