import React from "react";
import "./DoctorIntro.css";

const DoctorIntro = () => (
  <div className="intro-body">
    <img className="img-container" src="med_centre.png"></img>
    <div className="description">
      <h1>Welcome to the Doctor Portal</h1>
      <h4>High St Kensington, NSW 2052 Australia</h4>
      <p>
        As a Practitioner, you are able to block out appointment times in your
        diary, allowing you to easily stay on top of your busy schedule.
      </p>
      <br></br>
      <p>
        Our service provides a complete virtual telehealth experience, allowing
        you to complete consultations over Zoom. The platform also allows the
        upload of large data files so you can view the image of your patients'
        CAT-scan or X-ray in very high quality.
      </p>
      <br></br>
    </div>
  </div>
);

export default DoctorIntro;
