---
name: repomeld
description: Repository hygiene for codebases built with SDD, coding agents, or vibe coding. Audits and consolidates AI-development traces (stage markers like S1/S2/M1/M2, verbose process comments, temporary plans/reports/scratch files, stale TODOs, abandoned agent artifacts), normalizes comments against per-language template exemplars, and, within a user-chosen scope, adds missing necessary comments (API docs, non-obvious constraints, workarounds). Preserves runtime behavior, durable engineering knowledge, and incomplete tasks (kept unfinished with context, reported as unprocessed unless explicitly requested). Use when the user asks to clean, consolidate, normalize, organize, or remove AI/SDD development traces or messy comments, or to add or enhance necessary code comments. Not for unrelated refactoring, feature work, API/schema changes, dependency upgrades, or behavior changes.
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
13. Collect every user decision once, in the INIT upfront gate. After the gate closes, run unattended: no mid-run questions; undetermined items become escalations resolved through the resume protocol.
14. Incomplete tasks stay incomplete by default: never force-resolve, delete, or strip context from an unfinished work item. Its context is fully preserved and it is reported as unprocessed unless the user explicitly asks to verify or process it.

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

After REPORT, approved escalations may re-enter through the Escalation resume protocol without replaying earlier phases.

Any ambiguous deletion, behavior-sensitive change, ownership conflict, unexplained runtime diff, API/schema/config semantic change, or unexplained validation regression goes to `ESCALATE`, not auto-apply.

## INIT

- Identify repository root and version-control state.
- Capture baseline branch/status/diff when Git or equivalent is available.
- Protect files already modified before RepoMeld began.
- Discover repository-native validation from manifests, build files, CI, contributor docs, and test configuration.
- Avoid creating persistent RepoMeld state inside the repository unless the user explicitly requests it. Prefer in-memory or temporary state.

### Upfront gate

After the baseline is captured, resolve every user decision in one batched interaction following `references/scope-policy.md`: the cleanup scope, L3 pre-authorization, and the execution mode. Ask only what the invocation has not already determined; if the invocation pins everything, do not ask at all. In a non-interactive runtime, default to uncommitted changes only and record "scope not user-confirmed" as a verification gap.

### Incomplete-task policy (derived, never asked)

`incomplete_task_policy` is derived once at INIT and recorded in the cleanup plan; it is never part of the gate and never asked mid-run (`references/task-completion-policy.md`):

- default `retain`: incomplete/unknown tasks stay unfinished with their full context preserved and are reported as unprocessed;
- `verify_by_code`: only when the invocation explicitly asks to check completion by scanning code;
- `process`: only when the invocation explicitly asks to handle incomplete tasks.

Non-interactive runtimes use `retain`.

Once the gate closes, the run proceeds unattended through REPORT. No phase may ask the user anything; undetermined items become escalations handled by the Escalation resume protocol. The chosen scope is frozen: DISCOVER maps it, PARTITION shards it, AUDIT and APPLY stay inside it, VERIFY confirms nothing leaked outside it.

## DISCOVER

Load `references/subskills/01-discover.md`.

For large repositories, delegate read-only discovery when independent areas can be explored in parallel. Discovery workers MUST NOT edit files.

Produce a compact repository map containing:

- applications, packages, services, workspaces, bounded contexts, libraries, tests, docs, infra, generated/vendor areas;
- likely ownership/dependency boundaries;
- repository-native validation commands;
- candidate AI/SDD residue;
- task inventory: task-like markers, task-numbered plan/status artifacts, and one-off task scripts;
- ignored/generated paths;
- pre-existing modified files to protect.

If shell execution is available, `scripts/repomeld_scan.py` may be used as a deterministic read-only aid. Its findings are candidates, never deletion authority. RepoMeld must remain fully functional without the script; native inspection always suffices.

## PARTITION

Load `references/subskills/02-partition.md` and `references/partitioning-policy.md`.

Choose semantic shards dynamically. Preferred order:

1. workspace/package/service boundary;
2. bounded context/domain boundary;
3. dependency/ownership boundary;
4. stable directory boundary;
5. file-count split only as a last resort.

Do not ask the user to choose worker count unless a real external constraint requires it.

