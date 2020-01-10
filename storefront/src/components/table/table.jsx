import React from "react";

export class Table extends React.PureComponent {
	constructor(props) {
		super(props);
		this.state = {
			rows: [],
			columnsName: [],
			error: null,
			isLoaded: false
		};
	}

	//decrease counter of item quantity and write to state
	decreaseQty(counter, columnIdx, rowIdx) {
		const newQty = counter > 0 ? counter - 1 : 0;
		let newArray = [...this.state.rows];
		newArray[rowIdx].counters[columnIdx] = newQty;
		this.setState({ rows: newArray });
		this.getData(counter, columnIdx, rowIdx);
	}

	//send data to parent component
	getData(counter, columnIdx, rowIdx) {
		if (counter !== 0) {
			// const id = rowIdx.toString() + columnIdx.toString();
			this.props.getData((this.state.makePurchase = [columnIdx, rowIdx])); //maybe need to add id
		}
	}

	//get data from backend => then mount component
	componentDidMount() {
		fetch(process.env.REACT_APP_TABLE_DATA)
			.then(res => res.json())
			.then(
				result => {
					this.setState({
						isLoaded: true,
						rows: result[0].rows,
						columnsName: result[0].columnsName
					});
				},
				error => {
					this.setState({
						isLoaded: true,
						error
					});
				}
			);
	}

	render() {
		const { error, isLoaded } = this.state;
		if (error) {
			return <div>Помилка: {error.message}</div>;
		} else if (!isLoaded) {
			return <div>Загрузка...</div>;
		} else {
			return (
				<div className="row">
					<table className="table-bordered col mb-4">
						<colgroup>
							<col style={{ width: 50, minWidth: 50 }} />
						</colgroup>
						<thead className="rc-table-thead text-center">
							<tr>
								<th className="rc-table-row-cell-break-word" />
								{this.state.columnsName.map((name, rowIdx) => (
									<th key={rowIdx} className="rc-table-row-cell-break-word">
										{name}
									</th>
								))}
							</tr>
						</thead>
						<tbody className="rc-table-tbody">
							{this.state.rows.map((item, rowIdx) => (
								<tr
									key={rowIdx}
									className="rc-table-row rc-table-row-level-0"
									data-row-key={1}>
									<td className="rc-table-row-cell-break-word text-center">
										<span
											className="rc-table-row-indent indent-level-0"
											style={{ paddingLeft: 0 }}>
											{item.rowName}
										</span>
									</td>
									{item.counters.map((counter, columnIdx) => (
										<td
											key={columnIdx}
											className="rc-table-row-cell-break-word">
											<span
												className="rc-table-row-indent indent-level-0"
												style={{ paddingLeft: 0 }}
											/>
											<button
												className="btn btn-sm btn-light btn-block"
												onClick={() =>
													this.decreaseQty(counter, columnIdx, rowIdx)
												}>
												{counter}
											</button>
										</td>
									))}
								</tr>
							))}
						</tbody>
					</table>
				</div>
			);
		}
	}
}
