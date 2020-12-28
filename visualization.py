"""Visualizes diffing results."""

import math
from differ import Addition, Removal, Unchanged

_TERM_CODE_RED = 31
_TERM_CODE_GREEN = 32

# Represents a filler block for diff views.
_EMPTY_FILLER_CHANGE = Unchanged("")

def _color(content, term_code):
    """Colors the content using the given Terminal code."""
    return f"\x1b[{term_code}m{content}\x1b[0m"

def _red(content):
    """Colors the text in red."""
    return _color(content, _TERM_CODE_RED)

def _green(content):
    """Colors the text in green."""
    return _color(content, _TERM_CODE_GREEN)

def _format_diff_lines(diff, pad=0, show_removals=True,
                       show_additions=True, show_line_numbers=False):
    """Formats the lines of a diffing result with lines padded."""
    result = []

    num_digits = math.ceil(math.log(len(diff), 10))
    prefix_format = f"[%.{num_digits}d] "

    line_num = 1
    spacing = " " * 2
    # +1 to account for "+" and "-".
    hidden_spacing = pad + len(spacing) + 1

    for element in diff:
        if show_line_numbers:
            if element is _EMPTY_FILLER_CHANGE:
                prefix = " " * len(prefix_format % 0)
            else:
                prefix = prefix_format % line_num
                line_num += 1
        else:
            prefix = ""

        if isinstance(element, Addition):
            if show_additions:
                result.append(_green(f"{prefix}+{spacing}{element.content.ljust(pad)}"))
            else:
                result.append("".ljust(hidden_spacing))
        if isinstance(element, Removal):
            if show_removals:
                result.append(_red(f"{prefix}-{spacing}{element.content.ljust(pad)}"))
            else:
                result.append("".ljust(hidden_spacing))
        if isinstance(element, Unchanged):
            result.append(f"{prefix} {spacing}{element.content.ljust(pad)}")

    return result

def visualize_unified(diff, show_line_numbers):
    """Visualizes a diffing result in a unified view."""
    diff_lines =  _format_diff_lines(diff,
                                     show_removals=True,
                                     show_additions=True,
                                     show_line_numbers=show_line_numbers)
    for line in diff_lines:
        print(line)


def _diff_to_sxs_diffs(diff):
    """Takes a diffing result and creates diffing results for left and right."""
    left = []
    right = []

    # We need to keep track of how far to move Additions/Removals up.
    last_free_i = 0

    for i, element in enumerate(diff):
        if isinstance(element, Removal):
            left.append(element)

        if isinstance(element, Addition):
            right.append(element)

        if isinstance(element, Unchanged) or i == len(diff) - 1:
            pad = max(len(left), len(right))
            add_left = max(0, pad - len(left))
            add_right = max(0, pad - len(right))

            left += [_EMPTY_FILLER_CHANGE] * add_left
            right += [_EMPTY_FILLER_CHANGE] * add_right

        if isinstance(element, Unchanged):
            last_free_i = i
            left.append(element)
            right.append(element)


    assert len(left) == len(right), (
            "Expected left len %d == right len %d." % (len(left), len(right)))

    return left, right

def visualize_sxs(diff, show_line_numbers):
    """Visualizes a diffing result in a side-by-side view."""
    # We pad by the maximum line length of the left side.
    left_pad = max(len(element.content)
                   for element in diff
                   if not isinstance(element, Addition))

    left_diff, right_diff = _diff_to_sxs_diffs(diff)
    left_lines = _format_diff_lines(left_diff, left_pad,
                                    show_removals=True,
                                    show_additions=False,
                                    show_line_numbers=show_line_numbers)
    right_lines = _format_diff_lines(right_diff, left_pad,
                                     show_removals=False,
                                     show_additions=True,
                                     show_line_numbers=show_line_numbers)

    spacing = " " * 3
    for left, right in zip(left_lines, right_lines):
        print(f"{left}{spacing}|{spacing}{right}")
