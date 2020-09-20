import React from "react";
import "../../App.css";
import Header from "../../Components/Header/Header";

import PatientAppointments from "../../Components/PatientAppointments/PatientAppointments";

const Appointments = (props, state) => {
  const { doctor_id } = props.location.state;
  console.log(doctor_id);

  return (
    <div className="App">
      <Header portal="Upcoming Patient Consultations"></Header>
      <PatientAppointments doctor_id={doctor_id}></PatientAppointments>
    </div>
  );
};

export default Appointments;
