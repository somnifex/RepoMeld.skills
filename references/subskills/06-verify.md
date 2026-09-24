# Subskill: Verify Repository

Prefer a fresh independent context.

Review final diff against baseline, the cleanup plan, and the recorded scope.

Check for behavior-sensitive edits, contract/config/schema/dependency changes, broken references, lost rationale, and unexpected modifications to protected paths.

Scope checks:

- the final diff touches nothing outside the recorded cleanup scope;
- every in-scope file was audited or explicitly reported as skipped (coverage check against `files_in_scope` / `files_audited`);
- task preservation: every deferred task in the plan is untouched in the final diff (no resolution, rewrite, deletion, or context-carrier removal), and each appears in the report with its preserved context.

For comment rewrites and additions specifically, verify from the diff that:

- each rewritten comment block was replaced as a whole unit (no mixed half-old half-new residue inside one block);
- each added comment exists at a site the plan marked `add`, matches the cited template, and every claim inside it can be pinned to the actual code (the parameter, return value, constraint, or upstream link is really there); additions whose facts cannot be pinned are suspicious changes;
- no code lines changed as a side effect of comment edits;
- load-bearing comments (license/SPDX headers, generated-file markers, build/compiler directives, suppression directives, doctests, magic comments) were left intact.

Run repository-native validation when feasible.

Return a result compatible with `schemas/verification-result.schema.json`: `verified`, `failed`, or `incomplete` with evidence and gaps.
