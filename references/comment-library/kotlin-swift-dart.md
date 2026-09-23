# Kotlin / Swift / Dart 范本（加载条件：`.kt` `.kts` `.swift` `.dart`）

## Kotlin

### 语法

- 文档注释 `/** */`（KDoc），内容是 **Markdown**，由 Dokka 渲染；行注释 `//`。
- KDoc 兼容 Javadoc 的 block tag 习惯，但正文遵循 Markdown 而非 HTML。

### K1 KDoc 函数

```kotlin
/**
 * ⟨Validates the user request before it reaches the handler.⟩
 *
 * ⟨Longer description: contracts, thread-safety, cross-references.⟩
 *
 * @param ⟨request⟩ ⟨the request to validate⟩
 * @return ⟨the validation result, never null⟩
 * @throws ⟨ValidationException⟩ ⟨if the request is malformed⟩
 */
fun ⟨validate⟩(⟨request⟩: ⟨Request⟩): ⟨Result⟩
```

- 标准标签：`@param`、`@return`、`@throws`、`@constructor`、`@property ⟨name⟩`（记录与构造参数不同名的属性）、`@receiver`（扩展函数的接收者）、`@sample ⟨path.to.function⟩`（引用可执行示例）、`@see`、`@author`、`@since`。
- 链接：`[⟨Foo⟩]`、`[⟨Foo⟩.⟨bar⟩]` 生成 Dokka 内链；`[⟨text⟩](⟨url⟩)` 外链。Markdown 分节（`# ⟨Heading⟩`）。
- `@suppress` 使 Dokka 从文档中排除该声明——**可见性口径，承重**。

### K2 KDoc 类与属性

```kotlin
/**
 * ⟨A queue that supports atomic drain of all pending items.⟩
 *
 * ⟨Concurrency contract: safe for concurrent use from multiple coroutines.⟩
 */
class ⟨DrainableQueue⟩ {
    /**
     * ⟨Current number of buffered elements. Never negative.⟩
     */
    val ⟨size⟩: Int
}
```

### K3 弃用与抑制（Kotlin 一律用注解，不用注释）

```kotlin
@Deprecated("⟨Use ⟨newFunc⟩ instead.⟩", ReplaceWith("⟨newFunc⟩(⟨...⟩)"))
@Suppress("⟨WARNING_NAME⟩")
```

- 注释里可以另写弃用原因与迁移注意事项，但**弃用标记本身是注解**——见到只写注释、无注解的"弃用"按缺弃用标记处理。

## Swift

### 语法

- 文档注释 `///`（首选）或 `/** */`；内容由 Xcode Quick Help 渲染，支持 Markdown；行注释 `//`。

### S1 函数文档

```swift
/// Parses ⟨a date string into a Date⟩.
///
/// - Parameters:
///   - ⟨input⟩: ⟨The raw string. Must be UTF-8.⟩
///   - ⟨format⟩: ⟨The expected format.⟩
/// - Returns: ⟨The parsed date, or nil when the string doesn't match.⟩
/// - Throws: ⟨ParseError⟩ ⟨when the format is unknown⟩
func ⟨parse⟩(⟨input⟩: String, ⟨format⟩: String) throws -> Date?
```

- 单参数可用 `- Parameter ⟨input⟩: ⟨desc⟩`；无异常/返回值就不写对应行，不填占位。
- Quick Help 字段标签（行首 `- ⟨Keyword⟩:`）：`Parameter(s)`、`Returns`、`Throws`、`Precondition`、`Invariant`、`Complexity`、`Postcondition`、`Important`、`Note`、`Warning`、`SeeAlso`、`Tag`。

### S2 类型与属性文档

```swift
/// ⟨A thread-safe in-memory cache.⟩
///
/// ⟨Eviction policy and concurrency contract.⟩
final class ⟨Cache⟩ {
    /// ⟨Maximum number of entries; must be positive.⟩
    let ⟨capacity⟩: Int
}
```

- 注意：**任何行首 `⟨Word⟩:` 形态**（`- Note:` 是标签）都会被 Quick Help 渲染为 callout；改写时不要把普通散文写成 `Foo:` 形态。

## Dart

### 语法

- 文档注释 `///`（Effective Dart 明确要求；`/* */` 文档不推荐）；dartdoc 渲染 Markdown；行注释 `//`。

### D1 函数 / 类文档

```dart
/// Splits [⟨input⟩] into tokens.
///
/// ⟨Longer description. References: [⟨Token⟩], [⟨tokenizeMany⟩].⟩
///
/// ```dart
/// final ⟨tokens⟩ = ⟨tokenize⟩('a b');
/// ```
List<String> ⟨tokenize⟩(String ⟨input⟩) {}
```

- 首段是概览，以句号结尾；用 `[⟨symbol⟩]` 引用符号生成 dartdoc 链接；代码块标注 `dart` 语言。
- 不写 "This function..."、不复述签名。

## 任务标记

- 三种语言均无统一官方 TODO 格式；沿用 Google 系：`// TODO: ⟨bug/link⟩ - ⟨what⟩`。

## 承重注释（跨三语言）

| 写法 | 作用 |
|---|---|
| `@suppress`（KDoc） | Dokka 排除声明，删改改变文档可见性 |
| `@Deprecated` / `@Suppress` / `@file:Suppress`（Kotlin）、`@Deprecated`（Dart） | 注解而非注释，不动 |
| `// swiftlint:disable[:next/:this] ⟨rule⟩` … `// swiftlint:enable ⟨rule⟩` | SwiftLint 抑制指令 |
| `// swiftformat:disable:next ⟨rule⟩` | SwiftFormat 抑制指令 |
| `// ktlint-disable ⟨rule⟩` / `/* ktlint-disable ⟨rule⟩ */` … enable | ktlint 抑制指令 |
| `// ignore: ⟨lint⟩` / `// ignore_for_file: ⟨lint⟩` | Dart 分析器抑制；`ignore_for_file` 须在文件头 |
| `// dart format off` / `// dart format on` | dart_style 格式化岛（新版 dart_style） |
| `/// ` 代码块中的示例（dartdoc/KDoc/Swift） | 与文档一体，整块改写，不删示例 |

## 工具约束

- ktlint / detekt / SwiftLint / dart analyzer 的注释相关规则（如 ktlint 的注释格式规则）：仓库启用时保持通过。
- Dokka / dartdoc 对链接 `[⟨symbol⟩]` 做解析，指向不存在的符号产生告警——链接照抄声明名。

## 来源

kotlinlang.org/docs/kotlin-doc.html（KDoc）；Apple Markup Formatting Reference（Xcode 文档注释与 callout，developer.apple.com）；Effective Dart: Documentation（dart.dev/guides/language/effective-dart/documentation）；SwiftLint/SwiftFormat/ktlint/dart analyzer 官方文档。
