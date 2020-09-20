import React, { useState } from "react";
import "./BookingContainer.css";
import TimeDropdown from "../TimeDropdown/TimeDropdown";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Link } from "react-router-dom";

const DropdownContainer = (props) => {
  const { doctor_id, doctor_name } = props;
  const [selectedDate, setSelectedDate] = useState(null);
  const [time, setTime] = useState(null);
  const [diaryId, setDiaryId] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  // Setting Date
  var today_date = new Date();
  var dateInAWeek = new Date();
  dateInAWeek.setDate(dateInAWeek.getDate() + 14);

  var formattedDate = getPatientDate(selectedDate);

  const handleTimeUpdate = (value) => {
    setTime(value);
  };

  function getPatientDate(date) {
    var d = new Date(date),
      month = "" + (d.getMonth() + 1),
      day = "" + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;
    return [day, month, year].join("/");
  }

  function formatDate(date) {
    var d = new Date(date),
      month = "" + (d.getMonth() + 1),
      day = "" + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2) month = "0" + month;
    if (day.length < 2) day = "0" + day;
    return [year, month, day].join("-");
  }

  const getDiaryId = () => {
    var formattedDate = formatDate(selectedDate);
    if (time) {
      fetch(`/diary/${doctor_id}/${formattedDate}`)
        .then((res) => res.json())
        .then((data) => {
          for (var i = 0; i < data.length; i++) {
            if (data[i].time_slot === time.value) {
              setDiaryId(data[i].diary_id);
            }
          }
        });
    }
  };

  const submitAppointment = () => {
    fetch("/appointment", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },

      //make sure to serialize your JSON body
      body: JSON.stringify({
        patient_id: 1,
        diary_id: diaryId,
      }),
    }).then((response) => {
      if (response.status === 201) {
        setSubmitted(true);
      }
    });
  };

  return (
    <div className="height-setter">
      <div className="time-select">
        <h3>Book an appointment with Dr. {doctor_name}</h3>
        <div className="date-selection">
          <h5>Please select the date of your appointment</h5>
          <DatePicker
            selected={selectedDate}
            onChange={(date) => {
              setSelectedDate(date);
            }}
            dateFormat="dd/MM/yyyy"
            minDate={today_date}
            maxDate={dateInAWeek}
          ></DatePicker>
          {selectedDate && (
            <>
              <>
                <h5>Please select a time</h5>
                <TimeDropdown
                  doctor_id={doctor_id}
                  selectedDate={formatDate(selectedDate)}
                  onChosenTime={handleTimeUpdate}
                  onChange={getDiaryId()}
                ></TimeDropdown>
              </>
              <button className="submit-button" onClick={submitAppointment}>
                Submit!
              </button>
            </>
          )}
          {submitted && (
            <>
              <div className="submit">
                Your appointment with <strong>Dr. {doctor_name}</strong> has
                been succesfully booked on <strong>{formattedDate}</strong> at{" "}
                <strong>{time.value}</strong>
              </div>
              <Link className="sub-link" to="/patient">
                Return to Patient Portal
              </Link>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default DropdownContainer;
