# Subskill: Report

Produce a concise engineering report containing:

- execution mode/topology;
- the recorded cleanup scope (mode plus parameters) and whether it was user-confirmed or the non-interactive default;
- scope coverage: file-level counts (in-scope files audited / skipped with reasons), alongside barrier coverage snapshots (shards audited; shards explicitly excluded with reasons);
- counts and representative categories of changes, including comments rewritten and comments added;
- knowledge retained/relocated;
- task inventory: task-like findings by `task_status`, the incomplete-task policy in force and whether it was user-authorized, and the deferred (unprocessed) tasks with their preserved context locations;
- files deleted/moved;
- validation results;
- escalated/unresolved findings;
- behavior/API/schema/config/dependency impact statement;
- verification gaps, including "scope not user-confirmed" when the run defaulted to uncommitted changes without asking.

For approved escalations processed through the resume protocol, issue a short report addendum instead of a full report.
