# Rust 范本（加载条件：`.rs`）

## 语法

- `///`：外部文档注释，作用于**其后**的声明。
- `//!`：内部文档注释，作用于**所在**模块/crate（crate 根 `lib.rs` / `main.rs` 的首页文档）。
- rustdoc 渲染 CommonMark + 扩展（表格、脚注、删除线、任务列表、警告块）。

## 文档注释范本（rustdoc book + Rust API Guidelines）

### R1 crate / 模块级
```rust
//! ⟨Fast and easy queue abstraction.⟩
//!
//! ⟨Overview paragraph.⟩
//!
//! [`⟨Easy⟩`]: ⟨http://thatwaseasy.example.com⟩
```

### R2 条目结构（官方推荐顺序）
```rust
/// ⟨Short sentence explaining what it is, ending with a period.⟩
///
/// ⟨More detailed explanation.⟩
///
/// # Examples
///
/// ```
/// ⟨at least one copy-pasteable example⟩
/// ```
///
/// ⟨Even more advanced explanations if necessary.⟩
```
- 首个空行前的内容用于搜索与模块概览——保持一行、句号结尾。
- 不在散文里复述类型（签名会被 rustdoc 超链接）；不写 "This function..."。
- 示例用 `?` 而非 `unwrap`/`try!`（示例常被用户原样拷贝，API Guidelines C-QUESTION-MARK）。
- `#` 开头的行会参与 `cargo test` 编译但不在 rustdoc 显示（可作示例脚手架）。

### R3 # Errors / # Panics / # Safety（API Guidelines C-FAILURE）
```rust
/// # Errors
///
/// ⟨If this function encounters ⟨condition⟩, an error variant will be returned.⟩
```
```rust
/// # Panics
///
/// ⟨Panics if ⟨condition⟩.⟩
```
```rust
/// # Safety
///
/// ⟨All invariants that the caller is responsible for upholding.⟩
```
- 返回 `Result` 的公开函数应有 `# Errors`；可能 panic 的公开函数应有 `# Panics`；`unsafe fn` 必须有 `# Safety`（含 trait 方法）。

## 行内注释范本

### R4 SAFETY 注释（unsafe 块；std 惯例，clippy `undocumented_unsafe_blocks` 检查）
```rust
// SAFETY: ⟨why this unsafe block is sound⟩
unsafe { ... }
```
**承重**：删除会触发 clippy 告警并丢失健全性论证。

### R5 why / 约束 / workaround
```rust
// ⟨sentence⟩
⟨code⟩
```
workaround 带上游 issue 链接与解除条件。

## 任务标记

无官方格式；沿用仓库惯例，缺省 `// TODO: ⟨context⟩ - ⟨what⟩`。

## 抑制与属性（Rust 用**属性**而非注释抑制）

| 写法 | 性质 |
|---|---|
| `#[allow(⟨lint⟩)]` / `#[allow(clippy::⟨lint⟩)]` | 语义属性；注释（`// allow(...)`）无抑制效果，见到注释式"抑制"应视为残留 |
| `#[deprecated(note = "⟨...⟩")]` | 弃用用属性，不用注释；doc comment 里另配 `Deprecated:` 说明可以 |
| `#[allow(missing_docs)]` | 关闭文档 lint |
| `#[doc = "⟨...⟩"]` | doc comment 的属性形式（与 `///` 等价）；宏内部生成文档只能用它 |
| `#[doc(hidden)]` | 从 rustdoc 输出隐藏该条目——**可见性口径，承重** |
| `#[doc(alias = "⟨name⟩")]` | rustdoc 搜索别名 |
| doc test 标注 ```` ```no_run ```` / ```` ```ignore ```` / ```` ```compile_fail ```` / ```` ```should_panic ```` | **语义**：改变 doc test 行为 |

**doc test 承重**：`///` 中的代码块会被 `cargo test` 编译并运行——删除或改动 = 删测试、改测试。

## 工具约束

- rustfmt：`wrap_comments`、`normalize_comments`、`comment_width`（rustfmt.toml）决定注释是否被折行/归一化；改写前看配置。
- clippy：`undocumented_unsafe_blocks`、`missing_docs`（若启用）。

## 来源

doc.rust-lang.org/rustdoc/how-to-write-documentation.html；rust-lang.github.io/api-guidelines/documentation.html（C-EXAMPLE、C-FAILURE、C-QUESTION-MARK）；std style guide（SAFETY 注释惯例）。
