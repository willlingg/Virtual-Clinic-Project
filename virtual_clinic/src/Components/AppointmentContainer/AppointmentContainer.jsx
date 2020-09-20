import React, { useState, useEffect, useRef } from "react";
import "./AppointmentContainer.css";
import { post } from "axios";

const AppointmentContainer = (props) => {
  const [appointmentList, setAppointmentList] = useState(null);
  const [doctorList, setDoctorList] = useState(null);
  const [ApptLoaded, setApptLoaded] = useState(false);
  const [docLoaded, setDocLoaded] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [documents, setDocuments] = useState(null);
  const [documentLoaded, setDocumentLoaded] = useState(false);
  const [submitBUtton, setSubmitButton] = useState(false);

  const patient_id = props.patient_id;

  useEffect(() => {
    async function getAppointments() {
      let appointmentQuery = await fetch(`/appointment/patient/${patient_id}`);
      let appointments = await appointmentQuery.json();
      appointments.sort(
        (a, b) => new Date(a.diary_date) - new Date(b.diary_date)
      );
      setAppointmentList(appointments);
      setApptLoaded(true);
    }

    getAppointments();
  }, []);

  useEffect(() => {
    async function getDoctors() {
      try {
        let docResponse = await fetch("/doctors");
        let doctors = await docResponse.json();
        setDoctorList(doctors);
        setDocLoaded(true);
      } catch (err) {
        console.log(err);
      }
    }
    getDoctors();
  }, []);

  useEffect(() => {
    async function getUploadedFiles() {
      try {
        let response = await fetch(`/file/patient/${patient_id}`);
        let documents = await response.json();
        setDocuments(documents);
        console.log(documents);
        setDocumentLoaded(true);
      } catch (err) {
        console.log(err);
      }
    }
    getUploadedFiles();
  }, []);

  const getDoctorName = (doctor_id) => {
    for (var i = 0; i < doctorList.length; i++) {
      if (doctorList[i].doctor_id === doctor_id) {
        return (
          <h3>
            Dr. {doctorList[i].first_name} {doctorList[i].last_name}
          </h3>
        );
      }
    }
  };

  const getDate = (appointment) => {
    const dateArray = appointment.diary_date.split(" ");
    const date = dateArray.slice(1, 4);
    var day = dateArray[0];
    day = day.slice(0, 3);
    return <div>{day + " " + date.join("/")}</div>;
  };

  const getZoomUrl = (appointment) => {
    const zoomUrl = appointment.join_url;
    return (
      <a href={zoomUrl} target="_blank">
        Click here to begin your appointment
      </a>
    );
  };

  const deleteAppointment = (appointment_id) => {
    fetch("/appointment", {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },

      //make sure to serialize your JSON body
      body: JSON.stringify({
        patient_id: 1,
        diary_id: appointment_id,
      }),
    }).then((response) => {
      window.location.reload();
    });
  };

  const fileHandler = (e) => {
    setSelectedFiles(e.target.files[0]);
    setSubmitButton(true);
  };

  const uploadDocument = (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", selectedFiles);
    const url = `/file/patient/${patient_id}`;
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };
    post(url, formData, config).then((res) => {
      if (res.status === 201) {
        setSubmitButton(false);
        window.location.reload();
      }
    });
  };

  const deleteDocument = (doc_id) => {
    fetch(`/file/${doc_id}`, {
      method: "DELETE",
    }).then((response) => {
      window.location.reload();
    });
  };

  const downloadDocument = (doc_id) => {
    fetch(`/file/${doc_id}`).then((res) => window.open(res.url));
  };

  if (ApptLoaded && docLoaded && documentLoaded) {
    return (
      <div className="appointment-list">
        <div className="intro-container">
          <div className="patient-appointment-intro">
            <h2>Please read carefully</h2>
            <p>
              If you wish to upload any medical information or images such as
              X-rays or CAT scans, please do so by clicking the 'Upload Files'
              button and attaching the files you wish to provide the
              Practitioner. Ensure that your files are aptly named to represent
              what they are.
            </p>
            <p>
              When it is time for your appointment, please click on the link
              underneath 'Zoom URL' to begin your video consultation.
            </p>
          </div>
          <div className="appointment-box">
            <h2>Upload Files</h2>
            <form onSubmit={uploadDocument}>
              <input
                name="file"
                type="file"
                onChange={(e) => fileHandler(e)}
              ></input>
              {submitBUtton && <input type="submit" value="Submit" />}
            </form>
          </div>
          {documents.length > 0 && (
            <div className="doc-container">
              <h2>Your Uploaded Documents</h2>
              {documents.map((doc) => (
                <div className="file-list">
                  <div
                    id="doc-link"
                    onClick={() => downloadDocument(doc.document_id)}
                  >
                    {doc.file_name}
                  </div>
                  <button onClick={() => deleteDocument(doc.document_id)}>
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {appointmentList.map((appointment) => (
          <div className="appointment-container">
            <div className="calendar-container">
              <img className="calendar-pic" src="calendar.png"></img>
              <div className="appointment-box">
                <h2>{getDate(appointment)}</h2>
                <h3>
                  {appointment.time_from} - {appointment.time_to}
                </h3>
              </div>
            </div>
            <div className="appointment-box">
              <h2>Practitioner</h2>
              {getDoctorName(appointment.doctor_id)}
            </div>
            <div className="appointment-box">
              <h2>Zoom URL</h2>
              {getZoomUrl(appointment)}
            </div>
            <div className="appointment-box">
              <h2>Cancel appointment</h2>
              <button
                onClick={() => {
                  deleteAppointment(appointment.diary_id);
                }}
              >
                Cancel your appointment
              </button>
            </div>
          </div>
        ))}
      </div>
    );
  } else {
    return <></>;
  }
};

export default AppointmentContainer;
