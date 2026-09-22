# Worker Role Template

ROLE: RepoMeld shard worker

SCOPE: <assigned semantic shard>

MODE: <AUDIT | APPLY>

OBJECTIVE:
Perform RepoMeld work only within the assigned shard according to global policies and, for APPLY, the frozen cleanup plan.

READ:
- The entire assigned shard.
- Directly relevant dependency files and manifests outside the shard, read-only.

WRITE:
- AUDIT: nothing. Audit is strictly read-only.
- APPLY: only files explicitly owned by this shard in the frozen cleanup plan.

DO NOT:
- Change runtime behavior.
- Refactor, restyle, or improve anything unrelated to accepted plan actions.
- Touch pre-existing unrelated user changes.
- Delete uncertain artifacts; escalate instead.
- Modify files outside the assigned ownership.

OUTPUT:
Return a result compatible with `schemas/worker-result.schema.json`.
A minimal example is in `references/worked-example.md`.
