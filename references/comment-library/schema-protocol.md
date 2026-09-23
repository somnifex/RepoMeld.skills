# 接口 / 协议 / 数据定义语言范本（加载条件：`.graphql` `.gql` `.proto` `.json` `.jsonc` `.json5` 及 OpenAPI / JSON Schema 文件）

**总原则：这些语言里"注释"分两层——给人看的注释，和被工具读取的正式描述（description）。后者是 API 语义的一部分，出现在内省结果、代码生成产物与文档站上，绝不能当普通注释清理；只允许按文档标准整块改写。**

## GraphQL

### Q1 描述（description，承重）

```graphql
"""
⟨A human-readable summary of this type.⟩

⟨Longer description.⟩
"""
type ⟨Invoice⟩ {
  """⟨Total amount in minor units. Never negative.⟩"""
  total: Int!
}
```

- `"""..."""` 是 schema 的**正式文档**：通过 introspection 暴露、客户端代码生成器会带进生成代码 → 改写这里 = 改 API 文档；只能整块改写，必须保留为 description。
- 描述可出现在 schema、type、field、argument、enum value、directive 上。

### Q2 行注释与弃用指令

```graphql
# ⟨note for maintainers⟩
⟨definition⟩
```

- `#` 注释纯给人看，可按通用规则清理；`"""` 描述不可。
- 弃用是**指令**不是注释：`@deprecated(reason: "⟨Use ⟨newField⟩ instead.⟩")`——承重，禁删。

## Protocol Buffers

### Q3 消息 / 字段注释

```proto
// Invoice represents a billed order.
//
// Amounts are minor units to avoid float rounding.
message ⟨Invoice⟩ {
  // Total in minor units. Never negative; -1 means unknown (legacy rows).
  int64 total = 1;
}
```

- `//` 与 `/* */` 皆可；样式指南要求 file / message / field / enum / service / rpc 都有注释。
- 前置注释会被部分 protoc 插件转为目标语言文档注释（如 C# 生成 `///`），protoc-gen-doc、buf 等文档工具直接读取 → 注释即文档，按文档标准整块写，不写空话。
- 弃用是选项不是注释：`deprecated = true`。

## JSON 家族

### Q4 严格 JSON 没有注释

`.json` 文件里出现 `//` 或 `/* */` 属于解析风险：先确认解析器接受（VS Code 配置、tsconfig 等实为 JSONC），否则 escalate——**不清理也不补写**，注释在这里可能是坏数据而不是文档。

### Q5 JSONC / JSON5

- `//` 与 `/* */` 皆可；注释解释"为什么是这个值"，保守保留。

### Q6 JSON Schema

```json
{
  "$comment": "⟨Why this constraint exists.⟩",
  "description": "⟨User-facing description; shown by generators and editors.⟩"
}
```

- `$comment` 是规范关键字（供维护者注记，工具可剥离）——不当垃圾删除；`title` / `description` 是文档面 → 改写等同文档变更。
- 弃用：`"deprecated": true`（2020-12 规范关键字）。

## OpenAPI / AsyncAPI

- 文档职责由 `description`（及 `summary`）字段承担，不是注释；description 里出现流程残留（agent 叙事、阶段标记）按文档改写处理，字段本身保留。
- `deprecated: true` 字段承担弃用标记。

## 来源

spec.graphql.org（§Descriptions、@deprecated）；protobuf.dev 样式指南与语言指南（comments、deprecated）；JSON Schema Specification（`$comment`/`description`/`deprecated`）；OpenAPI Specification。
