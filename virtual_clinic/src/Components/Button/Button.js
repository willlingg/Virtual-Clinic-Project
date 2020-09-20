import React from "react";
import "./Button.css";

export class Button extends React.Component {
  render() {
    return (
      <button class="button-gray" onClick={this.props.onClick}>
        {this.props.title}
      </button>
    );
  }
}

export default Button;
