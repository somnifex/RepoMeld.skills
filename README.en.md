# RepoMeld

**RepoMeld** is a runtime-agnostic, self-orchestrating repository hygiene Skill for consolidating the "AI traces" left behind by SDD, coding agents, and vibe coding.

[简体中文](./README.md) | [English](./README.en.md)

## The problem it solves

Developing software with AI agents leaves behind a lot of process residue:

- Stage markers like `S1/S2/M1/M2`, `Phase 3`, `Task 2.1`;
- Agent narration in comments, such as "now we need to…", "as discussed above…";
- One-off plan / report / scratch / verification files;
- Stale TODOs, duplicated design rationale, abandoned agent artifacts.

Deleting everything loses design intent and constraints that are still valuable; keeping everything makes the repository progressively unmaintainable. RepoMeld's approach: **remove genuine process noise, normalize what remains into durable engineering knowledge, and never change observable runtime behavior.**

It is not an "AI comment deleter" and not a license for unrelated refactoring — behavior changes, API/schema changes, and dependency upgrades are out of scope by default.

## Key features

- Scans the current repository automatically and builds a repository map.
- Detects whether the host runtime supports subagents / child sessions / parallel delegation.
- Not bound to Codex, Claude Code, OpenCode, or any proprietary API.
- Uses multi-agent orchestration when available; degrades to single-agent sequential execution with identical semantics otherwise.
- Partitions work semantically by package / service / domain / ownership, not by comment, TODO, or file type.
- Worker → Integrator → Root hierarchical reduction, suitable for large monorepos.
- Hard barrier between Audit and Apply, preventing cascading edits from scan-as-you-go changes.
- Exactly one write owner per file within a mutation epoch.
- Independent Verifier runs maker-checker style review in a fresh context.
- An L0–L5 risk model keeps hygiene from turning into behavior refactoring.
- Internal subskills load progressively to keep the main context small.
- `scripts/repomeld_scan.py` provides an optional read-only, deterministic repository inventory.

## How it works

RepoMeld describes orchestration through a semantic dispatch protocol rather than any vendor API:

```text
DELEGATE(role, scope, instructions)
WAIT(required_tasks)
COLLECT(results)
REDUCE(results)
VERIFY(changes)
```

These are logical operations, not function calls. The host agent maps them onto whatever native subagent / delegation capabilities exist in the current runtime.

### Role hierarchy

1. **Root Coordinator**: capability discovery, repository discovery, global partitioning, barrier control, and the final report.
2. **Domain Integrator**: each integrator manages one semantic domain or group, e.g. `apps/*`, `packages/*`, a bounded context, or a service group.
3. **Worker**: each worker handles exactly one shard; read-only during Audit, and during Apply it may only touch files in its own write ownership.
4. **Independent Verifier**: after all Apply work completes, reviews the final diff and verification results in a fresh context, belonging to no modification group.

For example, with two domain groups the logical hierarchy is:

- Root Coordinator
  - Domain Integrator: application layer
    - Worker: `apps/web`
    - Worker: `apps/api`
    - Worker: `apps/admin`
  - Domain Integrator: shared packages
    - Worker: `packages/auth`
    - Worker: `packages/database`
    - Worker: `packages/ui`
  - Independent Verifier

### Lifecycle

Execution follows a strict phase order:

| Phase                           | Executor           | Parallel                | Mutations allowed         | Output / sync condition                           |
| ------------------------------- | ------------------ | ----------------------- | ------------------------- | ------------------------------------------------- |
| 1. Runtime capability discovery | Root               | No                      | No                        | Choose parallel, sequential, or single-agent mode |
| 2. Repository discovery         | Root / Explorers   | Yes                     | No                        | Repository map                                    |
| 3. Dynamic partitioning         | Root               | No                      | No                        | Semantic shards + ownership                       |
| 4. Audit fan-out                | Workers            | Yes                     | No                        | Worker findings                                   |
| 5. Audit reduction              | Integrators / Root | Grouped                 | No                        | Cleanup plan                                      |
| 6. Audit barrier                | Root               | No                      | No                        | All required audits complete before proceeding    |
| 7. Apply fan-out                | Workers            | Yes                     | Yes, own ownership only   | Shard diffs + local validation                    |
| 8. Apply reduction              | Integrators / Root | Grouped                 | Low-risk integration only | Repository-level diff                             |
| 9. Apply barrier                | Root               | No                      | No                        | All mutations done, final diff frozen             |
| 10. Independent verification    | Fresh Verifier     | Per verification domain | No by default             | Verification result                               |
| 11. Report                      | Root               | No                      | No                        | Final report and escalation items                 |

The two barriers are hard sync points: **no mutation before the Audit Barrier, and no repository-level verification before the Apply Barrier.**

### Risk levels

