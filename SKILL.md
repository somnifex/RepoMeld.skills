---
name: repomeld
description: Self-orchestrating repository hygiene for software projects developed with SDD, coding agents, or vibe coding. Audit and consolidate AI-development traces such as S1/S2/M1/M2 stage markers, verbose process comments, temporary plans/reports/scratch files, stale TODOs, duplicated rationale, and abandoned agent artifacts while preserving durable engineering knowledge and observable behavior. Use when the user asks to clean, consolidate, normalize, or remove AI/SDD development traces from a repository. Do not use as a justification for unrelated refactoring, feature work, API changes, schema changes, dependency upgrades, or behavior changes.
---

# RepoMeld

RepoMeld turns a repository containing accumulated agent/SDD process residue into a maintainable engineering repository without intentionally changing product behavior.

RepoMeld is runtime-agnostic. It describes logical orchestration, not vendor-specific APIs. When the host exposes native subagents, delegation, child sessions, or parallel workers, use those capabilities directly. Do not require a particular tool name such as `spawn_agent`, `Task`, or `subagent`.

## Non-negotiable invariants

1. Preserve observable runtime behavior unless the user explicitly expands scope.
2. Preserve durable engineering knowledge: design rationale, protocol constraints, safety boundaries, compatibility requirements, performance assumptions, business rules, and non-obvious operational constraints.
3. Remove or normalize execution metadata: milestone labels, S1/S2/M1/M2 markers, phase narration, agent chatter, scratch artifacts, temporary verification reports, stale generated notes, and redundant explanations.
4. Never overwrite, revert, or absorb unrelated pre-existing user changes.
5. Audit before mutation. Do not opportunistically edit during discovery.
6. During mutation, every file has exactly one write owner per epoch.
7. Partition by semantic/ownership boundary, not by cleanup operation type.
8. Prefer independent verification by a context that did not author the changes.
9. Deletion requires stronger evidence than comment rewriting.
10. Transformations must be idempotent: repeated RepoMeld runs should converge, not keep rephrasing text.
11. Use the host's highest useful parallelism, not its maximum possible parallelism.
12. Do not fail merely because subagents are unavailable; degrade to sequential execution while preserving the same workflow semantics.

## Runtime capability discovery

Before repository work, determine from the currently available tools/runtime whether you can:

- delegate tasks to independent subagents or child sessions;
- execute independent delegated tasks concurrently;
- wait for required delegated tasks and collect their results;
- give child agents isolated instructions/context;
- use read-only versus write-capable delegation;
- inspect files, run shell commands, and run repository-native validation.

Do not ask the user which vendor/runtime is active if capabilities are already visible.

Classify execution mode internally:

- `PARALLEL_NATIVE`: independent subagents can run concurrently.
- `SEQUENTIAL_NATIVE`: subagents exist but effective parallelism is unavailable or unsuitable.
- `PRIMARY_ONLY`: no usable subagent mechanism exists.

Map RepoMeld's logical operations to whatever native mechanisms exist:

`DELEGATE(role, scope, instructions)`
`WAIT(required_tasks)`
`COLLECT(results)`
`REDUCE(results)`
`VERIFY(changes)`

These are conceptual operations, not literal commands.

Load `references/orchestration-protocol.md` before creating the execution topology.

## Workflow state machine

Run these phases in order unless the user narrows scope:

1. `INIT`
2. `DISCOVER`
3. `PARTITION`
4. `AUDIT_FANOUT`
5. `AUDIT_REDUCE`
6. `PLAN`
7. `AUDIT_BARRIER`
8. `APPLY_FANOUT`
9. `APPLY_REDUCE`
10. `APPLY_BARRIER`
11. `VERIFY`
12. `REPORT`

`AUDIT_FANOUT` and `APPLY_FANOUT` may execute independent shards concurrently. Reduction may be hierarchical. Barriers are global synchronization points and cannot be bypassed.

Any ambiguous deletion, behavior-sensitive change, ownership conflict, unexplained runtime diff, API/schema/config semantic change, or unexplained validation regression goes to `ESCALATE`, not auto-apply.

## INIT

- Identify repository root and version-control state.
- Capture baseline branch/status/diff when Git or equivalent is available.
- Protect files already modified before RepoMeld began.
- Discover repository-native validation from manifests, build files, CI, contributor docs, and test configuration.
- Avoid creating persistent RepoMeld state inside the repository unless the user explicitly requests it. Prefer in-memory or temporary state.

## DISCOVER

Load `references/subskills/01-discover.md`.

For large repositories, delegate read-only discovery when independent areas can be explored in parallel. Discovery workers MUST NOT edit files.

Produce a compact repository map containing:

- applications, packages, services, workspaces, bounded contexts, libraries, tests, docs, infra, generated/vendor areas;
- likely ownership/dependency boundaries;
- repository-native validation commands;
- candidate AI/SDD residue;
- ignored/generated paths;
- pre-existing modified files to protect.

If shell execution is available, `scripts/repomeld_scan.py` may be used as a deterministic read-only aid. Its findings are candidates, never deletion authority.

## PARTITION

Load `references/subskills/02-partition.md` and `references/partitioning-policy.md`.

