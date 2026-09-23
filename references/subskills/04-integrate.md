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
- add findings touching the same symbol from different shards: converge them into one canonical comment location instead of letting two shards each add their own.

Return compact integration results and unresolved items.
