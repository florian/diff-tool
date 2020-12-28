import sys
from typing import List
from dataclasses import dataclass

@dataclass
class Addition:
    content: str

@dataclass
class Removal:
    content: str

@dataclass
class Unchanged:
    content: str

TERM_CODE_RED = 31
TERM_CODE_GREEN = 32

def _color(content, term_code):
    return f"\x1b[{term_code}m{content}\x1b[0m"

def red(content):
    return _color(content, TERM_CODE_RED)

def green(content):
    return _color(content, TERM_CODE_GREEN)

class Differ:
    def __init__(self, text1, text2):
        self._text1 = text1
        self._text2 = text2
        self._lcs = self._compute_longest_common_subsequence()

    def _compute_longest_common_subsequence(self):
        n = len(self._text1)
        m = len(self._text2)

        lcs = [[None for _ in range(m + 1)]
                     for _ in range(n + 1)]

        for i in range(0, n + 1):
            for j in range(0, m + 1):
                if i == 0 or j == 0:
                    lcs[i][j] = 0
                elif self._text1[i - 1] == self._text2[j - 1]:
                    lcs[i][j] = 1 + lcs[i - 1][j - 1]
                else:
                    lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])

        return lcs

    def diff(self, show_remove, show_add):
        results = []
        self._recursive_diff(results, show_remove, show_add, len(self._text1), len(self._text2))

        for element in results:
            if isinstance(element, Addition):
                print(green(f"+  {element.content}"))
            if isinstance(element, Removal):
                print(red(f"-  {element.content}"))
            if isinstance(element, Unchanged):
                print("  ", element.content)

    def _recursive_diff(self, results, show_remove, show_add, i, j):
        if i == j == 0:
            return
        elif i == 0:
            self._recursive_diff(results, show_remove, show_add, i, j - 1)
            results.append(Addition(self._text2[j - 1]))
        elif j == 0:
            self._recursive_diff(results, show_remove, show_add, i - 1, j)
            results.append(Removal(self._text1[i - 1]))
        elif self._text1[i - 1] == self._text2[j - 1]:
            self._recursive_diff(results, show_remove, show_add, i - 1, j - 1)
            results.append(Unchanged(self._text1[i - 1]))
        elif self._lcs[i - 1][j] <= self._lcs[i][j - 1]:
            self._recursive_diff(results, show_remove, show_add, i, j - 1)
            results.append(Addition(self._text2[j - 1]))
        else:
            self._recursive_diff(results, show_remove, show_add, i - 1, j)
            results.append(Removal(self._text1[i - 1]))


def _read_lines_from_file(path: str) -> List[str]:
    with open(path, 'r') as f:
        return [line[:-1] for line in f]

def main():
    lines1 = _read_lines_from_file(sys.argv[1])
    lines2 = _read_lines_from_file(sys.argv[2])

    differ = Differ(lines1, lines2)
    differ.diff(show_remove=True, show_add=True)

if __name__ == '__main__':
    main()
