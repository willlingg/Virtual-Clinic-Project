import React from "react";
import "../../App.css";
import Header from "../../Components/Header/Header";
import DoctorIntro from "../../Components/DoctorIntro/DoctorIntro";

const DoctorPage = () => {
  return (
    <div className="App">
      <Header portal="Doctor Portal" pageType="doctor"></Header>
      <DoctorIntro></DoctorIntro>
      {/* <DoctorBlock></DoctorBlock> */}
    </div>
  );
};

export default DoctorPage;
