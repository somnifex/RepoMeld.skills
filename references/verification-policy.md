# Verification Policy

Verification is both mechanical and semantic.

## Mechanical checks

Use repository-native commands when available:

- formatter/check mode;
- lint;
- typecheck;
- unit tests;
- integration tests;
- build/package;
- documentation/link checks.

## Semantic checks

Review the diff for:

- changed executable lines;
- changed literals/constants;
- changed conditions/control flow;
- changed exports/public signatures;
- changed configuration values;
- changed schema/migrations;
- changed dependency manifests/locks;
- removed files still referenced anywhere;
- loss of non-obvious rationale.

## Baseline protection

Distinguish RepoMeld edits from changes that existed before RepoMeld started.

Never report pre-existing user changes as RepoMeld changes.

## Confidence language

Only state "no behavior change observed" when both diff review and relevant validation support it.

If validation could not run, state the gap explicitly.
