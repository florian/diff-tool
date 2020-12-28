"""Visualizes diffing results."""

import math
from differ import Addition, Removal, Unchanged

_TERM_CODE_RED = 31
_TERM_CODE_GREEN = 32

def _color(content, term_code):
    """Colors the content using the given Terminal code."""
    return f"\x1b[{term_code}m{content}\x1b[0m"

def _red(content):
    """Colors the text in red."""
    return _color(content, _TERM_CODE_RED)

def _green(content):
    """Colors the text in green."""
    return _color(content, _TERM_CODE_GREEN)

def visualize(diff, show_removals, show_additions, show_line_numbers):
    """Visualizes a diffing result."""
    num_digits = math.ceil(math.log(len(diff), 10))
    prefix_format = f"[%.{num_digits}d] "

    for line_number, element in enumerate(diff):
        if show_line_numbers:
            prefix = prefix_format % (line_number + 1)
        else:
            prefix = ""

        if isinstance(element, Addition) and show_additions:
            print(_green(f"{prefix}+  {element.content}"))
        if isinstance(element, Removal) and show_removals:
            print(_red(f"{prefix}-  {element.content}"))
        if isinstance(element, Unchanged):
            print(f"{prefix}  ", element.content)
