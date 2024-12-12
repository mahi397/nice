import React, { useState } from "react";
import TopSection from "./TopSection";
import HeaderLoggedIn from "../HeaderLoggedIn";
import RoomSummaryBar from "./RoomSummaryBar";
import AddRoomSection from "./AddRoomSection";
import RoomCategorySection from "./RoomCategorySection";
import PackageSelection from "./PackageSelection";
import Header from "../Header";

const Booking = () => {
  const [currentStep, setCurrentStep] = useState(0); // Current step in the flow
  const [rooms, setRooms] = useState([{ id: 1, guests: 2 }]); // State to track rooms and guests for each room

  const components = [
    <AddRoomSection
      onContinue={() => setCurrentStep(currentStep + 1)}
      rooms={rooms}
      setRooms={setRooms}
    />,
    <RoomCategorySection onContinue={() => setCurrentStep(currentStep + 1)} />,
    <PackageSelection />,
  ];

  return (
    <div>
      <Header />
      <div className="room-list-container">
        <RoomSummaryBar rooms={rooms} />

        {components[currentStep]}
      </div>
    </div>
  );
};

export default Booking;
