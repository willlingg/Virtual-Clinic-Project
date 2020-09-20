import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

//Pages
import DoctorPage from "./pages/DoctorPage/doctor";
import PatientPage from "./pages/PatientPage/patient";
import LandingPage from "./pages/LandingPage/LandingPage";
import AppointmentPage from "./pages/AppointmentPage/Appointment";
import patientAppointments from "./pages/Appointments/Appointment";
import doctorAppointments from "./pages/DoctorAppointments/DoctorAppointments";

class App extends React.Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/" component={LandingPage} />
          <Route exact path="/patient" component={PatientPage} />
          <Route exact path="/doctor" component={DoctorPage} />
          <Route exact path="/appointment" component={AppointmentPage} />
          <Route
            exact
            path="/patientAppointments"
            component={patientAppointments}
          />
          <Route
            exact
            path="/doctorAppointments"
            component={doctorAppointments}
          />
        </Switch>
      </Router>
    );
  }
}

export default App;
