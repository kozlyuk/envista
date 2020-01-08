/** @format */

// import Table from "rc-table";
import React from "react";

import { Table } from "../table/table";
import Submit from "../submitTableData/submitTableData";
import PurchaseList from "../purchaseList/purchaseList";

class Content extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			purchase: []
		};
	}

	//get data from child component and put it to state
	makePurchase = purchase => {
		this.setState(prevState => ({
			purchase: [...prevState.purchase, purchase]
		}));
	};

	render() {
		return (
			<div className="section">
				<div className="w-container">
					<div className="w-row">
						<div className="column w-col w-col-6">
							<img
								src="https://uploads-ssl.webflow.com/5e01df57cdae92c47396eee8/5e01e2369802edbf02b8f0e0_csm_enVista-Toric_920x632_7b811276fa.png"
								alt="product"
								className="image-3"
							/>
							<PurchaseList purchaseList={this.state.purchase} />
							{this.state.purchase.length !== 0 && (
								<Submit purchaseList={this.state.purchase} />
							)}
						</div>
						<div className="w-col w-col-6">
							{/* Header */}
							<h1 className="heading">
								<strong className="bold-text" data-ix="new-interaction">
									enVista® Toric Intraocular Lens
								</strong>
							</h1>
							{/* End of header */}
							<Table getData={this.makePurchase} />
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default Content;
