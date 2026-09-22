# Subskill: Verify Repository

Prefer a fresh independent context.

Review final diff against baseline and cleanup plan.

Check for behavior-sensitive edits, contract/config/schema/dependency changes, broken references, lost rationale, and unexpected modifications to protected paths.

Run repository-native validation when feasible.

Return a result compatible with `schemas/verification-result.schema.json`: `verified`, `failed`, or `incomplete` with evidence and gaps.
