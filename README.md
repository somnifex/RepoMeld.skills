# RepoMeld

**RepoMeld** 是一个 runtime-agnostic、self-orchestrating 的 repository hygiene Skill，用于收敛 SDD / coding agent / vibe coding 之后留下的"AI 痕迹"。

[简体中文](./README.md) | [English](./README.en.md)

## 它解决什么问题

用 AI agent 开发软件，仓库里会积累大量过程残留：

- `S1/S2/M1/M2`、`Phase 3`、`Task 2.1` 之类的阶段标记；
- "现在我们需要……"、"如上所述……"之类的 agent 叙事性注释；
- 一次性的 plan / report / scratch / verification 文件；
- 过期 TODO、重复出现的设计理由、被遗弃的 agent 中间产物。

直接删除会丢掉仍有价值的设计意图与约束；原样保留则仓库逐渐不可维护。RepoMeld 的做法是：**删除真正的过程噪声，把仍有价值的知识归一化到长期可维护的位置，并且不改变可观察的运行时行为。**

它不是"AI 注释删除器"，也不是无关重构的借口——行为变更、API/schema/依赖升级等一律不在默认范围内。

## 核心特性

- 自动扫描当前仓库并建立 repository map。
- 自动探测宿主 runtime 是否支持 subagent / child session / 并行委派。
- 不绑定 Codex、Claude Code、OpenCode 或任何自研 API。
- runtime 支持时自动采用多智能体；不支持时降级为单 Agent 顺序执行，语义不变。
- 按 package / service / domain / ownership 做语义切分（semantic shard），而不是按注释、TODO 或文件类型切分。
- Worker → Integrator → Root 的层级归并，适合大型 monorepo。
- Audit 与 Apply 之间有硬 barrier，避免边扫边改造成级联改动。
- mutation epoch 内每个文件只有一个 write owner。
- Independent Verifier 使用全新上下文做 maker-checker 式检查。
- L0–L5 风险模型阻止 hygiene 演变成行为重构。
- 内部 subskills 渐进式加载，降低主上下文压力。
- `scripts/repomeld_scan.py` 提供可选的只读、确定性 repository inventory。

## 工作原理

RepoMeld 使用"语义调度协议"描述编排，而不是绑定某个厂商的 API：

```text
DELEGATE(role, scope, instructions)
WAIT(required_tasks)
COLLECT(results)
REDUCE(results)
VERIFY(changes)
```

这些是逻辑操作，不是函数调用。宿主 Agent 根据自身可用工具，把它们映射到当前 runtime 原生的 subagent / delegation 能力。

### 角色层级

1. **Root Coordinator**：capability discovery、repository discovery、全局 partition、barrier 控制和最终报告。
2. **Domain Integrator**：每个 integrator 管理一个或一组语义域，例如 `apps/*`、`packages/*`、某个 bounded context 或 service group。
3. **Worker**：每个 worker 只处理一个明确 shard；Audit 阶段只读，Apply 阶段只能修改分配给自己的 write ownership。
4. **Independent Verifier**：所有 Apply 完成后，以全新独立上下文检查最终 diff 和验证结果，不属于任何修改组。

例如仓库被划分成两个 domain group 时，逻辑层级为：

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

### 生命周期

执行使用严格的阶段顺序：

| 阶段                              | 执行者                | 可并行     | 允许修改             | 输出/同步条件                        |
| ------------------------------- | ------------------ | ------- | ---------------- | ------------------------------ |
| 1. Runtime capability discovery | Root               | 否       | 否                | 确定并行、顺序或单 Agent 模式             |
| 2. Repository discovery         | Root / Explorers   | 是       | 否                | Repository map                 |
| 3. Dynamic partitioning         | Root               | 否       | 否                | Semantic shards + ownership    |
| 4. Audit fan-out                | Workers            | 是       | 否                | Worker findings                |
| 5. Audit reduction              | Integrators / Root | 分组并行    | 否                | Cleanup plan                   |
| 6. Audit barrier                | Root               | 否       | 否                | 所有必需审计完成后才能继续                  |
| 7. Apply fan-out                | Workers            | 是       | 是，仅限各自 ownership | Shard diffs + local validation |
| 8. Apply reduction              | Integrators / Root | 分组并行    | 仅低风险整合           | Repository-level diff          |
| 9. Apply barrier                | Root               | 否       | 否                | 所有修改完成并冻结最终 diff               |
| 10. Independent verification    | Fresh Verifier     | 可按验证域拆分 | 默认否              | Verification result            |
| 11. Report                      | Root               | 否       | 否                | 最终报告和 escalation items         |

两个 barrier 是硬同步点：**Audit Barrier 之前绝不进入 mutation，Apply Barrier 之前绝不开始 repository 级验证。**

### 风险分级

