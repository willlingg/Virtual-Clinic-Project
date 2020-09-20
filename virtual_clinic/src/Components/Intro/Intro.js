import React from "react";
import "./Intro.css";

const Intro = (props) => (
  <div className="intro-body">
    <img className="img-container" src="med_centre.png"></img>
    <div className="description">
      <h1>Welcome to the Virtual Clinic, {props.name}</h1>
      <h3>UNSW Sydney</h3>
      <h4>High St Kensington, NSW 2052 Australia</h4>
      <p>
        During lockdown, many medical practices have been unable to provide the
        services their patients need, because patients, who are
        disproportionately comprised of the elderly, are particularly fearful of
        going to places of care over concerns of the virus.
      </p>
      <br></br>
      <p>
        Our service provides a complete virtual telehealth experience, from
        booking an appointment with your General Practitioner and having your
        consultation over Zoom. The platform also allows the upload of large
        data files so your doctor can view the image of your CAT-scan or X-ray
        in very high quality.
      </p>
      <br></br>
      <p>Please choose a Practitioner below to book an appointment</p>
    </div>
  </div>
);

export default Intro;
