# JavaScript / TypeScript 范本（加载条件：`.js` `.jsx` `.ts` `.tsx` `.mjs` `.cjs`）

## 语法

- 行注释 `//`；块注释 `/* */`；文档注释 `/** */`（JSDoc / TSDoc）。
- JSX 中注释写作 `{/* ⟨...⟩ */}`（常见错误是直接写 `//`）。

## 文档注释范本

### J1 JSDoc 函数（jsdoc.app 官方示例骨架）
```js
/**
 * ⟨Represents a book.⟩
 * @constructor
 * @param {string} ⟨title⟩ - ⟨The title of the book.⟩
 * @param {string} ⟨author⟩ - ⟨The author of the book.⟩
 */
function ⟨Book⟩(⟨title⟩, ⟨author⟩) {}
```
普通函数模板：
```js
/**
 * ⟨Summary sentence.⟩
 * @param {⟨type⟩} ⟨name⟩ - ⟨description⟩
 * @param {⟨type⟩} [⟨opt⟩] - ⟨optional param, bracket form marks optional⟩
 * @returns {⟨type⟩} ⟨description⟩
 * @throws {⟨ErrorType⟩} ⟨when⟩
 */
```
可选参数两种写法都有官方支持：`{string=} p2`（Closure）与 `{string} [p3]`（JSDoc）；同一仓库保持一种。

### J2 弃用
```js
/**
 * @deprecated ⟨Use ⟨replacement⟩ instead.⟩
 */
```
`@deprecated` 在 TS 与 JS 中都被识别（编辑器删除线）。

### J3 TypeScript 项目
- **`.ts` 文件**：类型写在签名里，文档注释只写散文（用途、约束、示例、警告），不重复类型信息。微软维护的 TSDoc 是 TS 生态标准：同样 `/** */` + `@param ⟨name⟩ - ⟨desc⟩`，类型不带花括号。
- **`.js` 文件被 TS 检查（checkJs / `// @ts-check`）时，JSDoc 承载类型语义**：
```js
/** @type {string | boolean} */
var ⟨sb⟩;

/**
 * @param {string} ⟨p1⟩ - A string param.
 * @returns {string} ⟨result⟩
 */
```
此时 JSDoc 是**语义信息**：删除或改错会改变类型检查结果 → 承重，禁改。
- 常用类型标注标签（TS 官方支持）：`@type` `@param` `@returns` `@typedef` `@callback` `@template` `@satisfies` `@public/@private/@protected/@readonly/@override`；`@async` 等不在支持列表，别引入。

### J4 文件头
```js
/**
 * @file ⟨One-line purpose of the file, plus cross-file constraints.⟩
 */
```
- `@fileoverview` / `@overview` 是 JSDoc 同义词；TSDoc 生态用 `@packageDocumentation`（含库概览段落）——按仓库既有习惯二选一，不混用。
- `@module ⟨name⟩` 声明模块标识（CommonJS / 无导出的文件）。

### J5 类型定义（checkJs 与 .js 库的类型承载）
```js
/**
 * @typedef {Object} ⟨Person⟩
 * @property {string} ⟨name⟩ - ⟨Full name.⟩
 * @property {number} [⟨age⟩] - ⟨Optional age.⟩
 */
```
```js
/**
 * @callback ⟨RequestHandler⟩
 * @param {⟨Request⟩} ⟨req⟩ - ⟨The incoming request.⟩
 * @returns {Promise<⟨Response⟩>} ⟨The response.⟩
 */
```
```js
/**
 * @template {object} ⟨T⟩
 * @param {⟨T⟩} ⟨value⟩
 * @returns {⟨T⟩}
 */
```
在 `.ts` 里用 `@typedef` 描述结构类型（TS 官方支持）；此时 typedef 是**类型语义**，承重。

### J6 TSDoc 扩展标签（TS 库工程）
```ts
/**
 * ⟨Summary.⟩
 * @remarks ⟨Longer context: contracts, performance notes.⟩
 * @defaultValue ⟨false⟩
 * @example
 * ```ts
 * ⟨usage snippet⟩
 * ```
 * @beta
 */
```
- 标准 release tags：`@alpha` / `@beta` / `@experimental` / `@public` / `@internal`。`@internal` 会被 API Extractor 从公开 API 面剥离——**改它 = 改 API 可见性口径，承重**。
- `@see ⟨link⟩`、`@throws ⟨desc⟩` 同属标准标签。

## 行内注释范本

- `// ⟨sentence⟩`：`//` 后一个空格（ESLint spaced-comment）；优先大写开头完整句（capitalized-comments）。
- why/约束/workaround 通用型同 `python.md` P7/P8，注释符换 `//`；workaround 必须带 issue/ticket 链接。

## 任务标记

```js
// TODO: ⟨bug/link⟩ - ⟨what⟩
// FIXME: ⟨context⟩ - ⟨what⟩
```
ESLint `no-warning-comments` 默认盯 `todo`/`fixme`/`xxx`（大小写不敏感、整词）。Google JS 指南未规定格式（仅在 8.2.2 提到"leave a TODO comment"是 last resort）；生态中 `// TODO(⟨owner⟩):`（AngularJS 时代沿袭）与裸 `// TODO:` 并存。规范化沿用仓库既有形式；缺省 ticket/链接优先，人名形式仅在仓库既有且无追踪号可挂时保留。

## 抑制指令清单（全部承重，禁止删除）

| 写法 | 说明 |
|---|---|
| `// @ts-expect-error ⟨-- reason⟩` | 抑制下一行错误；**若实际无错误则自身报错**（自动过期）。优先于 `@ts-ignore` |
| `// @ts-ignore` | 无条件抑制下一行；发现底层错误已修复、可换成 `@ts-expect-error` 时 → escalate 建议替换，不自动改 |
| `// @ts-nocheck` | 整文件关闭类型检查（文件头） |
| `// @ts-check` | 开启 .js 文件类型检查（文件头，承重） |
| `/* eslint-disable ⟨rules⟩ */` … `/* eslint-enable ⟨rules⟩ */` | 区间抑制；`eslint-enable` 不带规则则恢复全部 |
| `// eslint-disable-next-line ⟨rules⟩ -- ⟨reason⟩` | 行抑制 + 官方 `--` 描述语法 |
| `⟨code⟩ // eslint-disable-line ⟨rules⟩` | 同行抑制 |
| `/* prettier-ignore */` | 下一节点跳过 prettier |
| `/* jshint ignore:start/end */`、`// deno-lint-ignore ⟨rule⟩` | 其他 linter 家族 |

ESLint 官方最佳实践：disable 注释应少用、带 reason、视为临时手段；开启 `reportUnusedDisableDirectives` 的仓库中，确认指令无效 → escalate（不自动删，linter 配置差异可能掩盖真实效果）。

## 工具约束

- ESLint 相关注释风格规则：`spaced-comment`、`no-inline-comments`、`capitalized-comments`、`lines-around-comment`、`no-warning-comments`——改写保持通过。
- prettier 保留注释位置与文本（不会重排注释内容），注释折行遵循仓库 prettier printWidth 习惯。

## 来源

jsdoc.app Getting Started；TypeScript Handbook "JSDoc Reference" 与 "Type Checking JavaScript Files"（ts-expect-error 语义）；TSDoc（tsdoc.js.org）；ESLint 规则页（eslint.org）。
