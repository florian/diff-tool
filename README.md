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
