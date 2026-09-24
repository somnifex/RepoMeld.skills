# Subskill: Integrate Findings

Consume worker results rather than re-performing all scans.

Check:

- duplicates;
- inconsistent classifications;
- terminology drift;
- cross-shard references;
- ownership conflicts;
- canonical location for retained rationale;
- risk escalation;
- out-of-scope findings: record them as `skipped_scope_findings` for the report; never plan actions for them;
- add findings touching the same symbol from different shards: converge them into one canonical comment location instead of letting two shards each add their own;
- one task-like finding reported by several shards: converge into a single record with one continuation point;
- deferred tasks: route every incomplete/unknown task to `deferred_tasks` with complete `task_context`; never promote a deferred task into an action without an authorizing `incomplete_task_policy`.

Return compact integration results and unresolved items.
