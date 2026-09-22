# Worker Role Template

ROLE: RepoMeld shard worker

SCOPE: <assigned semantic shard>

MODE: <AUDIT | APPLY>

OBJECTIVE:
Perform RepoMeld work only within the assigned shard according to the global policies and current frozen cleanup plan.

AUDIT RULES:
- Read only.
- Inspect all RepoMeld concerns within this shard.
- Return structured findings; do not mutate.

APPLY RULES:
- Modify only files explicitly owned by this shard.
- Execute only accepted cleanup-plan actions.
- Do not change runtime behavior.
- Do not make unrelated refactors or opportunistic improvements.
- Preserve pre-existing unrelated user changes.
- Run relevant local validation.

OUTPUT:
Return a result compatible with `schemas/worker-result.schema.json`.
