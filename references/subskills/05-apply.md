# Subskill: Apply Cleanup

Execute only actions present in the frozen cleanup plan, and only inside the chosen cleanup scope. Treat every out-of-scope path as frozen.

Within the assigned shard:

- remove process-only markers;
- compress redundant comments;
- rewrite mixed process/rationale comments into durable rationale;
- add necessary comments exactly where the plan contains `add` actions: write the complete new comment unit from the cited comment-library template, slots filled only with facts observable in the code; do not add anything the plan does not list;
- delete L2 artifacts only after reference checks;
- never process a deferred task: no delete, rewrite, completion label, or resolution of an incomplete/unknown task;
- before deleting or relocating any artifact, confirm it is not the sole carrier of a deferred task's context; if it is, preserve that context at a canonical location first and record `context_preserved_at`;
- update links/references caused by approved moves/deletions;
- preserve pre-existing unrelated changes.

Do not refactor runtime code merely to make it cleaner.

Run local validation after changes.
