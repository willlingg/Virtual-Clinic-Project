import React from "react";
import Logo from "../virtualClinicLogo/virtualClinicLogo";
import Button from "../Button/Button";
import "./Header.css";
import { Link } from "react-router-dom";

const Header = (props) => {
  function goBack() {
    window.history.back();
  }
  if (props.pageType === "patient" || props.pageType === "doctor") {
    return (
      <div className="header-border">
        <div className="header" id="headerDiv">
          <Logo></Logo>
          <h1 className="portal-title">{props.portal}</h1>
          <div className="button-container">
            {props.pageType === "patient" && (
              <Link
                to={{
                  pathname: "/patientAppointments",
                  state: { patient_id: 1 },
                }}
              >
                <Button title={"View your appointments"}></Button>
              </Link>
            )}
            {props.pageType === "doctor" && (
              <Link
                to={{
                  pathname: "/doctorAppointments",
                  state: { doctor_id: 1, user: "doctor" },
                }}
              >
                <Button title={"View upcoming consultations"}></Button>
              </Link>
            )}
          </div>
        </div>
      </div>
    );
  } else {
    return (
      <div className="header-border">
        <div className="header">
          <Logo></Logo>
          <h1 className="portal-title">{props.portal}</h1>
          <div className="button-container">
            <Button title={"Home"} onClick={goBack}></Button>
          </div>
        </div>
      </div>
    );
  }
};

export default Header;
