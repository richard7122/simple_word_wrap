# simple_word_wrap

Wrap text to a given column width while keeping each line's existing leading
whitespace on every continuation line it produces.

```python
from simple_word_wrap import wrap, wrap_lines

wrap("the quick brown fox jumps", 10)
# 'the quick\nbrown fox\njumps'

wrap_lines("    alpha beta gamma delta", 12)
# ['    alpha', '    beta', '    gamma', '    delta']
```

## Why this exists

The standard library's `textwrap` treats indentation as something to strip and
reapply, which is convenient for prose but loses the exact prefix a line
started with. When the input is source code, log output, or a template with
meaningful leading tabs, that loss is a bug. This library takes the narrow
position that a line's indentation is simply the run of spaces and tabs at its
start, and that every continuation line inherits that same prefix verbatim.

## What it does not do

Words longer than the available width are emitted whole rather than being
split. Splitting would silently mangle identifiers, URLs, and hashes, so the
caller decides whether to pre-split them. A line whose indentation already
meets or exceeds the requested width is returned unchanged. A non-positive
width returns the input split into lines, since there is no wrapping to do.

## API

- `wrap(text, width) -> str`
- `wrap_lines(text, width) -> list[str]`

`width` is the total column budget for each output line, including its
indentation. Both functions raise `TypeError` if `width` is not an `int`.
