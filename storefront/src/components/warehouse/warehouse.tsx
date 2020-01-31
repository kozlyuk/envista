/*
 *
 *   Warehouse component.
 *
 *   @author                  Andrey Perestyuk (Arrathilar)
 *   @email-primary           a.perestyuk@itel.rv.ua
 *   @email-secondary         arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright               2020 ITEL-Service
 *
 *
 */

import React from "react";
import WarehouseTable from "../warehouseTable/WarehouseTable";
import Submit from "../submitTableData/submitTableData";
import ResetButton from "../warehouseResetButton/warehouseResetButton";

export default class Warehouse extends React.Component<{}, {}> {
	history: any;

	constructor(props: any) {
		super(props);
	}

	render() {
		return (
			<div className="container">
				<div className="mobile-first w-col w-col-12">
					<h4 className="text-center">Таблиця поповнення складу</h4>
					<WarehouseTable/>
					<Submit history={this.history} title={"Підтвердити"} redirectTo={"/warehouse/confirm"}/>
					<ResetButton/>
				</div>
			</div>
		)
	}
}
