# Subskill: Apply Cleanup

Execute only actions present in the frozen cleanup plan.

Within the assigned shard:

- remove process-only markers;
- compress redundant comments;
- rewrite mixed process/rationale comments into durable rationale;
- delete L2 artifacts only after reference checks;
- update links/references caused by approved moves/deletions;
- preserve pre-existing unrelated changes.

Do not refactor runtime code merely to make it cleaner.

Run local validation after changes.
