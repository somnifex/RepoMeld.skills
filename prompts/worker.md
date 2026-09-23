# Worker Role Template

ROLE: RepoMeld shard worker

SCOPE: <assigned semantic shard>

MODE: <AUDIT | APPLY>

OBJECTIVE:
Perform RepoMeld work only within the assigned shard — and only inside the chosen cleanup scope — according to global policies and, for APPLY, the frozen cleanup plan.

READ:
- The entire assigned shard.
- Directly relevant dependency files and manifests outside the shard, read-only.
- AUDIT (comments/docs present): `references/comment-library/INDEX.md`, then only the library files matching the languages detected in this shard per the INDEX loading table (normally 1-3 files). Never load the whole comment-library directory. If rewrites or additions are planned, also read `references/comment-library/selection-guide.md` and `references/comment-library/rewrite-recipes.md`.

COMMENTS:
- Perform comment scanning by reading code with file tools; do not rely on scripts.
- AUDIT: read every in-scope, non-vendor, non-generated source file in the shard; do not sample. Record file-level coverage in the result (`coverage`: files_in_scope, files_audited, skipped with reasons).
- New or rewritten comments must use a template from the matching library file (cite the template id in findings and plans); fill slots with facts observed in the code, never invented ones.
- Classify missing-comment candidates as `add` findings only when a necessity trigger from `references/cleanup-policy.md` applies (public API without docs, non-obvious constraint, workaround, reason-less suppression, undocumented deprecation); cite the template id and the code facts for each slot.
- Rewrite the entire logical comment unit in one pass; write additions as complete units the same way. Word-by-word minimal patching is forbidden. Do not modify code lines while rewriting comments.
- Preserve load-bearing comments (INDEX global list + language file lists) unchanged; suspect ones escalate.

WRITE:
- AUDIT: nothing. Audit is strictly read-only.
- APPLY: only files explicitly owned by this shard in the frozen cleanup plan.

DO NOT:
- Change runtime behavior.
- Refactor, restyle, or improve anything unrelated to accepted plan actions.
- Touch pre-existing unrelated user changes.
- Produce findings or edits outside the chosen cleanup scope; report out-of-scope observations instead of acting on them.
- Add comments that the frozen plan does not list.
- Delete uncertain artifacts; escalate instead.
- Modify files outside the assigned ownership.

OUTPUT:
Return a result compatible with `schemas/worker-result.schema.json`.
A minimal example is in `references/worked-example.md`.
