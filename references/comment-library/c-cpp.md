# C / C++ 范本（加载条件：`.c` `.cc` `.cpp` `.h` `.hpp`）

## 语法

- `//` 与 `/* */` 皆可（Google C++：保持一致即可，`//` 更常见）；Linux kernel 只用 `/* */`。**跟随仓库/模块既有风格，不引入第二种。**

## 文档注释范本

### CC1 Doxygen（仓库已启用 doxygen 时）
```cpp
/**
 * ⟨Brief description (first sentence).⟩
 *
 * ⟨Detailed description.⟩
 *
 * @param ⟨a⟩ ⟨an integer argument.⟩
 * @param ⟨s⟩ ⟨a constant character pointer.⟩
 * @return ⟨The test results⟩
 */
⟨ret⟩ ⟨f⟩(⟨...⟩);
```
- 等价风格（跟随仓库现状）：`/*! ... */`（Qt 风格）、`///`（C++ 风格）、`//!`（成员）；Javadoc 风格用 `@param`，Qt 风格用 `\param`。
- 成员后置注释：`int ⟨var⟩; ///< ⟨description after the member⟩`（仅对成员/参数有效）。
- `JAVADOC_AUTOBRIEF` 开启时首句即 brief——首句写完整短句。

### CC2 类注释（Google C++ 官方示例）
```cpp
// Iterates over the contents of a ⟨GargantuanTable⟩.
// Example:
//    std::unique_ptr<⟨GargantuanTableIterator⟩> iter = ⟨table⟩->NewIterator();
//    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
//      ⟨process⟩(iter->key(), iter->value());
//    }
class ⟨GargantuanTableIterator⟩ { ... };
```
要点：用途 + 最小用法示例 + 同步/多线程假设；接口注释讲用法，实现文件注释讲操作。

### CC3 函数声明注释（Google C++ 官方示例）
```cpp
// Returns an iterator for this table, positioned at the first entry
// lexically greater than or equal to `start_word`. If there is no
// such entry, returns a null pointer. The client must not use the
// iterator after the underlying GargantuanTable has been destroyed.
std::unique_ptr<Iterator> GetIterator(absl::string_view start_word) const;
```
- 隐含主语 "This function"、动词短语开头（"Opens the file"，不是 "Open the file"）。
- 描述 use：输入输出、指针参数可否为 null、输出参数的状态语义、性能影响、对象是否保留引用。
- 简单 accessor 可豁免；**`.cc` 内私有函数不豁免**。
- 函数定义处注释描述 operation：实现技巧、步骤概览、为何不用替代方案（例如"为何前半需要持锁而后半不需要"）；不复读声明注释。

### CC4 变量注释（哨兵值，Google C++ 官方示例）
```cpp
// Used to bounds-check table accesses. -1 means
// that we don't yet know how many entries the table has.
int num_total_entries_;
```
类型和名字已自解释的（`int num_events_;`）不用注释；全局变量都应有注释。

### CC5 文件头
- license boilerplate 必须保留；多抽象集合文件可加文件级概述，单抽象细节写在抽象旁边。

### CC6 DEPRECATED / TODO（Google C++ 推荐格式，按优先序）
```cpp
// DEPRECATED: ⟨use ⟨X⟩ instead⟩
// TODO: ⟨bug 12345678⟩ - ⟨Remove this after the 2047q4 compatibility window expires.⟩
// TODO: ⟨example.com/my-design-doc⟩ - ⟨what⟩
// TODO(⟨bug 12345678⟩): ⟨what⟩
// TODO(⟨John⟩): ⟨what⟩
```
带具体日期/事件的 TODO：写明确日期（"Fix by November 2005"）或明确事件（"Remove this code when all clients can handle XML responses."）。

## 行内注释（why）

```cpp
// Process "element" unless it was already processed.
if (std::find(v.begin(), v.end(), element) != v.end()) {
  Process(element);
}
```
**官方反例（禁止）**：`// Find the element in the vector.`——复述代码。自描述代码不需要注释；提供更高层的 why，或改代码使其自描述（改代码超出 RepoMeld 范围 → escalate）。

## Kernel 风格（仓库为 kernel 风格时）

```c
/*
 * This is the preferred style for multi-line
 * comments in the Linux kernel source code.
 * Please use it consistently.
 *
 * Description: A column of asterisks on the left side,
 * with beginning and ending almost-blank lines.
 */
```
- 官方原文：**"NEVER try to explain HOW your code works in a comment: it's much better to write the code so that the working is obvious"**——注释讲 what 与 why，放在函数头，而非散落函数体内。
- 数据结构要重点注释（每行一个声明、行尾短注释）；API 函数注释用 kernel-doc 格式；禁止重复函数签名的 boilerplate。

## 承重注释

| 写法 | 作用 |
|---|---|
| `/* fall through */`、`/* FALLTHRU */`、`/* FALLTHROUGH */` | GCC `-Wimplicit-fallthrough` 识别的可接受拼写（具体集合以 GCC 文档为准）；**不"规范化"拼写，跟随仓库现状** |
| `// clang-format off/on` | 格式化岛 |
| `// NOLINT`、`// NOLINTNEXTLINE(⟨check⟩)` | clang-tidy 抑制 |
| `// IWYU pragma: keep` 等 | include-what-you-use 指令 |
| `/* SPDX-License-Identifier: ⟨MIT⟩ */` | 许可证标识（SPDX 官方推荐行） |
| doxygen 块（若启用） | 文档语义 |

## 来源

google.github.io/styleguide/cppguide.html §Comments（原文提取）；www.kernel.org/doc/html/latest/process/coding-style.html §8；www.doxygen.nl/manual/docblocks.html；spdx.dev/learn/handling-license-info。