| Level | Scope                                                          | Default policy                                  |
| ----- | -------------------------------------------------------------- | ----------------------------------------------- |
| L0    | Metadata / process markers (S1/M2, agent narration)            | Auto-apply                                      |
| L1    | Comment / documentation normalization                          | Auto-apply                                      |
| L2    | Deletion / relocation of non-runtime files                     | Only after reference analysis and policy checks |
| L3    | Runtime dead-code removal                                      | Escalate for human confirmation                 |
| L4    | Behavior-changing code edits                                   | Forbidden by default                            |
| L5    | API / schema / security / config / dependency semantic changes | Forbidden by default                            |

## Usage

Invoke it in natural language from any host that supports `SKILL.md`.

Full cleanup (auto-applies L0–L2 only; L3+ is escalated in the report):

```text
Use RepoMeld to clean the current repository. Scan automatically and decide whether to use subagents based on the repository's semantic boundaries; when parallelism is available, organize Worker/Integrator/Verifier yourself. Auto-apply L0-L2 only, escalate L3+, and do not change runtime behavior.
```

Audit only, without modifying any file:

```text
Use RepoMeld to audit the current repository without modifying any file. Scan independent modules in parallel where possible and output a cleanup plan and risk items.
```

Scoped to specific directories:

```text
Use RepoMeld on apps/api and packages/auth; do not touch other directories or pre-existing uncommitted changes.
```

Practical tips:

- Run on a clean worktree (or a dedicated branch) so the final diff is easy to review;
- For large cleanups, run an audit-only pass first and confirm the cleanup plan looks right;
- RepoMeld is a prompt protocol — results depend on the host model's capability; the report always distinguishes verified facts from unverified assumptions.

## Installation

RepoMeld is a purely declarative Skill bundle: no build step, no third-party dependencies (the helper scripts only use the Python 3.8+ standard library).

Place this repository in your host's skill discovery directory, ideally named `repomeld`:

| Host                            | In-repo path (example)                         |
| ------------------------------- | ---------------------------------------------- |
| Claude Code                     | `.claude/skills/repomeld/`                     |
| Codex                           | `.agents/skills/repomeld/`                     |
| OpenCode                        | `.opencode/skill/repomeld/`                    |
| Other hosts supporting SKILL.md | See the host's own skill directory conventions |

User-level (global) installation works the same way, e.g. `~/.claude/skills/repomeld/`. You can also mount the repository at those paths via git submodule / subtree to follow upstream updates.

`agents/openai.yaml` holds interface metadata (display name, description, icon, implicit-invocation policy) for OpenAI-family hosts (ChatGPT / Codex / Atlas); other hosts ignore it, and removing it does not affect core functionality.

## File structure

```text
repomeld/
├── SKILL.md                     # Entry point: invariants, workflow state machine, phase definitions
├── README.md
├── README.en.md
├── LICENSE
├── agents/
│   └── openai.yaml              # Optional OpenAI-family host interface metadata
├── assets/
│   └── icon.svg
├── references/                  # Policies loaded progressively per phase
│   ├── orchestration-protocol.md
│   ├── cleanup-policy.md
│   ├── knowledge-preservation.md
│   ├── partitioning-policy.md
│   ├── risk-policy.md
│   ├── verification-policy.md
│   └── subskills/               # Sub-workflows for INIT → REPORT
├── prompts/                     # Subagent role prompts
│   ├── explorer.md
│   ├── worker.md
│   ├── integrator.md
│   └── verifier.md
├── schemas/                     # Structured result contracts per phase (JSON Schema)
└── scripts/
    ├── repomeld_scan.py         # Read-only repository inventory
    └── validate_skill.py        # Bundle integrity check
```

## Helper scripts

Read-only scan (produces candidate listings, changes nothing):

```bash
python scripts/repomeld_scan.py /path/to/repo
```

Validate the skill bundle:

```bash
python scripts/validate_skill.py
```

The scan script only produces candidate data and holds no deletion authority; every deletion is adjudicated by RepoMeld's policies and verification flow.

## Why there is no CodexAdapter / ClaudeAdapter / OpenCodeAdapter

Mainstream coding agents can already decide at runtime how to orchestrate subagents, so the adapters collapse into a single declarative Orchestration Protocol: the host agent sees its own tools and maps `DELEGATE / WAIT / COLLECT / REDUCE / VERIFY` onto native capabilities itself. RepoMeld therefore never needs to chase any vendor's API changes and works on future hosts out of the box.

## Contributing

Issues and PRs are welcome:

- Run `python scripts/validate_skill.py` after changing skill content to keep the bundle intact;
- Put new policies or phase details in `references/` and keep `SKILL.md` as a lean entry point;
- For changes to the orchestration protocol, risk model, or verification policy, describe the impact in the PR description.

## License

[MIT](./LICENSE) © 2026 HowieWood