| 级别 | 范围                              | 默认策略           |
| -- | ------------------------------- | -------------- |
| L0 | 元数据 / 过程标记（S1/M2、agent 叙事等）     | 自动执行           |
| L1 | 注释 / 文档归一化                      | 自动执行           |
| L2 | 非运行时文件的删除 / 移动                  | 引用分析 + 策略检查后执行 |
| L3 | 运行时死代码删除                        | 升级为人工确认        |
| L4 | 行为改变类代码修改                       | 默认禁止           |
| L5 | API / schema / 安全 / 配置 / 依赖语义变更 | 默认禁止           |

## 使用

在支持 `SKILL.md` 的宿主里，直接用自然语言调用。

完整清理（只自动执行 L0–L2，L3+ 升级报告）：

```text
使用 RepoMeld 清理当前仓库。自动扫描并按仓库语义边界决定是否使用 subagents；支持并行时自行组织 Worker/Integrator/Verifier。只自动执行 L0-L2，L3+ 升级报告，不改变运行时行为。
```

只审计、不修改任何文件：

```text
使用 RepoMeld audit 当前仓库，不修改任何文件。自动并行扫描可独立的模块，输出 cleanup plan 和风险项。
```

限定目录：

```text
使用 RepoMeld 处理 apps/api 和 packages/auth；不要碰其他目录或已有未提交改动。
```

使用建议：

- 先在干净的工作树（或专用分支）上运行，便于 review 最终 diff；
- 大范围清理前可先跑一次 audit-only，确认 cleanup plan 符合预期；
- 报告中的 L3+ escalation 项批准后可增量处理：只对批准项走 Apply → Verify，无需全量重跑；
- RepoMeld 是提示词协议，实际效果取决于宿主模型的能力；报告中会明确区分"已验证事实"与"未验证假设"。

## 安装

RepoMeld 是纯声明式的 Skill bundle，无构建步骤、无第三方依赖（辅助脚本仅使用 Python 3.8+ 标准库）。

把本仓库放入宿主的 skill 发现目录，目录名建议为 `repomeld`：

| 宿主                | 仓库内路径（示例）                   |
| ----------------- | --------------------------- |
| Claude Code       | `.claude/skills/repomeld/`  |
| Codex             | `.agents/skills/repomeld/`  |
| OpenCode          | `.opencode/skill/repomeld/` |
| 其他支持 SKILL.md 的宿主 | 参照对应宿主文档的 skill 目录约定        |

用户级（全局）安装同理，放到对应用户级 skill 目录，例如 `~/.claude/skills/repomeld/`。也可以用 git submodule / subtree 把仓库挂到上述路径，便于跟随上游更新。

`agents/openai.yaml` 是面向 OpenAI 系宿主（ChatGPT / Codex / Atlas）的接口元数据（显示名、描述、图标、隐式调用策略）；其他宿主会忽略它，删除后不影响核心功能。

## 文件结构

```text
repomeld/
├── SKILL.md                     # Skill 入口：不变量、工作流状态机、各阶段定义
├── README.md
├── README.en.md
├── LICENSE
├── agents/
│   └── openai.yaml              # OpenAI 系宿主接口元数据（可选）
├── assets/
│   └── icon.svg
├── references/                  # 按阶段渐进加载的策略文档
│   ├── orchestration-protocol.md
│   ├── cleanup-policy.md
│   ├── knowledge-preservation.md
│   ├── partitioning-policy.md
│   ├── risk-policy.md
│   ├── verification-policy.md
│   ├── worked-example.md        # 端到端最小示例（契约形态参考）
│   └── subskills/               # INIT → REPORT 各阶段子流程
├── prompts/                     # 子代理角色提示词
│   ├── explorer.md
│   ├── worker.md
│   ├── integrator.md
│   └── verifier.md
├── schemas/                     # 各阶段结构化结果契约（JSON Schema）
└── scripts/
    ├── repomeld_scan.py         # 只读 repository inventory
    └── validate_skill.py        # bundle 完整性校验
```

## 辅助脚本

只读扫描（生成候选清单，不做任何修改）：

```bash
python scripts/repomeld_scan.py /path/to/repo
```

验证 Skill bundle 完整性：

```bash
python scripts/validate_skill.py
```

扫描脚本只生成候选数据，不拥有删除决策权；所有删除都由 RepoMeld 的策略与验证流程裁决。

## 为什么不提供 CodexAdapter / ClaudeAdapter / OpenCodeAdapter

主流 coding agent 已经都能在运行时决定如何编排 subagents，因此把 Adapter 收敛成一个纯声明式的 Orchestration Protocol：宿主 Agent 看到自身工具后，自行把 `DELEGATE / WAIT / COLLECT / REDUCE / VERIFY` 映射到原生能力。这让 RepoMeld 不需要跟随任何厂商 API 的变化，也能在未来宿主上直接工作。

## 贡献

欢迎 Issue 和 PR：

- 修改 Skill 内容后请运行 `python scripts/validate_skill.py`，确保 bundle 完整；
- 新增策略或阶段细节请放入 `references/`，保持 `SKILL.md` 入口简洁；
- 涉及编排协议、风险模型或验证策略的改动，请在 PR 描述中说明影响。

## 许可证

[MIT](./LICENSE) © 2026 HowieWood
