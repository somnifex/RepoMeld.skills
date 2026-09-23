# Subskill: Apply Cleanup

Execute only actions present in the frozen cleanup plan, and only inside the chosen cleanup scope. Treat every out-of-scope path as frozen.

Within the assigned shard:

- remove process-only markers;
- compress redundant comments;
- rewrite mixed process/rationale comments into durable rationale;
- add necessary comments exactly where the plan contains `add` actions: write the complete new comment unit from the cited comment-library template, slots filled only with facts observable in the code; do not add anything the plan does not list;
- delete L2 artifacts only after reference checks;
- update links/references caused by approved moves/deletions;
- preserve pre-existing unrelated changes.

Do not refactor runtime code merely to make it cleaner.

Run local validation after changes.
