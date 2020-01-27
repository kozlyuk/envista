/*
 *
 *   Submit component for data from table.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
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
			<div className="text-center mb-4">
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
