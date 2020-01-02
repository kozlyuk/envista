import React from "react";

class Navbar extends React.Component {
  render() {
    return (
      <div
        data-collapse="medium"
        data-animation="default"
        data-duration={400}
        className="navbar w-nav"
      >
        <div className="d-flex justify-content-between w-container-flex">
          <a href="#" className="mr-auto p-2 m-0 brand w-nav-brand">
            <img
              src="https://uploads-ssl.webflow.com/5e01df57cdae92c47396eee8/5e048287478a40140bf39ce3_logo-crop.svg"
              height={50}
              alt="brand"
              className="image-2"
            />
          </a>
          <nav role="navigation" className="p-2 w-nav-menu">
            <a
              href="#"
              className="nav-link w-nav-link"
              style={{ maxWidth: 940 }}
            >
              Vendor main page
            </a>
            <a
              href="https://envista.toriccalculator.com/(S(3p54nq0ludca5hrzdtsqdtfl))/UserAgreement.aspx"
              target="_blank"
              className="nav-link-2 w-nav-link"
              style={{ maxWidth: 940 }}
            >
              Calculator
            </a>
            <a
              href="#"
              className="nav-link-3 w-nav-link"
              style={{ maxWidth: 940 }}
            >
              Logout
            </a>
          </nav>
          <div className="w-nav-button">
            <div className="w-icon-nav-menu" />
          </div>
        </div>
        <div className="w-nav-overlay" data-wf-ignore />
      </div>
    );
  }
}

export default Navbar;
