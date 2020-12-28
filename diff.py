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

def _compute_longest_common_subsequence(text1, text2):
    n = len(text1)
    m = len(text2)

    lcs = [[None for _ in range(m + 1)]
                 for _ in range(n + 1)]

    for i in range(0, n + 1):
        for j in range(0, m + 1):
            if i == 0 or j == 0:
                lcs[i][j] = 0
            elif text1[i - 1] == text2[j - 1]:
                lcs[i][j] = 1 + lcs[i - 1][j - 1]
            else:
                lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])

    return lcs

def diff(text1, text2):
    lcs = _compute_longest_common_subsequence(text1, text2)

    i = len(text1)
    j = len(text2)

    results = []

    while i != 0 and j != 0:
        # If we reached the end of text1 (i == 0) or text2 (j == 0), then we
        # just need to print the remaining additions and removals.
        if i == 0:
            results.append(Addition(text2[j - 1]))
            j -= 1
        elif j == 0:
            results.append(Removal(text1[i - 1]))
            i -= 1
        # Otherwise there's still parts of text1 and text2 left. If the
        # currently considered part is equal, then we found an unchanged part,
        # which belongs to the longest common subsequence.
        elif text1[i - 1] == text2[j - 1]:
            results.append(Unchanged(text1[i - 1]))
            i -= 1
            j -= 1
        # In any other case, we go in the direction of the longest common
        # subsequence.
        elif lcs[i - 1][j] <= lcs[i][j - 1]:
            results.append(Addition(text2[j - 1]))
            j -= 1
        else:
            results.append(Removal(text1[i - 1]))
            i -= 1

    return reversed(results)



def visualize(results, show_remove, show_add):
    for element in results:
        if isinstance(element, Addition):
            print(green(f"+  {element.content}"))
        if isinstance(element, Removal):
            print(red(f"-  {element.content}"))
        if isinstance(element, Unchanged):
            print("  ", element.content)


def _read_lines_from_file(path: str) -> List[str]:
    with open(path, 'r') as f:
        return [line[:-1] for line in f]

def main():
    lines1 = _read_lines_from_file(sys.argv[1])
    lines2 = _read_lines_from_file(sys.argv[2])

    diffing_result = diff(lines1, lines2)
    visualize(diffing_result, show_remove=True, show_add=True)

if __name__ == '__main__':
    main()
