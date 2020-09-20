import React, { useEffect } from "react";
import { useState } from "react";
import { Dropdown } from "semantic-ui-react";

const TimeDropdown = (props) => {
  const [time, setTime] = useState(null);
  const [timeSlots, setTimeSlots] = useState(null);

  useEffect(() => {
    fetch(`/diary/${props.doctor_id}/${props.selectedDate}`)
      .then((res) => res.json())
      .then((data) => {
        data.sort((b, a) => b.time_slot_id - a.time_slot_id);
        // Need to check if available
        const timeSlots = data.map((diary) => {
          if (diary.available === "Y") {
            return diary.time_slot;
          }
          return undefined;
        });
        var filteredDiary = timeSlots.filter(function (el) {
          return el !== undefined;
        });
        setTimeSlots(filteredDiary);
      });
  }, []);

  const options = [];

  if (timeSlots) {
    timeSlots.forEach((timeslot, index) => {
      return (options[index] = {
        key: index,
        text: timeslot,
        value: timeslot,
      });
    });
  }

  const handleChange = (_e, { value }) => {
    setTime({ value });
    props.onChosenTime({ value });
  };

  return (
    <div className="time-select">
      <Dropdown
        placeholder="Select choice"
        options={options}
        onChange={handleChange}
        selection
        scrolling
        clearable
      />
    </div>
  );
};

export default TimeDropdown;
