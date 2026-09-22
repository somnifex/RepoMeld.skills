# Worked Example (Minimal)

A compact end-to-end shape reference for RepoMeld contracts. Values are illustrative; adapt counts, names, and commands to the actual repository.

## Request

```text
使用 RepoMeld 清理当前仓库。只自动执行 L0-L2，L3+ 升级报告，不改变运行时行为。
```

## Repository map excerpt (DISCOVER)

```text
root: /repo (git, branch main, clean)
languages: typescript (pnpm workspace)
modules: apps/web, apps/api, packages/auth, packages/ui
validation: pnpm -r lint, pnpm -r test
protected_paths: [] (worktree clean)
residue candidates: packages/auth/docs/m2-notes.md; stage markers in packages/auth/src
```

## Topology (PARTITION)

```text
Root Coordinator
- Worker: apps/web
- Worker: apps/api
- Worker: packages/auth + packages/ui (combined; both small)
- Independent Verifier
```

## Worker result excerpt (AUDIT_FANOUT)

```json
{
  "worker_role": "RepoMeld shard worker",
  "mode": "AUDIT",
  "scope": "packages/auth + packages/ui",
  "status": "complete",
  "findings": [
    {
      "id": "F-001",
      "scope": "packages/auth + packages/ui",
      "path": "packages/auth/src/session.ts",
      "line_start": 42,
      "line_end": 42,
      "category": "stage_marker",
      "action": "rewrite",
      "risk": "L1",
      "confidence": 0.9,
      "rationale": "M2 label wraps a real constraint: the vendor API rejects concurrent mutations.",
      "proposed_change": "// Writes are serialized because the upstream vendor API rejects concurrent mutations.",
      "reference_evidence": [],
      "requires_review": false
    },
    {
      "id": "F-002",
      "scope": "packages/auth + packages/ui",
      "path": "packages/auth/docs/m2-notes.md",
      "category": "temporary_artifact",
      "action": "delete",
      "risk": "L2",
      "confidence": 0.8,
      "rationale": "Milestone notes fully superseded by docs/auth.md; no unique content.",
      "proposed_change": null,
      "reference_evidence": ["grep -rn 'm2-notes' -> no matches outside the file itself"],
      "requires_review": false
    }
  ],
  "changed_paths": [],
  "risks": [],
  "validation": [],
  "notes": []
}
```

## Plan actions excerpt (PLAN)

```json
{
  "repository_root": "/repo",
  "baseline": {"branch": "main", "commit": "abc1234", "clean": true},
  "protected_paths": [],
  "execution_mode": "PARALLEL_NATIVE",
  "shards": [
    {"id": "apps-web", "owned_paths": ["apps/web/**"]},
    {"id": "apps-api", "owned_paths": ["apps/api/**"]},
    {"id": "packages-auth-ui", "owned_paths": ["packages/auth/**", "packages/ui/**"]}
  ],
  "actions": [
    {
      "id": "A-001",
      "path": "packages/auth/src/session.ts",
      "category": "stage_marker",
      "action": "rewrite",
      "risk": "L1",
      "owner": "packages-auth-ui",
      "reason": "Convert M2 narration into durable constraint.",
      "preservation_rationale": "Serialization requirement retained in meaning at the same site.",
      "reference_evidence": [],
      "verification": ["pnpm --filter auth test"]
    },
    {
      "id": "A-002",
      "path": "packages/auth/docs/m2-notes.md",
      "category": "temporary_artifact",
      "action": "delete",
      "risk": "L2",
      "owner": "packages-auth-ui",
      "reason": "Superseded milestone notes; unique content already merged into docs/auth.md.",
      "preservation_rationale": null,
      "reference_evidence": ["grep -rn 'm2-notes' -> no references"],
      "verification": ["grep -rn 'm2-notes' ."]
    }
  ],
  "escalations": [
    "L3 dead helper packages/auth/src/legacyRetry.ts - requires explicit user authorization"
  ]
}
```

## Verification excerpt (VERIFY)

```json
{
  "status": "verified",
  "behavior_change": "none_observed",
  "api_change": "none_observed",
  "schema_change": "none_observed",
  "config_change": "none_observed",
  "dependency_change": "none_observed",
  "protected_paths": "untouched",
  "checks": [
    {"command": "git diff --stat <baseline>", "status": "pass"},
    {"command": "pnpm -r test", "status": "pass"}
  ],
  "suspicious_changes": [],
  "gaps": []
}
```

## Report excerpt (REPORT)

```text
mode: PARALLEL_NATIVE (3 workers, 1 fresh verifier)
changed: 1 comment rewritten, 1 file deleted, 0 moved
knowledge: vendor serialization constraint retained at original site
escalated: 1 (L3 dead helper, awaiting user decision)
impact: no API/schema/config/dependency changes observed; behavior unchanged per diff review + tests
gaps: none
```