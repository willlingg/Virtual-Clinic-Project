import React, { Fragment } from "react";
import "../../App.css";
import Header from "../../Components/Header/Header";
import "./Appointment.css";

import BookingContainer from "../../Components/BookingContainer/BookingContainer";

const AppointmentPage = (props, state) => {
  state = {
    doctor_id: null,
  };
  const { doctor_id, user, doctor_name } = props.location.state;

  //Set state
  if (user === "patient") {
    return (
      <div className="App">
        <Header portal="Appointment Management"></Header>
        <BookingContainer
          doctor_id={doctor_id}
          user={user}
          doctor_name={doctor_name}
        ></BookingContainer>
      </div>
    );
  } else {
    return <Fragment></Fragment>;
  }
};

export default AppointmentPage;
