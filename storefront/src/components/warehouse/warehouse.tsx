/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import WarehouseTable from "../warehouseTable/WarehouseTable";
import Submit from "../submitTableData/submitTableData";
import {ButtonGroup} from "react-bootstrap";

export default class Warehouse extends React.Component<{}, {}> {
  history: any;

  constructor(props: any) {
    super(props);
    this.state = {
      needUpdateneedUpdate: false
    }
  }

  updateComponent = (value: boolean): any => {
    this.setState({
        needUpdate: value
      }
    )
  }

  render() {
    return (
      <div className="container">
        <div className="mobile-first w-col w-col-12">
          <h4 className="text-center">Таблиця поповнення складу</h4>
          {/*
					// @ts-ignore*/}
          <WarehouseTable needUpdate={this.state.needUpdate}/>
          <div className="text-center">
            <ButtonGroup vertical>
              <Submit history={this.history} title={"Підтвердити"} redirectTo={"/warehouse/confirm"}/>
            </ButtonGroup>
          </div>
        </div>
      </div>
    )
  }
}
