# Subskill: Discover Repository

Goal: build a compact repository map before any cleanup decision, and supply the inputs the upfront scope gate needs.

Inspect root manifests, workspace declarations, build/test configs, CI, directory structure, docs, ignore rules, and current VCS status.

Capture the scope-gate inputs from the VCS state (read-only VCS commands, not scripts):

- uncommitted working-tree files (modified + untracked);
- recently touched files (last N commits / since-date / branch range), so the gate can offer concrete scope options without re-scanning.

Identify generated/vendor directories and avoid expensive deep scanning there unless explicitly relevant.

For large repositories, delegate independent read-only exploration of apps/packages/tests/docs/infra.

Once the user answers the upfront gate (`references/scope-policy.md`), the repository map covers the chosen scope; out-of-scope areas are only mapped as read-only dependency context.

Return:

- repository root;
- project languages/toolchains;
- semantic modules;
- validation commands;
- protected pre-existing modified paths;
- scope-gate inputs (uncommitted summary, recent-commit file set);
- candidate residue locations;
- task inventory: task-like markers, task-numbered plan/status artifacts, and one-off task scripts, each noted with whether completion is determinable from its own plan/artifact context;
- uncertainty notes.

The task inventory feeds the completion check in `references/task-completion-policy.md`. Default runs judge completion from plan/artifact context only — do not scan implementations to verify completion unless the user explicitly asked for it.