Shards are constructed exclusively from paths inside the frozen cleanup scope; out-of-scope areas are read-only dependency context at most.

Determine topology from repository breadth, semantic boundaries, dependency coupling, context footprint, risk, and runtime concurrency.

Heuristics:

- tiny/cohesive repository: primary agent may work directly;
- several independent regions: one worker per meaningful shard;
- many shards: group workers under integrators;
- very large monorepo: recursively group workers under package/domain integrators, then reduce those integrator results at the repository coordinator.

Combine small related shards. Split exceptionally large shards recursively. Avoid tiny workers whose coordination cost exceeds their work.

## AUDIT_FANOUT

Load `references/subskills/03-audit.md`, `references/cleanup-policy.md`, `references/knowledge-preservation.md`, `references/risk-policy.md`, and `references/task-completion-policy.md`.

Audit is strictly read-only.

When a shard contains comments or docs, each audit worker additionally loads `references/comment-library/INDEX.md`, then loads only the library files matching the languages actually detected inside its own shard (normally one to three files, per the INDEX loading table). Never load the whole comment-library directory. Template selection follows `references/comment-library/selection-guide.md`; rewrite and add candidates must name the template they would apply.

Comment scanning is performed by reading code with model file tools, not by scripts. `scripts/repomeld_scan.py` remains an optional aid; its comment-related output is candidate leads only, never decision authority, and RepoMeld stays fully functional without it.

Task-like findings (TODO/FIXME/WIP markers, stage/task-numbered labels, task plans) also receive a completion check per `references/task-completion-policy.md`: classify `task_status` (complete / incomplete / unknown — unknown is handled as incomplete) with `completion_basis`. Under the default `retain` policy, incomplete/unknown tasks are frozen in place and recorded with their full context (intent and remaining work, constraints, continuation point, related artifacts); they become `preserve` findings routed to the plan's `deferred_tasks`, never to `actions`. Only an invocation-authorized `verify_by_code` or `process` policy changes the determination basis or the disposition.

Audit completeness is file-level: every in-scope, non-vendor, non-generated source file must be read, never sampled. Each worker reports `coverage` (files in scope, files audited, skipped with reasons) in its result; the barrier snapshot aggregates it.

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
- deduplicate task-like findings and converge one task reported by several shards into a single record, then route deferred tasks to the plan's `deferred_tasks` with complete context carriers;
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

Comment rewrites are planned as whole-comment-unit transformations, never minimal word-level patches: for each rewrite, the plan references the selected template from `references/comment-library/` and the complete target text of the logical comment block (all lines of the unit in one pass), so mixed half-old half-new blocks never enter the codebase.

Add actions (missing necessary comments) are planned the same way: each names the selected template, the complete text of the new comment unit, and the code facts each slot was filled from. Only necessity triggers from `references/cleanup-policy.md` justify an add.

The plan also records the derived `incomplete_task_policy` and a `deferred_tasks` inventory: every incomplete/unknown task found in scope with its completion basis, context carriers, and the reason it was not processed. Deferred tasks are never planned as actions — they are the record that each was found and intentionally left unfinished, not missed.

For a minimal concrete example of worker results, plan actions, and verification results, see `references/worked-example.md`.

## AUDIT_BARRIER

Do not begin mutation until all required audit groups are complete or explicitly excluded.

Freeze the cleanup plan for the apply epoch. New low-risk observations may be recorded, but do not silently expand scope into risky or cross-owned changes.

Record a structured coverage snapshot at this barrier: shards audited, shards explicitly excluded with reasons, file-level audit coverage per shard, findings deferred as escalations, and the task inventory summary (task-like findings by `task_status`, with the policy in force).

## APPLY_FANOUT

Load `references/subskills/05-apply.md`.

Assign exclusive write ownership by shard. Prefer reusing the same semantic shard topology, but mutation workers receive only accepted plan actions.

Default permissions by risk (summary only; `references/risk-policy.md` is the authoritative definition and must not diverge from it):

- L0 metadata/process-only: auto-apply.
- L1 comment and documentation work (rewrites and additions): auto-apply.
- L2 non-runtime artifact deletion/move: only after reference analysis and policy checks.
- L3 runtime dead-code removal: escalate unless user explicitly authorized it.
- L4 behavior-changing code: forbidden by default.
- L5 API/schema/security/config/dependency semantic changes: forbidden by default.

