# Partitioning Policy

## Goal

Create independent, semantically coherent shards that minimize cross-worker mutation conflicts and context duplication.

## Preferred boundaries

1. workspace/package/service;
2. bounded context/domain;
3. ownership/dependency boundary;
4. stable directory boundary;
5. file-count chunk only as a last resort.

## Anti-patterns

Do not partition globally by operation type, for example:

- one agent cleans comments everywhere;
- one agent cleans TODOs everywhere;
- one agent deletes artifacts everywhere.

That creates overlapping write ownership.

Instead, assign a shard worker all RepoMeld capabilities within its owned scope.

## Dynamic sizing

Do not hardcode worker count.

Combine small related components. Split a huge component recursively if it contains independent submodules.

Consider:

- package count;
- dependency coupling;
- path breadth;
- likely finding volume;
- test/build boundaries;
- runtime context limits;
- available concurrency.

## Dependency awareness

A worker may read direct dependencies outside its shard when necessary, but must not mutate them unless ownership is explicitly transferred.
