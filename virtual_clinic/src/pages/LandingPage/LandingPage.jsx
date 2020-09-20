import React from "react";
import "../../App.css";
import Button from "../../Components/Button/Button";

import "./LandingPage.css";
import { Link } from "react-router-dom";

const LandingPage = () => {
  return (
    <div className="landing-page-container">
      <div className="portal-link">
        <Link className="sub-link" to="/patient">
          <Button title={"Log into the Patient Portal"}></Button>
        </Link>
        <br></br>
        <br></br>
        <br></br>
        <Link className="sub-link" to="/doctor">
          <Button title={"Log into the Doctor Portal"}></Button>
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;
