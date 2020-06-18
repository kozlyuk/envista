/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import Auth from "../auth/auth";
import axios from "axios";
import {toast} from "react-toastify";
import "../table/style.css"
import Loader from "react-loader-spinner";
import {Sticky, StickyContainer} from 'react-sticky';
import TableButton from "./TableButton";


interface TableProps {
  rows?: any
  columnsName?: any
  error?: any
  isLoaded?: boolean
  makePurchase?: []
  makePreOrder?: []
}

export class Table extends React.PureComponent<{}, TableProps> {
  private user: Auth;
  protected readonly authToken: any;

  /**
   * Table constructor.
   *
   * @param props
   */
  constructor(props: any) {
    super(props);
    this.state = {
      rows: [],
      columnsName: [],
      error: null,
      isLoaded: false,
      makePurchase: [],
      makePreOrder: []
    };
    this.user = new Auth();
    this.authToken = this.user.getAuthToken();
  }

  /**
   * Decrease counter of item quantities and write to state
   *
   * @param event
   * @param counter
   * @param columnIdx
   * @param rowIdx
   */
  decreaseQty = (event: any, counter: number, columnIdx: number, rowIdx: number) => {
    const newQty = counter > 0 ? counter - 1 : 0;
    let newArray = [...this.state.rows];
    newArray[rowIdx].quantities[columnIdx] = newQty;
    if (counter === 0) {
      this.preOrder(rowIdx, columnIdx)
        .then(() => {
          this.setState({rows: newArray})
        })
        .catch(error => {
          const message = error.response.data;
          toast.error(message);
        })
    } else {
      this.sendData(rowIdx, columnIdx)
        .then(() => this.setState({rows: newArray}))
        .catch(error => {
          const message = error.response.data;
          toast.error(message);
        });
    }
    // send get request to backend, then setstate with new quantity
    this.getData(event, counter, columnIdx, rowIdx);
    this.getArray(this.state.columnsName, this.state.rows);
    return void 0;
  }

  /**
   * Pre order
   *
   * @param rowIdx
   * @param columnIdx
   */
  public async preOrder(rowIdx: number, columnIdx: number) {
    const row = rowIdx + 1;
    const col = columnIdx + 1;
    const {REACT_APP_ADD_TO_CARD}: any = process.env;
    return axios(REACT_APP_ADD_TO_CARD + row + "/" + col + "/", {
      headers: {
        "Authorization": "Token " + this.authToken
      }
    });
  }

  /**
   * Regular buy
   *
   * @param rowIdx
   * @param columnIdx
   */
  public async sendData(rowIdx: number, columnIdx: number) {
    const row = rowIdx + 1;
    const col = columnIdx + 1;
    const {REACT_APP_ADD_TO_CARD}: any = process.env;
    return axios(REACT_APP_ADD_TO_CARD + row + "/" + col + "/", {
      headers: {
        "Authorization": "Token " + this.authToken
      }
    });
  }

  /**
   * Send order data to parent component
   *
   * @param event
   * @param counter
   * @param columnIdx
   * @param rowIdx
   */
  public getData(event: any, counter: number, columnIdx: number, rowIdx: number) {
    if (counter !== 0) {
      /* eslint-disable react/no-direct-mutation-state */
      // @ts-ignore
      this.props.getData((this.state.makePurchase = ([columnIdx, rowIdx]))); //maybe need to add id
    } else if (counter === 0) {
      event.target.innerHTML = "п"
      /* eslint-disable react/no-direct-mutation-state */
      // @ts-ignore
      this.props.getPreOrderData((this.state.makePreOrder = ([columnIdx, rowIdx])));
    }
  }

  /**
   * Send array to parent component
   *
   * @param columnsName
   * @param rows
   */
  public getArray(columnsName: any, rows: any) {
    /* eslint-disable react/no-direct-mutation-state */
    let array: any;
    // @ts-ignore
    array = this.props.getArray((this.state.getArray = ([columnsName, rows]))); //maybe need to add id
    return void 0;
  }

  /*
   * componentDidMount(): void
   *
   * get data from backend => mount component
   */
  componentDidMount() {
    const {REACT_APP_TABLE_DATA}: any = process.env;
    axios(REACT_APP_TABLE_DATA, {
      headers: {
        "Authorization": "Token " + this.authToken
      }
    })
      .then(
        result => {
          this.setState({
            isLoaded: true,
            rows: result.data.rows,
            columnsName: result.data.columns
          });
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

  public render() {
    const {error, isLoaded} = this.state;
    if (error) {
      return <div>Помилка: {error.message}</div>;
    } else if (!isLoaded) {
      return (
        <div className="loaderWrapper text-center mt-4">
          <Loader
            type="MutatingDots"
            color="#007bff"
            height={100}
            width={100}
            timeout={3000} //3 secs

          />
          <h3 className="text-center text-muted">Завантаження...</h3>
        </div>)
        ;
    } else {
      return (
        <div className="col">


          <div className="row">
          </div>
          <div className="row">
            <table className="table-bordered col mb-4 header-fixed">
              <StickyContainer>
                <colgroup>
                  <col style={{width: 50, minWidth: 50}}/>
                </colgroup>
                <Sticky style={{zIndex: 1000}}>{({style}) =>
                  <thead style={style} className="rc-table-thead sticky border-0">
                  <tr style={{width: "57px"}} className="border-0">
                    <th style={{width: "57px"}}
                        className="rc-table-row-cell-break-word bg-white border-bottom-0"/>
                    {this.state.columnsName.map((name: string, rowIdx: number) => (
                      <th style={{width: "57px"}} key={rowIdx}
                          className="rc-table-row-cell-break-word text-info text-center bg-white border-bottom-0">
                        {name}
                      </th>
                    ))}
                  </tr>
                  </thead>
                }</Sticky>
                <tbody style={{display: "inline-table", width: "100%"}} className="rc-table-tbody">
                {this.state.rows.map((item: { row: React.ReactNode; quantities: any[]; }, rowIdx: string | number | undefined) => (
                  <tr key={rowIdx}
                      className="rc-table-row rc-table-row-level-0"
                      data-row-key={1}>
                    <td style={{width: "57px"}}
                        className="rc-table-row-cell-break-word text-center">
									<span className="rc-table-row-indent indent-level-0 font-weight-bold text-primary"
                        style={{paddingLeft: 0}}>{item.row}</span>
                    </td>
                    {item.quantities.map((counter, columnIdx) => (
                      <td
                        style={{width: "57px"}}
                        key={columnIdx}
                        className="rc-table-row-cell-break-word">
											<span
                        className="rc-table-row-indent indent-level-0"
                        style={{paddingLeft: 0}}
                      />
                        <div>
                          <TableButton decreaseQty={this.decreaseQty} counter={counter} columnIdx={columnIdx}
                                       rowIdx={rowIdx}/>
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
                <tr className="text-center">
                  <th className="rc-table-row-cell-break-word"/>
                  {this.state.columnsName.map((name: string, rowIdx: number) => (
                    <th key={rowIdx} className="rc-table-row-cell-break-word text-info">
                      {name}
                    </th>
                  ))}
                </tr>
                </tbody>
              </StickyContainer>
            </table>
          </div>

        </div>
      );
    }
  }
}
