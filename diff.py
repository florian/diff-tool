"""A tool for diffing two given files.

Example usage:
    $ python diff.py file1.txt file2.txt

There are optional flags for hiding removals or additions and for showing line
numbers.
"""

from argparse import ArgumentParser
from differ import diff
from visualization import visualize

def _parse_args():
    parser = ArgumentParser(description="A tool for diffing.")

    parser.add_argument("file1", help="The original file to diff.")
    parser.add_argument("file2", help="The updated file to diff.")

    parser.add_argument("--hide_removals",
                        default=False,
                        action='store_true',
                        help="If set, removals are not shown.")
    parser.add_argument("--hide_additions",
                        default=False,
                        action='store_true',
                        help="If set, additions are not shown.")
    parser.add_argument("--show_line_numbers",
                        default=False,
                        action='store_true',
                        help="If set, line numbers are not shown.")

    return parser.parse_args()

def _read_lines_from_file(path):
    """Returns the lines without trailing new lines read from the given path."""
    with open(path, 'r') as f:
        return [line for line in f.read().splitlines()]

def main():
    args = _parse_args()

    lines1 = _read_lines_from_file(args.file1)
    lines2 = _read_lines_from_file(args.file2)

    visualize(diff(lines1, lines2),
              show_removals=not args.hide_removals,
              show_additions=not args.hide_additions,
              show_line_numbers=args.show_line_numbers,
    )

if __name__ == '__main__':
    main()
