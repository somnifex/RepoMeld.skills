# Knowledge Preservation

RepoMeld removes execution context, not engineering knowledge.

## Conversion rule

Convert:

`process statement -> durable reason/constraint`

Examples:

- "M3 added retries because production was flaky" -> document the specific transient failure contract.
- "S2 temporary workaround" -> preserve the compatibility condition if it is still active.
- "Phase 4 changed ordering" -> document the required ordering and why it matters.

## Canonical location

Place knowledge where future maintainers will naturally need it:

- local implementation invariant -> code comment;
- public/user behavior -> user/developer documentation;
- architectural decision -> ADR/design doc;
- test-specific rationale -> test comment;
- operational constraint -> runbook/config documentation.

Avoid duplicating the same rationale across many locations.

## Compression

Prefer concise, testable statements over conversational history.

Bad:
"After trying multiple approaches in M2 and discussing the issue, we eventually realized that..."

Good:
"Writes are serialized because the upstream endpoint rejects concurrent mutations."
