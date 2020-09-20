import React from "react";
import "./DoctorBlock.css";
import { Link } from "react-router-dom";

// Need to pull in doctor_id here

class DoctorBlock extends React.Component {
  render() {
    return (
      <div className="doc-block-container">
        <h2>Manage your upcoming appointments</h2>
        <Link
          to={{
            pathname: "/doctorAppointments",
            state: { doctor_id: 1, user: "doctor" },
          }}
        >
          Manage your upcoming appointments
        </Link>
      </div>
    );
  }
}

export default DoctorBlock;
