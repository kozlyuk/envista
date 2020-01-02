import React from "react";
import Navbar from "../navbar/navbar";
import Content from "../content/content";
import Footer from "../footer/footer";

class Welcome extends React.Component {
  render() {
    return (
      <div>
        <Navbar/>
        <Content/>
        <Footer/>
      </div>
    );
  }
}

export default Welcome;
