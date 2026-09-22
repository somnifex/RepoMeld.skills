# Subskill: Discover Repository

Goal: build a compact repository map before any cleanup decision.

Inspect root manifests, workspace declarations, build/test configs, CI, directory structure, docs, ignore rules, and current VCS status.

Identify generated/vendor directories and avoid expensive deep scanning there unless explicitly relevant.

For large repositories, delegate independent read-only exploration of apps/packages/tests/docs/infra.

Return:

- repository root;
- project languages/toolchains;
- semantic modules;
- validation commands;
- protected pre-existing modified paths;
- candidate residue locations;
- uncertainty notes.