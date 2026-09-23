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
- stale TODO/FIXME markers;
- duplicated rationale;
- one-off helper scripts;
- references to deleted/obsolete development artifacts;
- missing necessary comments (Add candidate triggers in `references/cleanup-policy.md`: public API without docs, unexplained non-obvious constraints, uncommented workarounds, reason-less suppression directives, undocumented public deprecations).

Classify each finding as `delete`, `rewrite`, `add`, `preserve`, `relocate`, or `escalate` and assign risk.

A missing comment is classified `add` only when a necessity trigger applies; otherwise absence of comments is not a finding (convergence check). `add` findings must cite the comment-library template id and the code facts each slot would be filled from.

Skip text that already reads as durable rationale with no process metadata; it is not a finding (convergence check).

Produce findings only for files inside the chosen cleanup scope; out-of-scope observations go back to the integrator as skipped-scope notes.

Do not modify files.
