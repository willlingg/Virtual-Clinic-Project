import React from "react";
import "./DoctorList.css";
import { Link } from "react-router-dom";

const DoctorList = (props) => {
  const doctor_id = props.id;
  const doctor_name = props.firstName + " " + props.lastName;

  return (
    <div className="doctor-container">
      <div className="left-container">
        <img className="profile-pic" src="profile.png"></img>
        <div className="doc-details">
          <h2>Dr. {doctor_name}</h2>
          <p>General Practitioner</p>
          <p></p>
        </div>
      </div>

      <div className="appointment-link">
        <Link
          to={{
            pathname: "/appointment",
            state: {
              doctor_id: doctor_id,
              user: "patient",
              doctor_name: doctor_name,
            },
          }}
        >
          Book with Dr. {doctor_name}
        </Link>
      </div>
    </div>
  );
};

export default DoctorList;
