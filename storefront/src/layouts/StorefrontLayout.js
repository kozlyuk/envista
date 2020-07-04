import React, {Fragment} from 'react';
import NavbarMenu from "../components/navbar/navbarMenu";
import Footer from "../components/footer/footer";
import {GlobalContext} from "../context/GlobalContext";

class StorefrontLayout extends React.Component {

  render() {
    const {children} = this.props;
    return (
      <Fragment>
        <GlobalContext.Consumer>
          {value =>
            <NavbarMenu brandLogo={value.brandLogo} userEmail={value.user.email}
                        permission={value.permission}/>
          }
        </GlobalContext.Consumer>
        <div className="section">
          <div>
            {children}
          </div>
        </div>
        <GlobalContext.Consumer>
          {value =>
            <Footer title={value.footer}/>
          }
        </GlobalContext.Consumer>
      </Fragment>
    );
  }
}

export default StorefrontLayout;