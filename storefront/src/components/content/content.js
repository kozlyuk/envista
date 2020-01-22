/**
 * Content component.
 *
 * @author           Andrey Perestyuk (Arrathilar)
 * @email-primary    a.perestyuk@itel.rv.ua
 * @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright        2020 ITEL-Service
 */

import React from "react";

import {Table} from "../table/table";
import Submit from "../submitTableData/submitTableData";
import PurchaseList from "../purchaseList/purchaseList";
import InfoBlock from "../infoBlock/infoBlock";
import {Container} from "react-bootstrap";
import axios from "axios";
import Auth from "../auth/auth";

export default class Content extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			purchase: [],
			array: []
		};
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
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

	componentDidMount() {
		axios(process.env.REACT_APP_INFO_CONTEXT, {
			headers: {
				Authorization: "Token " + this.authToken
			}
		}).then(
			result => {
				this.setState({
					isLoaded: true,
					product: result.data[0]
				});
				this.props.getData(this.state.product.brand_image);
			},
			error => {
				this.setState({
					isLoaded: true,
					error
				});
			}
		);
		return void 0;
	}

	render() {
		const {error, isLoaded} = this.state;
		if (error) {
			return <div>Помилка: {error.message}</div>;
		} else if (!isLoaded) {
			return <div>Загрузка...</div>;
		} else {
			return (
				<Container>
					<div className="w-row">
						<div className="mobile-second w-col w-col-6">
							{/* Header */}
							<h1 className="heading mt-0">
								<strong className="bold-text" data-ix="new-interaction">
									{this.state.product.title}
								</strong>
							</h1>
							{/* End of header */}
							<img
								src={this.state.product.product_image}
								alt={this.state.product.title}
								className="image-3"
							/>

							<InfoBlock info={this.state.product.short_description}/>
						</div>
						<div className="mobile-first w-col w-col-6">
							<h4 className="text-center">Таблиця наявності лінз на складі</h4>
							<Table getData={this.makePurchase} getArray={this.getArray}/>
							<PurchaseList
								purchaseList={this.state.purchase}
								array={this.state.array}
							/>
							{this.state.purchase.length !== 0 && (
								<Submit history={this.history} purchaseList={this.state.purchase}/>
							)}
						</div>
					</div>
				</Container>
			);
		}
	}
}
