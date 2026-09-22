# Shell / Ruby / PHP / 其他脚本语言范本（加载条件：`.sh` `.bash` `.rb` `.php` `.pl` `.r` `.lua` 等）

## Shell

### 文件头范本
```bash
#!/usr/bin/env bash
# ⟨script-name⟩ — ⟨one-line purpose.⟩
#
# ⟨Usage / constraints / required environment.⟩
```
- shebang 承重：必须是文件第一行；紧贴其后的 shellcheck 指令作用于全文件。

### 行内注释
`# ⟨sentence⟩`；why/约束/workaround 通用型同 `python.md` P7/P8，注释符 `#`。

### ShellCheck 指令（承重，官方语法）
```bash
# shellcheck disable=SC2059
printf "\x$1"
```
- 多码：`# shellcheck disable=SC2086,SC2059`；范围：`# shellcheck disable=SC1000-SC9999`（可省 `SC` 前缀）。
- 方言：`# shellcheck shell=sh`（或 `bash` 等）。
- 来源提示：`# shellcheck source=⟨file⟩`、`# shellcheck source-path=SCRIPTDIR`。
- 理由写法（官方两种样式）：
```bash
# this is intentional because of reasons
# shellcheck disable=SC1234
⟨statement⟩
```
```bash
# shellcheck disable=SC1234 # this is intentional
⟨statement⟩
```
- 文件级配置放 `.shellcheckrc`（键值对，无注释前缀）——不属于注释清理范围。

## Ruby

### 魔法注释（承重）
```ruby
# frozen_string_literal: true
```
必须在首个非注释代码行之前——**语义注释，禁删禁移**。同类还有 `# typed: strict`（Sorbet，承重）。

### YARD 文档范本（Ruby 生态事实标准）
```ruby
# ⟨Sets a value on key.⟩
#
# @param key [Symbol] ⟨describe key param⟩
# @param value [Object] ⟨describe value param⟩
# @return [⟨Type⟩] ⟨description⟩
# @raise [⟨TypeError⟩] ⟨when⟩
# @deprecated ⟨Use #⟨new_method⟩ instead.⟩
def ⟨set⟩(⟨key⟩, ⟨value⟩)
```
RDoc 是另一体系（无 @tag）；同一仓库只用一种，跟随现状。

### 任务标记
RuboCop `Style/CommentAnnotation`：大写关键词 + 冒号 + 空格——`# TODO: ⟨...⟩`、`# FIXME: ⟨...⟩`、`# OPTIMIZE:`、`# NOTE:`。

## PHP

### PHPDoc 范本（phpDocumentor 官方示例骨架）
```php
/**
 * ⟨A summary informing the user what the associated element does.⟩
 *
 * ⟨A description that can span multiple lines to go in-depth
 * into the details of this element.⟩
 *
 * @param string $⟨myArgument⟩ ⟨With a description of this argument.⟩
 *
 * @return void
 */
function ⟨myFunction⟩($⟨myArgument⟩) {}
```
结构固定：Summary（句号/空行结束）→ Description → 空行 → `@tag` 区。PSR-5 仍是草案，但该语法是社区事实标准。

### 抑制
PHPStan 用注释抑制（如 `@phpstan-ignore-next-line`；具体写法以仓库现有用法与 phpstan 版本为准，不确定 → escalate）。

## 其他语言速查

| 语言 | 行注释 | 文档机制 |
|---|---|---|
| Perl | `#` | POD：`=pod ... =cut` 独立块（perldoc 读取，承重） |
| R | `#` | roxygen2：`#' @param ⟨x⟩ ⟨desc⟩`（生成 Rd 文档，承重） |
| Lua | `--` | LDoc：以 `---` 起始的块 |
| MATLAB | `%` | — |
| Fortran | `!` | — |
| VHDL | `--` | — |
| Haskell | `--` | Haddock：`-- |`（前置）/ `{-| ... -|}`（块，承重） |

以上语言本页模板不够用时：优先沿用**仓库内既有文件**的写法；仍不足 → escalate。

## 来源

shellcheck wiki（Directive，github.com/koalaman/shellcheck）；rubydoc.info YARD Tags.md；docs.phpdoc.org（What is a DocBlock）；rubocop 文档（Style/CommentAnnotation）；roxygen2、Haddock、perlpod 官方文档。
