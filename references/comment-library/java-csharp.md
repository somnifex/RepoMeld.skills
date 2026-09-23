# Java / C# 范本（加载条件：`.java` 或 `.cs`）

## Java

### 语法

- Traditional Javadoc `/** */`；JDK 23+ 支持 Markdown Javadoc `///`（Google Java Style 两者皆认可，同一仓库保持一致）。
- 实现行内注释 `//`。

### 文档注释范本（Google Java Style + Oracle Javadoc）

#### JC1 Traditional Javadoc
```java
/**
 * ⟨Multiple lines of Javadoc text are written here,
 * wrapped normally...⟩
 */
public ⟨int⟩ ⟨method⟩(⟨String p1⟩) { ... }
```
单行形（整体含标记能放进一行、且**无 block tag** 时）：`/** ⟨An especially short bit of Javadoc.⟩ */`

#### JC2 Markdown Javadoc（JDK 23+）
```java
/// ⟨Javadoc text is written here,
/// wrapped normally...⟩
public ⟨int⟩ ⟨method⟩(⟨String p1⟩) { ... }
```
段落用空行分隔（除前导 `///` 外无内容即空行），无需 `<p>`；tag 续行缩进两空格。

#### JC3 完整方法模板（block tag 顺序固定）
```java
/**
 * ⟨Summary fragment: a noun/verb phrase, capitalized and punctuated
 * as if a sentence — not "A Foo is a..." nor "This method returns...".⟩
 *
 * ⟨Longer description.⟩
 *
 * @param ⟨p1⟩ ⟨description⟩
 * @return ⟨description⟩
 * @throws ⟨Exception⟩ ⟨when⟩
 * @deprecated ⟨use ⟨replacement⟩ instead⟩
 */
```
- 顺序固定：`@param` → `@return` → `@throws` → `@deprecated`；四类 tag 描述**永不为空**。
- `@return the customer ID` 是官方点名的错误写法 → `Returns the customer ID.`（或 `{@return ...}`）。
- 覆盖范围：每个可见 class / member 至少有 Javadoc；"simple, obvious" 成员（`getFoo()`）可豁免；override 不强制（需要时只写 override 特有信息，不复述父类）。

#### JC6 包文档 / 内联标签 / HTML 转义
包文档写 `package-info.java`：
```java
/**
 * ⟨Provides ⟨...⟩ for ⟨domain⟩. Not thread-safe unless noted.⟩
 */
package com.example.⟨pkg⟩;
```
- 内联标签：`{@code ⟨literal⟩}`（防止 HTML 解析，代码与标识符一律包住）、`{@link ⟨Class#member⟩}`（交叉链接）、`{@literal ⟨char⟩}`、`{@value}`。
- **Javadoc 正文是 HTML**：`<`、`>`、`&` 必须写作 `&lt;` / `&gt;` / `&amp;`——改写时保持转义，不得引入裸角括号。
- 其他常用 block tag：`@since ⟨version⟩`、`@see ⟨reference⟩`；`@author` 是否保留跟随仓库现状（Google Style：新文件不加 author line）。

#### JC4 TODO（Google Java Style 现行格式）
```java
// TODO: ⟨crbug.com/12345678⟩ - ⟨Remove this after the 2047q4 compatibility window expires.⟩
```
上下文用 bug 引用或链接（可追踪、有后续讨论），**避免** `// TODO: @yourusername - ...`（官方反例）。

### 承重
- 文件头 license boilerplate（checkstyle RegexpHeader / package-info）→ 禁删。Google Style：新文件一般不加 author line；重大修改后可删 author line——仅在用户授权下操作，默认保留现状。
- `@SuppressWarnings` 是注解不是注释，不动。

## C#

### 语法

- XML 文档注释 `///`。**编译器校验**：XML 必须良构；`<param name="...">` 必须与签名匹配、覆盖全部参数；`cref` 引用必须存在——错配产生编译告警。重写时参数名照抄签名。

### 文档注释范本（learn.microsoft.com）

#### JC5 方法 / 类型
```csharp
/// <summary>
/// ⟨Complete sentences ending with full stops.⟩
/// </summary>
/// <param name="⟨p1⟩">⟨description⟩</param>
/// <returns>⟨description⟩</returns>
/// <exception cref="⟨ExceptionType⟩">⟨when⟩</exception>
public ⟨...⟩ ⟨Method⟩(⟨...⟩) { ... }
```
- `<summary>` 是最低要求；官方建议：文档化**所有公开可见类型及其成员**，正文用完整句号结尾的完整句。
- `<remarks>` 补充细节；`<example>` + `<code>` 给示例；`<see cref/href>` 与 `<seealso>` 做链接（外链用 `href`，`cref` 不产生可点击外链）；`<paramref name="...">` 引用参数；泛型用 `<typeparam name="⟨T⟩">`。
- 角括号转义：`&lt;` / `&gt;`。
- 继承基类/接口文档用 `<inheritdoc />`，不复制粘贴重复文本。
- 属性用 `<value>`；文档不用于命名空间。

### 行内注释 / 任务标记
`// ⟨sentence⟩`；TODO 用 Google 通用格式 `// TODO: ⟨bug/link⟩ - ⟨what⟩`。

### 承重
- `#region` / `#endregion` 是预处理指令（非注释）：默认保留；删除属低风险但需在计划中单独列明。
- `[SuppressMessage(...)]` 是特性，不动。

## 来源

google.github.io/styleguide/javaguide.html（§7 Javadoc、§4.8.6.2 TODO）；docs.oracle.com javadoc guide；learn.microsoft.com/dotnet/csharp/language-reference/xmldoc/recommended-tags。
