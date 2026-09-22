# Python 范本（加载条件：shard 含 `.py`）

## 语法

- 行注释 `#`；无独立文档语法，文档注释 = docstring（`"""triple double quotes"""`，PEP 257）。
- `# -*- coding: utf-8 -*-` 编码声明（PEP 263）：语义注释，旧文件保留。

## 文档注释范本

### P1 PEP 257 单行 docstring（默认首选）
```python
def kos_root():
    """Return the pathname of the KOS root directory."""
```
要点：祈使句（Return / Compute / Parse…）、句号结尾、三引号起止同行、前后不留空行；不复读函数签名。

### P2 PEP 257 多行 docstring + Google 风格分节（仓库无一致风格时默认）
```python
def ⟨func⟩(⟨param1⟩, ⟨param2⟩=None):
    """⟨Summary line: imperative, fits on one line.⟩

    ⟨Elaborate description.⟩

    Args:
        ⟨param1⟩ (⟨int⟩): ⟨description⟩
        ⟨param2⟩ (⟨str, optional⟩): ⟨description⟩

    Returns:
        ⟨bool⟩: ⟨True if successful, False otherwise.⟩

    Raises:
        ⟨ValueError⟩: ⟨If ⟨condition⟩.⟩
    """
```
结构对齐 sphinxcontrib-napoleon 的 Google style 示例（Args / Returns / Raises / Attributes）。多行 docstring 的收尾 `"""` 独占一行。

### P3 NumPy 风格（仓库已统一使用时）
```python
def ⟨func⟩(⟨param1⟩, ⟨param2⟩):
    """⟨Summary line.⟩

    Parameters
    ----------
    ⟨param1⟩ : ⟨type⟩
        ⟨description⟩
    ⟨param2⟩ : ⟨type⟩, optional
        ⟨description⟩

    Returns
    -------
    ⟨type⟩
        ⟨description⟩

    Raises
    ------
    ⟨ValueError⟩
        ⟨If ⟨condition⟩.⟩
    """
```
生成器用 `Yields` 代替 `Returns`。节名下划线用与节名等宽的 `-----`。

### P4 reST/Sphinx 风格（仓库已使用时）
```python
def ⟨func⟩(⟨param1⟩):
    """⟨Summary line.⟩

    :param ⟨param1⟩: ⟨description⟩
    :type ⟨param1⟩: ⟨type⟩
    :returns: ⟨description⟩
    :rtype: ⟨type⟩
    :raises ⟨ValueError⟩: ⟨when⟩
    """
```

### P5 类 docstring（Google 风格）
```python
class ⟨Class⟩:
    """⟨Summary of the class.⟩

    ⟨Longer class description.⟩

    Attributes:
        ⟨attr1⟩ (⟨str⟩): ⟨description⟩
        ⟨attr2⟩ (⟨int, optional⟩): ⟨description⟩
    """
```
类 docstring 结束后空一行再写第一个方法（PEP 257）。实例属性也可用行内 `#:` 或赋值后 docstring 记录（napoleon 兼容写法）。

### P6 模块 docstring
```python
"""⟨One-line summary of the module.⟩

⟨Longer description: purpose, constraints, entry points.⟩
"""
```

## 行内注释范本（PEP 8 原文规则）

- **块注释**：与被描述代码同缩进，每行以 `# ` 开头（`#` 后一个空格）；段落之间用只含一个 `#` 的行分隔。
- **行内注释**：与语句间隔至少两个空格，`#` 后一个空格；少用。
- 完整句子、首词大写、句末句号（标识符开头的句子除外，不改标识符大小写）。
- PEP 8 原文：**过时的注释比没有注释更糟**；如代码变更使注释失真，更新或删除，而非修补。
- 语言：用英语，"unless you are 120% sure that the code will never be read by people who don't speak your language"（PEP 8）。

### P7 约束型（why）
```python
x = x + 1                 # Compensate for border
```
（PEP 8 官方正例；对照其反例 `# Increment x`——复述代码，禁止。）

```python
# ⟨Invariant/constraint sentence.⟩
⟨code⟩
```

### P8 workaround 型
```python
# ⟨Work around upstream bug ⟨URL⟩⟩. Remove when ⟨condition⟩.
⟨code⟩
```

## 任务标记

- 跨语言统一用 Google 风格：`# TODO: ⟨bug ID or link⟩ - ⟨what to do⟩`。
- 上下文优先给可追踪对象（bug/链接），避免只写人名（Google Java Style 明确反对 @username 型上下文）。
- 多行 TODO 保持块注释格式（每行 `# `）。

## 抑制与魔法注释清单（全部承重，禁止删除）

| 写法 | 来源 | 性质 |
|---|---|---|
| `# type: ignore[code]` | mypy | 抑制类型错误；`[code]` 限定错误码 |
| `# type: ⟨T⟩` | mypy | 类型注释（无注解时的类型来源） |
| `# noqa` / `# noqa: ⟨code⟩` | flake8/ruff | 抑制单行警告 |
| `# pylint: disable=⟨msg⟩` | pylint | 抑制检查 |
| `# pragma: no cover` | coverage.py | 排除覆盖率统计 |
| `# fmt: off` / `# fmt: on` | black / ruff format | 格式化岛，区间内格式不动 |
| `# ruff: noqa`、`# isort: skip_file` | ruff / isort | 文件级指令 |
| `#!/usr/bin/env python3` | shebang | 解释器选择，必须第一行 |
| `# -*- coding: utf-8 -*-` | PEP 263 | 编码声明 |
| `>>> ⟨expr⟩` + 期望输出 | doctest | docstring 内的 doctest 会被 pytest/doctest 执行 |

无 reason 的抑制指令可补 reason（见 rewrite-recipes R8，Python 用上一行 `# ⟨reason⟩`）。

## 工具约束

- pydocstyle / flake8-docstrings / ruff(pydocstyle) 规则族：D1xx（缺失 docstring）、D2xx（格式）、D4xx（内容）。仓库若启用，改写必须保持通过；未启用也不主动大范围补写私有符号的 docstring。
- black / ruff 会重排代码与注释缩进；`# fmt: off/on` 岛内内容保持原样。

## 来源

PEP 8 §Comments / §Documentation Strings（peps.python.org/pep-0008）；PEP 257（peps.python.org/pep-0257）；sphinxcontrib-napoleon example_google / example_numpy；mypy、flake8、coverage.py、black 官方文档。