Workers must not perform unrelated refactors, style cleanup, dependency upgrades, or opportunistic code improvements.

Deferred tasks are frozen: never delete, rewrite, resolve, or relabel an incomplete/unknown task, and never remove or gut the sole context carrier of one. Before deleting or relocating any artifact, confirm it does not carry a deferred task's context; if it does, preserve that context at a canonical location first and record it.

After each shard, run the cheapest relevant local validation.

## APPLY_REDUCE

Integrators review diffs, not entire raw shards unless necessary.

Check:

- stale references to deleted/moved artifacts;
- terminology consistency;
- duplicated rationale;
- accidental cross-scope edits;
- protected baseline changes;
- deferred tasks and their context carriers untouched;
- suspicious runtime-line edits;
- ownership violations.

Integrators may make only explicitly owned low-risk integration edits. Otherwise escalate.

## APPLY_BARRIER

All apply workers/integrators must finish before repository-level verification.

Capture the final diff against the original baseline before verification.

At this barrier, record per-shard action outcomes (applied / skipped / failed) together with the frozen final diff.

## VERIFY

Load `references/subskills/06-verify.md` and `references/verification-policy.md`.

Whenever subagents are available, use a fresh independent verifier from `prompts/verifier.md`. The verifier must not assume worker conclusions are correct.

If only `PRIMARY_ONLY` mode is available, verification cannot be context-independent. Re-read the final diff from disk rather than from memory, challenge each change adversarially, and always record "verification performed by the author in the same context" as a verification gap. Do not use confidence language stronger than this supports.

Verify as applicable:

- final diff against baseline;
- formatting/lint/typecheck;
- unit/integration tests;
- build/package checks;
- deleted-file reference scan;
- API/schema/config/dependency diffs;
- suspicious runtime-line changes;
- unintentional edits to pre-existing modified files;
- deferred incomplete tasks: none was resolved, rewritten, or deleted, and no context carrier was removed or gutted (checked against the plan's `deferred_tasks`);
- every deferred task appears in the report with its preserved context.

Passing tests alone is not proof of semantic equivalence.

## REPORT

Load `references/subskills/07-report.md`.

Report:

- execution mode and topology actually used;
- the recorded cleanup scope and whether it was user-confirmed or the non-interactive default;
- file-level scope coverage (in-scope files audited / skipped with reasons), alongside barrier coverage snapshots (shards audited; shards explicitly excluded with reasons);
- files modified/deleted/moved;
- stage markers and agent narration removed;
- comments/docs normalized and necessary comments added;
- process knowledge converted into durable engineering knowledge;
- task inventory summary, the incomplete-task policy in force, and every deferred (unprocessed) task with its preserved context location;
- validation performed and outcomes;
- unresolved/escalated items;
- whether behavior/API/schema/config/dependency changes were observed;
- verification gaps, if any.

Never claim "no behavior change" when verification was incomplete.

## Escalation resume

Escalated items end the run; they never require a full re-run.

When the user later approves one or more escalated items:

1. Build a delta cleanup plan containing only the approved items, compatible with `schemas/cleanup-plan.schema.json`.
2. Reuse the existing shard topology where possible and give each item a write owner.
3. Apply the same barrier semantics within the delta epoch: no mutation before the delta plan is frozen; no verification before all delta mutations finish.
4. Verify only the affected scopes, then issue a short report addendum with updated verification status.

Items the user rejects are recorded as rejected with the reason. Do not re-audit the whole repository to process a resume.

## Completion criteria

RepoMeld is complete only when:

- the requested repository scope was audited at file level, or every skipped file was reported with a reason;
- accepted cleanup actions were applied or explicitly reported as skipped/escalated;
- the final diff touches nothing outside the frozen cleanup scope;
- deleted artifacts have no unresolved references;
- retained rationale has a durable canonical location;
- every incomplete task in scope was retained unfinished with its context preserved and recorded as deferred, unless the user authorized processing;
- repository-level verification was attempted to the extent supported by the project/runtime;
- final reporting accurately distinguishes verified facts from unverified assumptions.
