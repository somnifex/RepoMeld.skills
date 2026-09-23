# Rewrite Recipes（整块改写与新增手册）

核心原则：**不做最小修正**。逐词/逐行修补会在同一个注释块里留下混合风格与破碎语境——这正是"拆东墙补西墙"。改写的基本单位是**逻辑注释单元**：

- 同一声明（函数/类/字段/类型）上方的完整注释块（`//` 行组、`/* */` / `/** */` / `""" """` 块、YARD/KDoc/PHPDoc 块等）；
- 同一语句上下的连续行注释组；
- 分散于块内但同属一个主题的多段注释。

一个单元内的所有行一次性改到位，不留"半旧半新"。**新增注释（`add`）遵循同一单位规则**：按选定的语言模板一次性写出完整单元，slot 只填从代码观察到的事实，不逐行追加、不半写留白。

## 整块改写流程（APPLY worker 执行）

1. **重读完整单元与相邻代码**：注释块 + 它描述的代码 + 相邻声明。用代码的**实际行为**判断哪句话是耐久知识、哪句已经失真。
2. **抽取**：把耐久知识逐条列出（约束、理由、协议、安全边界、兼容性、性能假设、业务规则、ticket 链接）；再列出过程元数据（里程碑、步骤编号、叙事、署名、日期、agent 标记）。
3. **选模板**：按 `selection-guide.md` 场景表，从语言范本文件取一个模板（注明模板编号）。
4. **重写整块**：耐久知识填入模板 slot；元数据丢弃；文档注释空缺的语义槽位（参数、返回值、异常）按代码事实补写，不臆造。
5. **自检**：块内无混合风格残留；未引入新的过程元数据；未改动任何代码行；与同文件既有风格一致；幂等——重复运行不会再改出不同措辞。**新增注释额外自检**：每个 slot 的事实都能在代码中指认（参数、返回值、约束、链接确实存在），指认不出的事实删掉或 escalate。

## 配方（Before → After 均为完整单元替换）

### R1 里程碑标签 + 理由混合
```
Before: // M2: We changed this to sequential calls after parallel calls broke the vendor API.
After:  // Keep vendor writes sequential; the upstream API does not support concurrent mutations.
```
整块重写：去掉 `M2:` 与叙事语气（"We changed"），保留顺序约束与上游理由。

### R2 步骤旁白（代码自解释）
```
Before: // Step 2: Now we need to iterate through every user and check the flag
```
→ 整块删除。若该函数为公开 API 且缺文档注释 → 改补一条模板化文档注释（不把旁白原样搬进去）。

### R3 教程式冗长 docstring（AI 生成典型特征）
```
Before: /** This function takes two numbers and adds them together and returns the result. */
```
→ 无额外信息时整块删除；有信息时压缩为单行模板：`/** Adds ⟨a⟩ and ⟨b⟩. */`。判断标准：删除后读者是否丢失"代码签名之外"的信息。

### R4 注释掉的代码
→ 整块删除（VCS 承载历史）。若代码行之间夹有说明文字且含耐久知识 → 只保留那句说明、删除代码行，并按需并入相应文档注释。

### R5 日志/署名/日期注释
```
Before: // Modified by John 2023-05-01 to fix bug
```
→ 整块删除（git history 承载）。若 bug 编号是关键上下文 → 并入文档注释的 References/See 类槽位，不单独留日志注释。

### R6 陈旧/失控 TODO
按 cleanup-policy 分类：仍可执行 → 保留并规范化到语言文件的任务标记模板（补 owner 或 ticket 链接）；已完成且代码证实 → 删除；属于历史理由 → 转成耐久注释；存疑 → escalate。规范化也是整块操作：同一个 TODO 主题的多行注释一次改完。

### R7 中英混杂/多语言碎片描述同一件事
→ 选定一种语言（仓库惯例优先），把多个碎片**合并成一个**规范注释块，删除其余碎片。不允许留下翻译腔的混合块。

### R8 抑制指令缺 reason
```
Before: // eslint-disable-next-line no-console
After:  // eslint-disable-next-line no-console -- ⟨reason from context⟩
```
ESLint 支持 `--` 后接描述；ShellCheck 用上一行注释或行尾 `# this is intentional`；Python/Go 等用上一行 `# ⟨reason⟩`。**仅当能从上下文可靠推断理由时补写**，否则 escalate，不编造理由。

### R9 空洞文档注释
```
Before: /// <summary>The class.</summary>
After:  （按代码事实重写整个 summary；无法可靠描述时 escalate，不写废话）
```
C# 编译器校验 `<param name>` 与签名匹配——重写时参数名照抄签名，不即兴改。

### R10 同一单元上的矛盾注释

```
Before: // Retry up to 3 times before giving up.
        // Retries are disabled for batch jobs; failures propagate to the caller.
```

→ 以代码实际行为为准：保留与代码一致的一句，把仍然成立的信息合并为一个规范块，删除矛盾方。矛盾通常来自新旧迭代残留（旧规则没删干净）——合并时以代码为准，不保留"历史沿革"叙事。两句都无法从代码证实哪句正确 → escalate，不猜测。

## 新增（add）配方

补写不是改写，但同样整块产出。按 `selection-guide.md` 决策树 B 确认"必要"后：

- 从语言范本选定模板并注明模板编号（finding 与 plan 均须 cite）；
- slot 只填从代码观察到的事实：参数/返回值照抄签名，约束/理由取自代码行为或上下文证据，workaround 必须带链接与解除条件；
- 模板槽位填不满时 escalate，不用套话填充（"TODO"、"待补充"类占位文本属于新的过程元数据，禁止引入）；
- 写入位置遵循语言惯例（声明上方、docstring 位置、行尾约束注释），并沿用该文件既有风格。

## 禁止事项

- 不改代码行，只改注释行（含空白调整需谨慎：以 formatter 规则为准）。
- 不把耐久知识从代码库中删除——宁可整块保留原文，也不丢信息。
- 不引入新风格；只使用所选模板与仓库既有风格。
- 一次改写后，同单元不得在后续运行中被再次"优化"出措辞差异（幂等收敛）。
- 不给 vendored/生成代码加注释。
