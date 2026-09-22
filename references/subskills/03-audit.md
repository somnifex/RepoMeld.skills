# Subskill: Audit AI/SDD Residue

Read-only.

Search for:

- S1/S2/M1/M2 and similar implementation-stage markers;
- Phase/Step/Task labels used only as process metadata;
- conversational agent narration;
- verbose comments that restate code;
- temporary plans/reports/status/debug artifacts;
- stale TODO/FIXME markers;
- duplicated rationale;
- one-off helper scripts;
- references to deleted/obsolete development artifacts.

Classify each finding as `delete`, `rewrite`, `preserve`, `relocate`, or `escalate` and assign risk.

Skip text that already reads as durable rationale with no process metadata; it is not a finding (convergence check).

Do not modify files.
