import React, { useState, useEffect } from "react";
import "../../App.css";
import Header from "../../Components/Header/Header";
import Intro from "../../Components/Intro/Intro";
import DoctorList from "../../Components/DoctorList/DoctorList";

const PatientPage = () => {
  const [doctorList, setDoctorList] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    async function getDoctors() {
      try {
        let docResponse = await fetch("/doctors");
        let doctors = await docResponse.json();
        setDoctorList(doctors);
        setIsLoaded(true);
      } catch (err) {
        console.log(err);
      }
    }
    getDoctors();
  }, []);

  if (isLoaded) {
    return (
      <div className="App">
        <Header portal="Patient Portal" pageType="patient"></Header>
        <Intro name="Tony"></Intro>
        {doctorList.map((doctor) => (
          <DoctorList
            firstName={doctor.first_name}
            lastName={doctor.last_name}
            id={doctor.doctor_id}
          ></DoctorList>
        ))}
      </div>
    );
  } else {
    return <div>Loading</div>;
  }
};

export default PatientPage;