Choose semantic shards dynamically. Preferred order:

1. workspace/package/service boundary;
2. bounded context/domain boundary;
3. dependency/ownership boundary;
4. stable directory boundary;
5. file-count split only as a last resort.

Do not ask the user to choose worker count unless a real external constraint requires it.

Determine topology from repository breadth, semantic boundaries, dependency coupling, context footprint, risk, and runtime concurrency.

Heuristics:

- tiny/cohesive repository: primary agent may work directly;
- several independent regions: one worker per meaningful shard;
- many shards: group workers under integrators;
- very large monorepo: recursively group workers under package/domain integrators, then reduce those integrator results at the repository coordinator.

Combine small related shards. Split exceptionally large shards recursively. Avoid tiny workers whose coordination cost exceeds their work.

## AUDIT_FANOUT

Load `references/subskills/03-audit.md`, `references/cleanup-policy.md`, `references/knowledge-preservation.md`, and `references/risk-policy.md`.

Audit is strictly read-only.

When delegation is useful, create independent audit workers from `prompts/worker.md`. Give each worker only:

- global policies;
- repository summary;
- assigned shard;
- directly relevant dependency/ADR context;
- the structured result contract.

Each worker audits all RepoMeld concerns within its shard rather than assigning separate global Comment/TODO/Artifact agents.

Workers return `schemas/worker-result.schema.json` compatible results.

## AUDIT_REDUCE

Load `references/subskills/04-integrate.md`.

If only a few worker results exist, the coordinator may integrate directly. If aggregation would overload the primary context, delegate hierarchical integrators using `prompts/integrator.md`.

Integrators:

- deduplicate findings;
- reject scope leakage;
- detect cross-file and cross-shard references;
- normalize terminology;
- distinguish process residue from durable engineering knowledge;
- identify canonical locations for retained knowledge;
- surface ownership conflicts and high-risk changes;
- return compact structured summaries.

Repeat reduction recursively if needed.

## PLAN

Build a repository-wide cleanup plan compatible with `schemas/cleanup-plan.schema.json`.

Every planned action must include:

- target scope/file;
- finding category;
- intended transformation;
- preservation rationale when knowledge is retained or moved;
- risk level;
- reference/dependency evidence for deletions;
- designated write owner;
- required verification.

## AUDIT_BARRIER

Do not begin mutation until all required audit groups are complete or explicitly excluded.

Freeze the cleanup plan for the apply epoch. New low-risk observations may be recorded, but do not silently expand scope into risky or cross-owned changes.

## APPLY_FANOUT

Load `references/subskills/05-apply.md`.

Assign exclusive write ownership by shard. Prefer reusing the same semantic shard topology, but mutation workers receive only accepted plan actions.

Default permissions by risk:

- L0 metadata/process-only: auto-apply.
- L1 comment/documentation normalization: auto-apply.
- L2 non-runtime artifact deletion/move: only after reference analysis and policy checks.
- L3 runtime dead-code removal: escalate unless user explicitly authorized it.
- L4 behavior-changing code: forbidden by default.
- L5 API/schema/security/config/dependency semantic changes: forbidden by default.

Workers must not perform unrelated refactors, style cleanup, dependency upgrades, or opportunistic code improvements.

After each shard, run the cheapest relevant local validation.

## APPLY_REDUCE

Integrators review diffs, not entire raw shards unless necessary.

Check:

- stale references to deleted/moved artifacts;
- terminology consistency;
- duplicated rationale;
- accidental cross-scope edits;
- protected baseline changes;
- suspicious runtime-line edits;
- ownership violations.

Integrators may make only explicitly owned low-risk integration edits. Otherwise escalate.

## APPLY_BARRIER

All apply workers/integrators must finish before repository-level verification.

Capture the final diff against the original baseline before verification.

## VERIFY

Load `references/subskills/06-verify.md` and `references/verification-policy.md`.

Whenever subagents are available, use a fresh independent verifier from `prompts/verifier.md`. The verifier must not assume worker conclusions are correct.

Verify as applicable:

- final diff against baseline;
- formatting/lint/typecheck;
- unit/integration tests;
- build/package checks;
- deleted-file reference scan;
- API/schema/config/dependency diffs;
- suspicious runtime-line changes;
- unintentional edits to pre-existing modified files.

Passing tests alone is not proof of semantic equivalence.

## REPORT

Load `references/subskills/07-report.md`.

Report:

- execution mode and topology actually used;
- scopes/shards processed;
- files modified/deleted/moved;
- stage markers and agent narration removed;
- comments/docs normalized;
- process knowledge converted into durable engineering knowledge;
- validation performed and outcomes;
- unresolved/escalated items;
- whether behavior/API/schema/config/dependency changes were observed;
- verification gaps, if any.

Never claim "no behavior change" when verification was incomplete.

## Completion criteria

RepoMeld is complete only when:

- the requested repository scope was audited;
- accepted cleanup actions were applied or explicitly reported as skipped/escalated;
- deleted artifacts have no unresolved references;
- retained rationale has a durable canonical location;
- repository-level verification was attempted to the extent supported by the project/runtime;
- final reporting accurately distinguishes verified facts from unverified assumptions.
