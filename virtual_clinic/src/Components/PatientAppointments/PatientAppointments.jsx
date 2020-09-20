import React, { useState, useEffect } from "react";
import Modal from "react-modal";
import "./PatientAppointments.css";

const PatientAppointments = (props) => {
  const [appointmentList, setAppointmentList] = useState(null);
  const [ApptLoaded, setApptLoaded] = useState(false);
  const [modalIsOpen, setmodalIsOpen] = useState(false);
  const [modalPatientId, setModalPatientId] = useState(null);
  const [modalPatientName, setModalPatientName] = useState(null);
  const [documents, setDocuments] = useState(null);
  const [documentLoaded, setDocumentLoaded] = useState(false);

  const doctor_id = props.doctor_id;

  useEffect(() => {
    async function getAppointments() {
      let appointmentQuery = await fetch(`/appointment/doctor/${doctor_id}`);
      let appointments = await appointmentQuery.json();
      appointments.sort(
        (a, b) => new Date(a.diary_date) - new Date(b.diary_date)
      );
      setAppointmentList(appointments);
      setApptLoaded(true);
    }

    getAppointments();
  }, []);

  const getPatientName = (appointment) => {
    return (
      <h3>
        {appointment.first_name} {appointment.middle_name}{" "}
        {appointment.last_name}
      </h3>
    );
  };

  const getDate = (appointment) => {
    const dateArray = appointment.diary_date.split(" ");
    const date = dateArray.slice(1, 4);
    var day = dateArray[0];
    day = day.slice(0, 3);
    return <div>{day + " " + date.join("/")}</div>;
  };

  const getZoomUrl = (appointment) => {
    const zoomUrl = appointment.start_url;
    return (
      <a href={zoomUrl} target="_blank">
        Click here to begin your consult
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

  async function getUploadedFiles(pat_id) {
    try {
      let response = await fetch(`/file/patient/${pat_id}`);
      let documents = await response.json();
      setDocuments(documents);
      console.log(documents);
      setDocumentLoaded(true);
    } catch (err) {
      console.log(err);
    }
  }

  const downloadDocument = (doc_id) => {
    fetch(`/file/${doc_id}`).then((res) => window.open(res.url));
  };

  if (ApptLoaded) {
    return (
      <div className="appointment-list">
        {documentLoaded && (
          <Modal
            isOpen={modalIsOpen}
            onRequestClose={() => setmodalIsOpen(false)}
            style={{
              overlay: {
                backgroundColor: "rgba(255, 255, 255, 0.75)",
              },
              content: {
                width: "40%",
                margin: "0 auto",
              },
            }}
          >
            <h2>Files for {modalPatientName}</h2>
            <div className="doc-container">
              {documents.map((doc) => (
                <div className="file-list-doc">
                  <div
                    id="doc-link"
                    onClick={() => downloadDocument(doc.document_id)}
                  >
                    {doc.file_name}
                  </div>
                </div>
              ))}
            </div>
            <div>
              <button onClick={() => setmodalIsOpen(false)}>Close</button>
            </div>
          </Modal>
        )}

        <div className="patient-appointment-intro">
          <h2>Please read carefully</h2>
          <p>
            If you wish to download any medical information or images uploaded
            by your patient such as X-rays or CAT scans, please do so by
            clicking the file name under the 'Uploaded Files' column.
          </p>
          <p>
            When it is time for your appointment, please click on the link
            underneath 'Zoom URL' to begin hosting your video appointment.
          </p>
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
              <h2>Patient</h2>
              {getPatientName(appointment)}
            </div>
            <div className="appointment-box">
              <h2>Uploaded Files</h2>
              <button
                onClick={() => {
                  setmodalIsOpen(true);
                  setModalPatientId(appointment.patient_id);
                  setModalPatientName(
                    appointment.first_name + " " + appointment.last_name
                  );
                  getUploadedFiles(appointment.patient_id);
                }}
              >
                Click here for patient files
              </button>
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
                  //   forceUpdate();
                }}
              >
                Cancel the appointment
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

export default PatientAppointments;
