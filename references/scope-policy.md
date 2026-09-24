# Scope Policy

The cleanup scope decides where RepoMeld may find, comment, and modify. It is resolved once, at the start of INIT, and stays frozen for the entire run.

RepoMeld asks the user as little as possible: every decision that can be derived from the invocation, the repository state, or policy is derived. What remains is collected in a single upfront gate; after the gate closes, the run proceeds unattended.

## Upfront gate (INIT, the only interaction point)

After the VCS baseline is captured, ask the user once, in a single batched interaction. Ask only what the invocation has not already determined:

1. **Cleanup scope**:
   - full repository;
   - uncommitted changes only (working-tree modified plus untracked files);
   - files touched in the last N commits (default N=10, or a since-date / branch range);
   - explicit paths or modules;
   - audit-only (no file changes at all).
2. **L3 handling**: pre-authorize runtime dead-code removal for this run (default: no — L3 items are escalated at the end and resolved through the resume protocol).
3. **Execution mode**: auto-apply L0–L2 (default) or audit-only. (Audit-only may also be chosen directly as the scope option above.)

L4/L5 remain forbidden regardless of the answers. Worker counts, comment templates, comment language, and risk classification are never asked; they are policy-derived (see `partitioning-policy.md` and `references/comment-library/`).

### Incomplete-task policy (derived, never asked)

The incomplete-task policy is not part of the gate and is never asked mid-run. It is derived once at INIT from the invocation and recorded in the cleanup plan (see `references/task-completion-policy.md`):

- default `retain`: incomplete/unknown tasks (TODO/FIXME/WIP, stage/task-numbered labels, task plans) stay unfinished with their context fully preserved, and are recorded as unprocessed;
- `verify_by_code`: only when the invocation explicitly asks to check completion against the implementation;
- `process`: only when the invocation explicitly asks to handle incomplete tasks; dispositions still follow the normal risk gates.

Non-interactive runtimes use `retain`. Nothing about tasks is ever asked mid-run.

### When not to ask

- If the invocation already pins the scope ("only clean apps/api", "only my uncommitted changes"), do not ask; restate the derived scope in the plan and report instead.
- If the invocation also pins the L3 stance or execution mode, skip that question.
- If nothing is pinned, ask the gate once. This is the only moment RepoMeld asks anything.
- If the runtime cannot interact with the user, do not block: default to **uncommitted changes only** and record "scope not user-confirmed" as a verification gap in the report.

After the gate closes there are no further questions in any phase. Undetermined items discovered mid-run become escalations, not questions (see `orchestration-protocol.md` failure handling and the Escalation resume protocol in `SKILL.md`).

## Scope semantics

The chosen scope governs finding, mutation, and completeness — it is not a read restriction:

- **DISCOVER** maps the chosen scope; files outside it are only read as dependencies.
- **PARTITION** constructs shards exclusively from in-scope paths.
- **AUDIT** must read every in-scope, non-vendor, non-generated source file and produces findings only for in-scope files. Skipping a file requires a recorded reason that surfaces in the coverage snapshot.
- **APPLY** writes only in-scope files.
- **VERIFY** confirms the final diff touches nothing outside the scope.

Out-of-scope files may be read freely: judging whether a comment is stale and choosing canonical locations for retained knowledge usually requires wider context. Wider reading never becomes wider writing.

### protected_paths semantics

Before a scope is chosen, protected paths means files modified before RepoMeld started. Once the scope is chosen, protection follows the scope: everything outside the chosen scope is frozen for the whole run, and in-scope pre-existing modifications become legitimate targets. For the "uncommitted changes" scope the two sets coincide. Within the scope, user edits that predate RepoMeld must still never be silently reverted or absorbed — comment work goes around them, never over them.

## Scope lifecycle

- The gate answers are restated in the cleanup plan (`scope` field) so verification and reporting can check against the recorded decision, not against memory.
- Mid-run scope expansion is not allowed. If a genuinely out-of-scope, high-value finding appears, it is recorded as a skipped-scope observation (`skipped_scope_findings` in the integration result) or an escalation — never applied.
- A later run with a different scope is a fresh run, not an extension of this one; repeated runs must converge (see `cleanup-policy.md`).
