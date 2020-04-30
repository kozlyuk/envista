/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */
import React from "react";
import {Button} from "react-bootstrap";
import {withRouter} from 'react-router-dom'

interface SubmitProps {
  title?: string
  history?: any
  redirectTo?: string
}

class Submit extends React.Component <SubmitProps, {}> {
  send() {
    const {history} = this.props;
    const {push} = history;
    push(this.props.redirectTo)
  }

  render() {
    return (
      <div className="text-center mb-4 ml-auto mr-auto">
        <Button
          variant="outline-success"
          size="sm"
          onClick={() => {
            this.send();
          }}>
          {this.props.title}
        </Button>
      </div>
    );
  }
}

// @ts-ignore
export default withRouter(Submit)
