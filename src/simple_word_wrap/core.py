"""Word wrapping that preserves a line's existing indentation.

Design decision: a line's indentation is the leading run of space and tab
characters. Continuation lines produced from that line receive the same
indentation prefix. This is the single interpretation the library implements:
indentation is a prefix, not a hanging indent, and it is not re-derived from
paragraph context.

Words longer than the available width are emitted intact on their own line
rather than being split. Splitting would silently corrupt identifiers, URLs,
and long tokens, so the caller keeps the choice of whether to pre-split them.
"""

from __future__ import annotations

from typing import Iterable, List

__all__ = ["wrap", "wrap_lines"]


def _leading_whitespace(line: str) -> str:
    """Return the leading run of spaces and tabs from ``line``."""
    i = 0
    while i < len(line) and line[i] in " \t":
        i += 1
    return line[:i]


def _wrap_single_line(line: str, width: int) -> List[str]:
    """Wrap one line, reusing its leading whitespace on every output line."""
    indent = _leading_whitespace(line)
    body = line[len(indent):]

    # A line that is only whitespace (or empty) is returned unchanged. There is
    # no content to wrap, and inventing continuation lines would change the
    # caller's layout for no benefit.
    if body == "":
        return [line]

    if width <= len(indent):
        # No room for content after the indent. The only faithful choice is to
        # leave the line alone; trimming the indent would lose information.
        return [line]

    available = width - len(indent)
    words = body.split()
    if not words:
        return [line]

    out: List[str] = []
    current = words[0]
    for word in words[1:]:
        # A word that cannot fit even on an empty continuation line is placed
        # on its own line. We never split it.
        if len(current) + 1 + len(word) <= available:
            current = current + " " + word
        else:
            out.append(indent + current)
            current = word
    out.append(indent + current)
    return out


def wrap_lines(text: str, width: int) -> List[str]:
    """Wrap ``text`` to ``width`` columns and return the resulting lines.

    Existing line breaks are preserved: each input line is wrapped
    independently. Explicit trailing newlines are not represented in the
    result, so ``"a\n"`` and ``"a"`` both yield ``["a"]``. Use ``wrap`` when a
    single string is wanted.

    ``width`` is the total column budget for each output line, including the
    line's indentation. A non-positive ``width`` returns the input lines
    unchanged, because there is no sensible wrapping to perform.
    """
    if not isinstance(width, int):
        raise TypeError("width must be an int")
    if width <= 0:
        return text.splitlines()

    result: List[str] = []
    for line in text.splitlines():
        result.extend(_wrap_single_line(line, width))
    return result


def wrap(text: str, width: int) -> str:
    """Wrap ``text`` to ``width`` columns and return it as a single string."""
    return "\n".join(wrap_lines(text, width))
