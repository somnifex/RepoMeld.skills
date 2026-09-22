# Subskill: Partition Repository

Goal: construct a useful orchestration topology.

Partition by semantic ownership. Prefer module/package/service boundaries.

For each shard record:

- shard id;
- owned paths;
- read-only dependency paths if needed;
- expected size/complexity;
- mutation owner;
- local validation commands.

If result count is large, group related shards under an integrator.
