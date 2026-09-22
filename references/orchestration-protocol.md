# Runtime-Agnostic Orchestration Protocol

## Purpose

This protocol lets RepoMeld express multi-agent coordination without binding to vendor APIs or tool names.

The host runtime is responsible for mapping logical roles to whatever it provides: subagents, child sessions, task delegation, background workers, or equivalent mechanisms.

## Logical operations

- `DELEGATE(role, scope, instructions)`: create an isolated work unit.
- `WAIT(tasks)`: synchronize on required work units.
- `COLLECT(tasks)`: retrieve structured results.
- `REDUCE(results)`: consolidate many results into a smaller result set.
- `VERIFY(changes)`: independently review the resulting repository state.

Never treat these names as required literal tools.

## Capability preference

1. Native concurrent subagents.
2. Native sequential subagents.
3. Direct primary-agent execution.

The workflow semantics must remain the same across all modes.

## When to delegate

Delegate when one or more conditions apply:

- multiple repository regions can be inspected independently;
- the repository contains multiple packages/services/workspaces/domains;
- an individual context would otherwise become excessively large;
- isolated review improves confidence;
- independent workstreams do not require shared mutable state.

Do not delegate when:

- only a few tightly coupled files are involved;
- the work is inherently sequential;
- workers would need overlapping write ownership;
- coordination overhead exceeds expected work;
- a direct grep/read/edit is clearly simpler.

## Parallelism policy

Use the highest useful parallelism, not maximum available parallelism.

Prefer a small number of coherent workers over many tiny workers.

Never parallelize dependent tasks merely for speed.

## Hierarchical reduction

If the parent can safely consume all worker results, integrate directly.

If result volume or context size becomes large, reduce results hierarchically. Treat the hierarchy as nested ownership, not as a visual diagram:

- Root Coordinator
  - Domain Integrator A
    - Local Integrator A1, when needed
      - Worker results for shard group A1
    - Local Integrator A2, when needed
      - Worker results for shard group A2
  - Domain Integrator B
    - Worker results for shard group B

Not every level is mandatory. Use the shallowest hierarchy that keeps each integration context bounded. Integrators should consume compact structured results and diffs, not blindly re-read the entire repository.

## Context isolation

A worker receives the minimum useful context:

- global RepoMeld policies;
- repository summary;
- assigned scope;
- directly relevant dependencies/ADRs;
- task contract and result schema.

Do not flood workers with unrelated repository contents or other workers' raw transcripts.

## Mutation ownership

During APPLY, a file has exactly one write owner.

Read overlap is allowed. Write overlap is not.

Cross-scope changes must be returned to the coordinator for reassignment or escalation.

## Synchronization

### Audit barrier

No mutation until required audit work and reduction have completed and a cleanup plan exists.

### Apply barrier

No repository-level verification until required mutation and integration work has completed.

## Independent verification

When child contexts are available, the final verifier must be newly delegated and must not have authored the reviewed changes.

The verifier receives the plan, final diff/state, validation evidence, and policies. It must challenge worker conclusions rather than endorse them by default.

## Failure and fallback

If a delegated task fails:

- retry only when failure is transient and safe;
- otherwise reassign to the parent or another worker;
- do not silently omit the scope;
- report incomplete coverage.

If subagents are unavailable, simulate the same phases sequentially in the primary context.
