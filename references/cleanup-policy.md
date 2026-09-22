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
- explanations that only restate the next line of code.

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