// import Table from "rc-table";
import React from "react";

import { Table } from "../table/table";
// //requests to db
// let tableData = new Ajax();
// const data = tableData.get("http://localhost:3004/data").then(response => {

//   return JSON.parse(response);
// });

class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      array: props.array,
    };
  }
  render() {
    return (
      <div className="section mt-2">
        <div className="w-container">
          <div className="w-row">
            <div className="column w-col w-col-6">
              <img
                src="https://uploads-ssl.webflow.com/5e01df57cdae92c47396eee8/5e01e2369802edbf02b8f0e0_csm_enVista-Toric_920x632_7b811276fa.png"
                alt="product"
                className="image-3"
              />
              {/* Form start */}
              <div className="form-block w-form">
                <form
                  action=""
                  id="email-form"
                  name="email-form"
                  data-name="Email Form"
                  className="form"
                >
                  <label htmlFor="name" className="field-label">
                    First value
                  </label>
                  <select id="field" name="field" className="select-2">
                    <option value="none">Select one...</option>
                    <option value="First">First Choice</option>
                    <option value="Second">Second Choice</option>
                    <option value="Third">Third Choice</option>
                  </select>
                  <label htmlFor="email" className="field-label-2">
                    Second value
                  </label>
                  <select
                    id="field-2"
                    name="field-2"
                    data-name="Field 2"
                    className="select-2"
                  >
                    <option value="none">Select one...</option>
                    <option value="First">First Choice</option>
                    <option value="Second">Second Choice</option>
                    <option value="Third">Third Choice</option>
                  </select>
                  <label className="field-label-3">Quantity</label>
                  <input
                    type="text"
                    className="text-field w-input"
                    maxLength={256}
                    name="field-3"
                    data-name="Field 3"
                    placeholder={"100"}
                    id="field-3"
                    required
                  />
                  {/* Block with pdf button */}
                  <div className="div-block">
                    <input
                      type="submit"
                      defaultValue="Approve order"
                      data-wait="Please wait..."
                      className="submit-button w-button"
                    />
                    <a href="/" className="button w-button">
                      View PDF
                    </a>
                  </div>
                  {/* End block with pdf button */}
                </form>
                <div className="w-form-done">
                  <div>Thank you! Your submission has been received!</div>
                </div>
                <div className="w-form-fail">
                  <div>
                    Oops! Something went wrong while submitting the form.
                  </div>
                </div>
              </div>
              {/* Form end */}
            </div>
            <div className="w-col w-col-6">
              {/* Header */}
              <h1 className="heading">
                <strong className="bold-text" data-ix="new-interaction">
                  enVista® Toric Intraocular Lens
                </strong>
              </h1>
              {/* End of header */}
              <Table />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Content;
