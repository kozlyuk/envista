/**
 * Content component.
 *
 * @author    Andrey Perestyuk (Arrathilar)
 * @email-primary a.perestyuk@itel.rv.ua
 * @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright 2020 ITEL-Service
 */


import React from "react";

import {Table} from "../table/table";
import Submit from "../submitTableData/submitTableData";
import PurchaseList from "../purchaseList/purchaseList";
import InfoBlock from "../infoBlock/infoBlock";
import {Container} from "react-bootstrap";

class Content extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			purchase: [],
			array: []
		};
	}

	count(array) {
		let counts = {};
		array.map(x => {
			counts[x] = (counts[x] || 0) + 1;
		});
		return counts;
	}

	//get data from child component and put into state
	makePurchase = purchase => {
		this.setState(prevState => ({
			purchase: [...prevState.purchase, purchase]
		}));
	};

	//get table data from child component and put into state
	getArray = array => {
		this.setState(prevState => ({
			array: [...prevState.array, array]
		}));
	};

	render() {
		return (
			<Container>
				<div className="w-row">
					<div className="mobile-second w-col w-col-6">
						{/* Header */}
						<h1 className="heading mt-0">
							<strong className="bold-text" data-ix="new-interaction">
								enVista® Toric Intraocular Lens
							</strong>
						</h1>
						{/* End of header */}
						<img
							src="https://uploads-ssl.webflow.com/5e01df57cdae92c47396eee8/5e01e2369802edbf02b8f0e0_csm_enVista-Toric_920x632_7b811276fa.png"
							alt="product"
							className="image-3"
						/>

						<InfoBlock/>
					</div>
					<div className="mobile-first w-col w-col-6">
						<h4 className="text-center">Таблиця наявності лінз на складі</h4>
						<Table getData={this.makePurchase} getArray={this.getArray}/>
						<PurchaseList purchaseList={this.state.purchase} array={this.state.array}/>
						{this.state.purchase.length !== 0 && (
							<Submit purchaseList={this.state.purchase}/>
						)}
					</div>
				</div>
			</Container>
		);
	}
}

export default Content;
