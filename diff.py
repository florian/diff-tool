"""A tool for diffing two given files.

Example usage:
    $ python3 diff.py file1.txt file2.txt

There are also some optional flags below.
"""

from argparse import ArgumentParser
from differ import diff
from visualization import visualize_unified, visualize_sxs

def _setup_arg_parser():
    """Sets up the command line argument parser."""
    parser = ArgumentParser(description="A tool for diffing.")

    parser.add_argument("file1", help="The original file to diff.")
    parser.add_argument("file2", help="The updated file to diff.")

    parser.add_argument("--unified_view",
                        default=False,
                        action='store_true',
                        help="If set, the diff is shown in one view. "
                        "Otherwise they are shown in a split view.")
    parser.add_argument("--show_line_numbers",
                        default=False,
                        action='store_true',
                        help="If set, line numbers are not shown. "
                        "This mostly useful for the split view.")

    return parser

def _read_lines_from_file(path):
    """Returns the lines without trailing new lines read from the given path."""
    with open(path, 'r') as f:
        return [line for line in f.read().splitlines()]

def main():
    args = _setup_arg_parser().parse_args()

    lines1 = _read_lines_from_file(args.file1)
    lines2 = _read_lines_from_file(args.file2)

    diff_result = diff(lines1, lines2)

    if args.unified_view:
        visualize_unified(diff_result, args.show_line_numbers)
    else:
        visualize_sxs(diff_result, args.show_line_numbers)

if __name__ == '__main__':
    main()
