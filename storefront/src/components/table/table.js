import React from "react";

export class Table extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      array: props.array,
    };
  }

  decreaseQty(counter, columnIdx, rowIdx) {
    const newQty = this.state.counter > 0 ? this.state.counter - 1 : 0;
    let newArray = [...this.state.array];
    newArray[rowIdx].counters[columnIdx] = newQty;
    this.setState({ array: newArray });
  }

  recalculateTotal() {
    this.setState({ total: this.state.counter * 1 });
  }
  render() {
    return (
      <table className="table-bordered">
        <colgroup>
          <col style={{ width: 100, minWidth: 100 }} />
        </colgroup>
        <thead className="rc-table-thead text-center">
          <tr>
            <th className="rc-table-row-cell-break-word" />
            <th className="rc-table-row-cell-break-word">1,25</th>
          </tr>
        </thead>
        <tbody className="rc-table-tbody">
          {this.state.array.map((item, rowIdx) => (
            <tr
              key={rowIdx}
              className="rc-table-row rc-table-row-level-0"
              data-row-key={1}
            >
              <td className="rc-table-row-cell-break-word text-center">
                <span
                  className="rc-table-row-indent indent-level-0"
                  style={{ paddingLeft: 0 }}
                >
                  {item.rowName}
                </span>
              </td>
              {item.counters.map((counter, columnIdx) => (
                <td key={columnIdx} className="rc-table-row-cell-break-word">
                  <span
                    className="rc-table-row-indent indent-level-0"
                    style={{ paddingLeft: 0 }}
                  />
                  <button
                    className="btn btn-sm btn-light btn-block"
                    onClick={() => this.decreaseQty(counter, columnIdx, rowIdx)}
                  >
                    {counter}
                  </button>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
}
