/*
 * *
 *  * Background component.
 *  *
 *  * @author    Andrey Perestyuk (Arrathilar)
 *  * @email-primary a.perestyuk@itel.rv.ua
 *  * @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *  * @copyright 2020 ITEL-Service
 *
 *
 */


import React from "react";

export default class ButtonBackground extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isChecked: false
		}
	}

	doChecked() {
		this.setState({isChecked: true})
	}

	render() {
		return (
			<div style={{borderRadius: "5px", backgroundColor: this.state.isChecked ? "#159ba7" : "#fff"}}
				 onClick={() => {
					 this.doChecked()
				 }}>
				{this.props.children}
			</div>
		)
	}
}


