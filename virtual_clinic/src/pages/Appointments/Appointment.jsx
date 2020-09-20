import React from "react";
import "../../App.css";
import Header from "../../Components/Header/Header";

import AppointmentContainer from "../../Components/AppointmentContainer/AppointmentContainer";

const Appointments = (props, state) => {
  const { patient_id } = props.location.state;

  return (
    <div className="App">
      <Header portal="Upcoming Appointments"></Header>
      <AppointmentContainer patient_id={patient_id}></AppointmentContainer>
    </div>
  );
};

export default Appointments;
