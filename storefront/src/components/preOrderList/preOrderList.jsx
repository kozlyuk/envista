/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";


export default class PreOrderList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      rows: [],
      columns: []
    };
  }


  render() {
    if (this.props.preOrderList.length !== 0) {
      return (
        <div className="text-center mb-4 ml-4 mr-4">
          <h4>Попереднє замовлення:</h4>
          <table className="table-bordered col mb-4">
            <tbody className="rc-table-tbody">
            <tr className="rc-table-row rc-table-row-level-0" data-row-key={1}>
              <td className="rc-table-row-cell-break-word text-center">
									<span
                    className="rc-table-row-indent indent-level-0"
                    style={{paddingLeft: 0}}>
										#
									</span>
              </td>
              <td className="rc-table-row-cell-break-word text-center">
									<span
                    className="rc-table-row-indent indent-level-0"
                    style={{paddingLeft: 0}}>
										Сфера
									</span>
              </td>
              <td className="rc-table-row-cell-break-word text-center">
									<span
                    className="rc-table-row-indent indent-level-0"
                    style={{paddingLeft: 0}}>
										Циліндр
									</span>
              </td>
            </tr>
            {this.props.preOrderList.map((item, index) => (
              <tr
                key={index}
                className="rc-table-row rc-table-row-level-0"
                data-row-key={1}>
                <td className="rc-table-row-cell-break-word text-center">
										<span
                      className="rc-table-row-indent indent-level-0"
                      style={{paddingLeft: 0}}>
											{index + 1}
										</span>
                </td>
                <td className="rc-table-row-cell-break-word text-center">
										<span
                      className="rc-table-row-indent indent-level-0"
                      style={{paddingLeft: 0}}>
											{this.props.array[0][1][item[1]].row} {/*[item[1]]*/}
										</span>
                </td>
                <td className="rc-table-row-cell-break-word text-center">
										<span
                      className="rc-table-row-indent indent-level-0"
                      style={{paddingLeft: 0}}>
											{this.props.array[0][0][item[0]]}
										</span>
                </td>
              </tr>
            ))}
            </tbody>
          </table>
        </div>
      );
    } else {
      return (
        <>
        </>
      )
    }
  }
}
