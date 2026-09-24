# Cleanup Policy

RepoMeld performs five kinds of actions on comments, docs, and artifacts: delete, rewrite, add, remove, and preserve/relocate. This file defines when each applies.

## Delete candidates (files and artifacts)

Examples of process-only residue:

- temporary planning/status/verification files that are no longer referenced;
- agent scratch files and debug outputs;
- milestone/stage trackers whose information is fully obsolete;
- duplicated generated summaries with no canonical role;
- temporary scripts created only for a completed one-off analysis.

Deletion is never justified by filename alone.

## Rewrite candidates

Normalize comments or docs that contain durable meaning mixed with process metadata.

Example:

Before:
`// M2: We changed this to sequential calls after parallel calls broke the vendor API.`

After:
`// Keep vendor writes sequential; the upstream API does not support concurrent mutations.`

Also rewrite: contradictory comments on the same declaration — merge into one block that matches the code's actual behavior (see `references/comment-library/rewrite-recipes.md` R10); escalate when the code cannot settle which statement is correct.

## Add candidates (necessary comments)

A missing comment is not a finding by itself. Add a comment only when a necessity trigger applies:

- a public/exported API lacks a documentation comment (library code by default; application/script code follows repository convention and is not proactively documented);
- a non-obvious constraint, invariant, or sentinel value is unexplained (e.g. "-1 means unknown");
- an active workaround carries no comment (the comment must include the upstream issue link and the removal condition);
- a suppression directive lacks a reason where the language supports one (recipe R8);
- a public deprecation has no deprecation marker.

Not necessary — never add: comments restating signatures or obvious behavior, private implementation details, documentation for vendored/generated code, speculative "might be useful later" notes.

Every addition must cite a template from `references/comment-library/` and fill its slots only with facts observable in the code. Additions follow the same whole-unit rule as rewrites: the complete comment unit is written in one pass. Additions are L1, like rewrites.

## Remove candidates

Remove comments that merely narrate obvious code or agent steps, for example:

- "Now iterate through every user" directly above a self-explanatory loop;
- "Step 3" / "Phase 2" / "M1" labels with no durable meaning;
- "As discussed above" / "we now need to" process narration;
- explanations that only restate the next line of code;
- tutorial-style docstrings that add nothing beyond the signature ("This function takes two numbers and adds them together and returns the result.");
- journal/attribution comments ("Modified by John 2023-05-01") — version control history carries this;
- commented-out code (including commented-out blocks in HTML/CSS/SQL), unless it is load-bearing (see the comment-library load-bearing lists).

## Comment template library

When rewriting or adding comments, do not let the model invent a style. Select a template:

1. Load `references/comment-library/INDEX.md`.
2. Load only the library files matching the languages present in the shard (per the INDEX loading table); never the whole directory.
3. Choose a template from the matching language file, fill its slots from the code's actual behavior, and write the entire logical comment unit in one pass.

Minimal word-level patching is forbidden: partial rewrites leave mixed styles and broken context inside one comment block. Each rewrite or addition produces the complete final text of the unit at once, and must not touch code lines.

Repo conventions override library defaults: if the shard already uses one consistent style (e.g. NumPy-style docstrings, kernel-style C comments), keep it; style differences alone are never findings. Load-bearing comments (license/SPDX headers, generated-file markers, build/compiler directives, suppression directives, doctests, magic comments) are preserved unchanged and handled via escalation when suspect.

## Preserve candidates

Preserve or relocate:

- non-obvious business rules;
- protocol and interoperability constraints;
- security reasoning;
- compatibility workarounds;
- performance tradeoffs;
- ordering/idempotency requirements;
- operational caveats;
- intentional deviations from common patterns.

## TODO/FIXME and task-like findings

Task-like findings (TODO/FIXME/WIP markers, stage/task-numbered labels, task plans, one-off task scripts) follow `references/task-completion-policy.md`:

- never delete a TODO/FIXME solely because it looks stale;
- check completion first: `complete`, `incomplete`, or `unknown` — `unknown` is handled as `incomplete`;
- under the default `retain` policy, incomplete/unknown tasks are `preserve` findings: frozen in place, never force-resolved, with their full context recorded and reported as unprocessed;
- a completed task may be removed only when the evidence required for deletion (see the delete rules above) actually proves completion; otherwise keep or normalize it;
- processing incomplete tasks at all requires the run's `incomplete_task_policy` to authorize it — resolving one without authorization escalates (see `references/risk-policy.md`).

## Convergence rule

Text that already reads as durable rationale and contains no process metadata is not a finding, even if RepoMeld could phrase it differently.

A missing comment is a finding only when an Add candidate trigger applies; otherwise absence of comments is never actionable.

If a candidate is already in the form RepoMeld would produce, leave it unchanged.

Repeated runs must converge: never rephrase already-normalized text, never re-add a comment that a previous run already added in template form, and never introduce new process metadata while cleaning.
