# Task Completion Policy

Scanning finds unfinished work as well as residue. This file defines how RepoMeld determines whether a discovered task is finished, and what happens to unfinished ones.

## Task-like findings

A finding is task-like when its subject is a unit of work that may still be pending:

- TODO / FIXME / WIP / XXX / HACK markers and their equivalents in any language;
- S1/S2/M1/M2 stage markers and Phase/Step/Task-numbered labels that track planned work;
- temporary plans, status reports, and task lists describing work to be done;
- one-off scripts or artifacts created for a specific task.

Task-like findings receive a completion check before any disposition is decided.

## Completion status

Every task-like finding carries `task_status`:

- `complete` — the task's own plan/status artifact, or unambiguous evidence at the task's own site, proves the work landed;
- `incomplete` — evidence shows work remains, or the plan still marks the task pending;
- `unknown` — completion cannot be determined. `unknown` is handled exactly like `incomplete`.

`completion_basis` records how the status was determined:

- `plan_artifact` — the default. Status is read from the task's own declaration, plan, or status context. Default runs do not perform completion verification against implementations.
- `code_scan` — only when the user explicitly authorized scanning code. Implementation, test, and reference evidence may settle completion.
- `undetermined` — no usable basis (counts as incomplete).

Under the default basis, reading code as part of the mandatory file-level audit is not "scanning code to check completion": only systematic verification across implementations, tests, and call sites counts as `code_scan`. If the code immediately surrounding the marker settles completion unambiguously, record that evidence; otherwise mark `unknown`.

## Policy (derived, never asked)

`incomplete_task_policy` is derived once at INIT, recorded in the cleanup plan, and restated in the report. It is never a gate question and is never asked mid-run:

1. `retain` (default): incomplete/unknown tasks are left unfinished and marked unprocessed. Completion is judged from plan/artifact context only.
2. `verify_by_code`: the invocation explicitly asks to check completion against the implementation. Completed tasks then follow the normal finding flow; incomplete/unknown tasks still default to `retain`.
3. `process`: the invocation explicitly asks to handle incomplete tasks. They may be normalized, relocated, or removed like ordinary findings — still risk-gated (L0–L2, escalate on ambiguity).

Explicit invocation phrasing pins the policy ("also handle the unfinished TODOs", "check completion by scanning the code"). Absent such phrasing, the policy is always `retain`. Non-interactive runtimes use `retain`.

## Incomplete tasks: default disposition (retain)

Under `retain`:

- the marker or artifact is frozen in place: no delete, no rewrite, no completion label, no code change to resolve it;
- it is recorded in the plan's `deferred_tasks` with its completion basis and its context carriers;
- it is reported as explicitly unprocessed — never silently dropped;
- repeated runs leave it byte-identical (convergence).

A deferred task is not an escalation: it requires no user decision to be valid. It is the run's honest record of "found, unfinished, intentionally left unfinished" — not "missed".

## Context preservation for deferred tasks

"Left unfinished" must not mean "left unexplained". Every deferred task carries enough context for a future maintainer — or a later authorized run — to resume the work:

- the task's intent and what "done" means;
- the current state and what remains;
- constraints, rationale, and any linked design notes attached to the task;
- the continuation point — the file and symbol where work resumes;
- related references and artifacts (plan docs, issues, helper scripts).

Rules:

1. The sole context carrier of a deferred task may never be deleted or gutted. A delete/relocate candidate whose content is the only home of a deferred task's context is blocked until that context is preserved at a canonical location, and the finding records `context_preserved_at`.
2. Extracting durable knowledge from an artifact never consumes its task record: if an artifact carries both reusable rationale and an unfinished task, the rationale may be relocated while the task context stays.
3. Context carriers are recorded in `task_context` on the finding and `context_refs` in the plan, so verification can check them.
4. If the user later authorizes processing, the deferred record — with its preserved context — is the input to the delta plan. No re-audit of the repository is needed.

## Authorized processing (verify_by_code / process)

Only under an explicit user request may incomplete tasks be acted on:

- `verify_by_code` changes the evidence basis for completion, nothing else: incomplete/unknown tasks still default to `retain` unless the policy is `process`.
- `process` permits normalization, relocation, or deletion of incomplete-task artifacts under the normal risk gates (L0–L2). Deleting an incomplete task's artifact requires the same evidence as any L2 deletion. If completion or ownership of the task cannot be settled, escalate.

## Interaction with existing policy

- The TODO/FIXME rules in `references/cleanup-policy.md` are the task-like subset of this policy.
- Resolving an incomplete task without authorization follows the escalation rule in `references/risk-policy.md`.
- Deferred task context is durable engineering knowledge under `references/knowledge-preservation.md`.
- Verification checks for deferred tasks live in `references/verification-policy.md`.
