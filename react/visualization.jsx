class DiffVisualization extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      view: "diff",
      showUnified: props.showUnified || false,
      leftText: props.leftText,
      rightText: props.rightText,
      ...this.computeDiff(props.leftText, props.rightText)
    }
  }

  render () {
    return <div className="diff-visualization">
      <h4>Live Demo: {this.props.title}</h4>
      { this.state.view == "edit" ? this.renderEdit() : this.renderDiff() }
  </div>
  }

  renderEdit () {
    return <div>
      <div className="diff-wrapper">
        <div className="diff-side">
          <textarea ref="leftTextarea"
            value={this.state.leftText}
            style={{height: this.state.leftTextAreaHeight + "px"}}
            onChange={this.handleLeftTextarea.bind(this)} />
         </div>
        <div className="diff-side right-diff-side">
          <textarea ref="rightTextarea"
            value={this.state.rightText}
            style={{height: this.state.rightTextAreaHeight + "px"}}
            onChange={this.handleRightTextarea.bind(this)} />
        </div>
     </div>
     <button onClick={this.switchState.bind(this)}>Show diff</button>
    </div>
  }

  renderDiff (height) {
    if (this.state.showUnified) {
      return <div>
               <div className="diff-wrapper">
                 <div className="diff-full">
                   <ul className="diff-results">
                     {this.state.unifiedDiff.map(this.renderDiffElement.bind(this))}
                   </ul>
                 </div>
              </div>
              <button onClick={this.switchState.bind(this)}>Edit</button>
            </div>
    } else {
    return <div>
             <div className="diff-wrapper">
               <div className="diff-side">
                 <ul className="diff-results">
                   {this.state.leftDiff.map(this.renderDiffElement.bind(this))}
                 </ul>
               </div>
               <div className="diff-side right-diff-side">
                 <ul className="diff-results">
                   {this.state.rightDiff.map(this.renderDiffElement.bind(this))}
                 </ul>
               </div>
             </div>
             <button onClick={this.switchState.bind(this)}>Edit</button>
           </div>
     }
  }

  renderDiffElement (element) {
    return <li className={"diff-change diff-" + element.type}>{element.content}</li>
  }

  componentDidUpdate() {
    if (this.state.view == "edit" &&
            (this.state.leftTextAreaHeight != this.refs.leftTextarea.scrollHeight
          || this.state.rightTextAreaHeight != this.refs.rightTextarea.scrollHeight)) {
      this.setState({
        leftTextAreaHeight: this.refs.leftTextarea.scrollHeight,
        rightTextAreaHeight: this.refs.rightTextarea.scrollHeight
      })
    }
  }

  switchState(e) {
    if (this.state.view == "edit") {
      this.setState({view: "diff",
                     ...this.computeDiff(this.state.leftText, this.state.rightText)})
    } else{
      this.setState({view: "edit"})
    }
  }

  handleLeftTextarea (e) {
    // HACK: This needs to be set outside of React apparently.
    e.target.style.height = 'inherit'
    e.target.style.height = e.target.scrollHeight + "px"
    this.setState({ leftText: e.target.value, leftTextAreaHeight: e.target.scrollHeight })
  }

  handleRightTextarea (e) {
  // HACK: This needs to be set outside of React apparently.
    e.target.style.height = 'inherit'
    e.target.style.height = e.target.scrollHeight + "px"
    this.setState({ rightText: e.target.value, rightTextAreaHeight: e.target.scrollHeight })
  }

  computeDiff (leftText, rightText) {
    var leftText = leftText.split("\n")
    var rightText = rightText.split("\n")

    var unifiedDiff = diff(leftText, rightText)
    var {left, right} = diff_to_sxs_diff(unifiedDiff)

    return { leftDiff: left, rightDiff: right, unifiedDiff }
  }
}
