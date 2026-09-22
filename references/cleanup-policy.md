# Cleanup Policy

## Delete candidates

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
3. Choose a template from the matching language file, fill its slots from the code's actual behavior, and rewrite the entire logical comment unit in one pass.

Minimal word-level patching is forbidden: partial rewrites leave mixed styles and broken context inside one comment block. Each rewrite produces the complete final text of the unit at once, and rewriting must not touch code lines.

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

## TODO/FIXME

Do not delete TODO/FIXME solely because they look stale.

Classify as:

- still actionable -> preserve/normalize;
- completed -> remove if implementation proves completion;
- historical rationale -> convert to durable comment/doc if needed;
- ambiguous -> escalate.

## Convergence rule

Text that already reads as durable rationale and contains no process metadata is not a finding, even if RepoMeld could phrase it differently.

If a candidate is already in the form RepoMeld would produce, leave it unchanged.

Repeated runs must converge: never rephrase already-normalized text, and never introduce new process metadata while cleaning.