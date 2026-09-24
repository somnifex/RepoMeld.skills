# Risk Policy

This file is the authoritative definition of the L0-L5 levels and their default permissions. SKILL.md carries only a summary and must not diverge from it.

## L0 — Process metadata only

Examples: stage labels, agent narration, obsolete status metadata.

Default: auto-apply.

## L1 — Comments and documentation

No runtime semantic effect expected.

Default: auto-apply after preserving durable knowledge.

## L2 — Non-runtime artifact deletion or relocation

Examples: unreferenced scratch reports, stale temporary plans, generated analysis residue.

Default: apply only after reference scan, content review, and repository-convention check.

## L3 — Runtime-source cleanup

Examples: dead debug helper, unused runtime branch, unreachable helper.

Default: escalate. Do not auto-apply unless explicitly authorized.

## L4 — Behavior changes

Any control-flow, algorithmic, data-processing, error-handling, concurrency, or runtime-semantic change.

Default: forbidden for RepoMeld.

## L5 — Contract/security/system-semantic changes

API, schema, dependency, permission, security policy, persistent configuration semantics, migration semantics.

Default: forbidden for RepoMeld.

## Uncertainty rule

If risk classification is uncertain, choose the higher risk level.

## Incomplete tasks

Resolving an incomplete task — deleting it, marking it complete, rewriting it away, or removing the sole carrier of its context — without the user's explicit authorization is treated like an L3 change: escalate, never auto-apply. With authorization recorded as the run's `incomplete_task_policy`, processing follows the normal risk levels above (see `references/task-completion-policy.md`).
