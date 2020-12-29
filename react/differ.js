class DiffingElement {
  constructor(type, content) {
    this.type = type
    this.content = content
  }
}

Addition = (content) => new DiffingElement("added", content)
Removal = (content) => new DiffingElement("removed", content)
Unchanged = (content) => new DiffingElement("unchanged", content)
Buffer = (content) => new DiffingElement("buffer", "")

function compute_longest_common_subsequence(text1, text2) {
  const n = text1.length
  const m = text2.length

  var lcs = Array.from(Array(n + 1), () => Array(m + 1) )

  for(var i = 0; i <= n; i++) {
    for(var j = 0; j <= m; j++) {
      if (i == 0 || j == 0) {
        lcs[i][j] = 0
      } else if (text1[i - 1] == text2[j - 1]) {
        lcs[i][j] = 1 + lcs[i - 1][j - 1]
      } else {
        lcs[i][j] = Math.max(lcs[i - 1][j], lcs[i][j - 1])
      }
    }
  }

  return lcs
}

function diff(text1, text2) {
  const lcs = compute_longest_common_subsequence(text1, text2)
  var results = []

  var i = text1.length
  var j = text2.length

  while(i != 0 || j != 0) {
    if (i == 0) {
      results.push(Addition(text2[j - 1]))
      j -= 1
    } else if (j == 0) {
      results.push(Removal(text1[i - 1]))
      i -= 1
    } else if (text1[i - 1] == text2[j - 1]) {
      results.push(Unchanged(text1[i - 1]))
      i -= 1
      j -= 1
    } else if (lcs[i - 1][j] <= lcs[i][j - 1]) {
      results.push(Addition(text2[j - 1]))
      j -= 1
    } else {
      results.push(Removal(text1[i - 1]))
      i -= 1
    }
  }

  return results.reverse()
}

function diff_to_sxs_diff(diff) {
  left = []
  right = []

  var last_free_i = 0

  for (var i = 0; i < diff.length; i++) {
    const element = diff[i];

    if (element.type == "removed") {
      left.push(element)
    }

    if (element.type == "added") {
      right.push(element)
    }

    if (element.type == "unchanged" || i == diff.length - 1) {
      const pad = Math.max(left.length, right.length)
      const addLeft = Math.max(0, pad - left.length)
      const addRight = Math.max(0, pad - right.length)

      left = left.concat(Array(addLeft).fill(Buffer()))
      right = right.concat(Array(addRight).fill(Buffer()))
    }

    if (element.type == "unchanged") {
      last_free_i = i;
      left.push(element)
      right.push(element)
    }
  }

  return { left, right }
}
