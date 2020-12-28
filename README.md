# Diffing Tool

Diffing tools show you what changed between two versions of a file.
You probably know this from code review tools, e.g. the one from GitHub.
I decided to implement my own diffing tool for fun. :)

## Usage

To show the diff between `file1` and `file2`:

```sh
$ python3 diff.py file1.txt file2.txt
```

There are several optional flags:

| Flag                | Description                     | Default                  |
| :-------------------|:--------------------------------|:-------------------------|
| `--hide_removals`   | If set, removals are hidden.    | Removals are shown       |
| `--hide_additions`  | If set, additions are hidden.   | Additions are shown.     |
| `show_line_numbers` | If set, line numbers are shown. | Line numbers are hidden. |

## Potential improvements

There's some things left that could be improved:

- Actually packaging this into a tool that could be easily installed
- Side-by-side view with only removals on the left and only additions on the right.
  This would also make the line numbers more useful
- Char-based diffing as opposed to line-based diffing. The algorithm would stay
  exactly the same. The only thing that would need to be updated is the visualization
- Faster line-based diffing. One could first hash all lines to make comparisons faster
