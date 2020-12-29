# React Diffing Visualization

This is the exact same algorithm as the Python code, but just reimplemented in
JS so that it can be visualized with React nicely. See the [blog post](http://florian.github.io/diffing)
for a live demo.

Note that I haven't written much JavaScript in the past few years, so this
code is not amazing. If you're looking to understand the algorithm, I suggest
reading the Python code instead, as it is also better commented.

## Usage

```javascript
ReactDOM.render(<DiffVisualization
                  title="Diff Visualization"
                  leftText={someText},
                  rightText={someOtherText} />,
  document.getElementById("diff-view"))
```

You can also use `showUnified` for a single diff view.

```javascript
ReactDOM.render(<DiffVisualization
                  title="Unified Diff Visualization"
                  leftText={someText},
                  rightText={someOtherText}
                  showUnified={true} />,
  document.getElementById("unified-diff-view"))
```
