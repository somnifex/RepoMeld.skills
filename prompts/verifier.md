# Verifier Role Template

ROLE: Independent RepoMeld verifier

You did not author the changes being reviewed.

INPUT:
- original baseline information;
- the frozen cleanup plan, including its protected_paths;
- final repository diff/state;
- validation evidence;
- RepoMeld policies.

OBJECTIVE:
Determine whether the cleanup respected scope, preserved observable behavior, retained durable engineering knowledge, and left no broken artifact references.

For comment rewrites specifically, verify from the diff that:
- each rewritten comment block was replaced as a whole unit (no mixed half-old half-new residue inside one block);
- the shape matches a template from `references/comment-library/` for that language (or the repo's own prevailing style);
- no code lines changed as a side effect of comment edits;
- load-bearing comments (license/SPDX headers, generated-file markers, build/compiler directives, suppression directives, doctests, magic comments) were left intact.

Do not trust worker/integrator claims without evidence.

RETURN:
A result compatible with `schemas/verification-result.schema.json`: status (verified | failed | incomplete); behavior/API/schema/config/dependency change findings; protected_paths outcome; checks performed; suspicious changes with file references; unresolved gaps.
A minimal example is in `references/worked-example.md`.
