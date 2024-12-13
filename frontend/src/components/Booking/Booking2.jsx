import React, { useState } from "react";
import { Steps, Button } from "antd";
// import 'antd/dist/antd.css';
import AddRoomSection2 from "./AddRoomSection2";
import RoomCategorySection2 from "./RoomCategorySection2";
import PackageSelection2 from "./PackageSelection2";
import HeaderLoggedIn from "../HeaderLoggedIn";
import RoomSummaryBar from "./RoomSummaryBar";
import "./booking2.css";
import Header from "../Header";
import RoomCategoryParent from "./RoomCategoryParent";
import PackageSelectionParent from "./PackageSelectionParent";

const { Step } = Steps;

const Booking = () => {
  // State to track the current step
  const [currentStep, setCurrentStep] = useState(0);
  const [rooms, setRooms] = useState([{ id: 1, guests: 1 }]); // State to track rooms and guests for each room
  const [guests, setGuests] = useState(1);
  
  const StepOne = () => <AddRoomSection2 rooms={rooms} setRooms={setRooms} />;
  // const StepTwo = () => <RoomCategorySection2 />;
  const StepTwo = () => <RoomCategoryParent rooms={rooms} />;
  // const StepThree = () => <PackageSelection2 />;
  const StepThree = () => <PackageSelectionParent rooms={rooms} guests={guests} />;

  // Components for each step
  const stepComponents = [<StepOne />, <StepTwo />, <StepThree />];

  const nextStep = () => {
    if (currentStep < stepComponents.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="booking-container">
      {/* Top Navigation */}
      <Header />

      {/* Summary Bar */}
      <RoomSummaryBar rooms={rooms} />

      {/* Ant Design Steps */}
      <div className="step-container">
        <Steps current={currentStep}>
          <Step title="Add Rooms" description="Choose your rooms." />
          <Step
            title="Select Room Category"
            description="Choose the room type."
          />
          <Step title="Select Packages" description="Choose package add-ons." />
        </Steps>

        {/* Current Step Component */}
        <div className="step-content" style={{ margin: "20px 0" }}>
          {stepComponents[currentStep]}
        </div>

        {/* Navigation Buttons */}
        <div className="step-navigation">
          <Button
            onClick={prevStep}
            disabled={currentStep === 0}
            style={{ marginRight: "10px" }}
          >
            Previous
          </Button>
          <Button
            type="primary"
            onClick={nextStep}
            disabled={currentStep === stepComponents.length - 1}
          >
            {currentStep === stepComponents.length - 1 ? "Finish" : "Next"}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Booking;
