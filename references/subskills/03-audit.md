# Subskill: Audit AI/SDD Residue

Read-only.

Completeness rule: read every in-scope, non-vendor, non-generated source file in the shard. Comment auditing is done by reading, not sampling; a file skipped without a recorded reason is a coverage failure, not a shortcut. Record file-level coverage (`files_in_scope`, `files_audited`, `skipped` with reasons) in the worker result.

Search for:

- S1/S2/M1/M2 and similar implementation-stage markers;
- Phase/Step/Task labels used only as process metadata;
- conversational agent narration;
- verbose comments that restate code;
- contradictory comments on the same declaration;
- temporary plans/reports/status/debug artifacts;
- stale TODO/FIXME markers and other task-like work items (WIP/XXX/HACK, task-numbered labels, task plans);
- duplicated rationale;
- one-off helper scripts;
- references to deleted/obsolete development artifacts;
- missing necessary comments (Add candidate triggers in `references/cleanup-policy.md`: public API without docs, unexplained non-obvious constraints, uncommented workarounds, reason-less suppression directives, undocumented public deprecations).

Classify each finding as `delete`, `rewrite`, `add`, `preserve`, `relocate`, or `escalate` and assign risk.

A missing comment is classified `add` only when a necessity trigger applies; otherwise absence of comments is not a finding (convergence check). `add` findings must cite the comment-library template id and the code facts each slot would be filled from.

Skip text that already reads as durable rationale with no process metadata; it is not a finding (convergence check).

## Task completion check

Every task-like finding carries `task_status` (`complete` / `incomplete` / `unknown` — unknown is handled as incomplete) plus `completion_basis`. The default basis is `plan_artifact`: the task's own declaration and plan/status context. Reading files as part of the mandatory coverage is not completion verification; only systematic checking of implementations, tests, and call sites — authorized by an explicit user request — counts as `code_scan`. If the code immediately surrounding the marker settles completion unambiguously, record that evidence too; otherwise mark `unknown`.

Under the default `retain` policy, an incomplete/unknown task is a `preserve` finding: frozen in place, no rewrite, no deletion, no resolution. Record its full context — intent and definition of done, current state and remaining work, constraints and rationale, continuation point (file/symbol), related artifacts — in `task_context` so the integrator can route it to the plan's `deferred_tasks`. Flag any case where the only carrier of a task's context is itself a delete/relocate candidate.

Produce findings only for files inside the chosen cleanup scope; out-of-scope observations go back to the integrator as skipped-scope notes.

Do not modify files.
