import React, { useState } from "react";
import { Input, Button, Form, Steps, notification, DatePicker } from "antd";
import {
  CreditCardOutlined,
  UserOutlined,
  CheckCircleOutlined,
} from "@ant-design/icons";
import "./checkout.css";

const { Step } = Steps;

const Checkout = () => {
  const [step, setStep] = useState(0); // 0 for Step 1, 1 for Step 2, 2 for Step 3
  const [passengerDetails, setPassengerDetails] = useState({
    firstName: "",
    lastName: "",
    dob: "",
    gender: "",
    email: "",
    phone: "",
  });
  const [paymentDetails, setPaymentDetails] = useState({
    cardNumber: "",
    cvv: "",
    expirationDate: "",
  });

  const handleNextStep = () => {
    if (
      step === 0 &&
      Object.values(passengerDetails).some((value) => value === "")
    ) {
      notification.error({ message: "Please fill in all passenger details." });
      return;
    }
    if (
      step === 1 &&
      Object.values(paymentDetails).some((value) => value === "")
    ) {
      notification.error({ message: "Please fill in all payment details." });
      return;
    }
    setStep(step + 1);
  };

  const handlePrevStep = () => {
    setStep(step - 1);
  };

  const handlePassengerDetailsChange = (e) => {
    setPassengerDetails({
      ...passengerDetails,
      [e.target.name]: e.target.value,
    });
  };

  const handlePaymentDetailsChange = (e) => {
    setPaymentDetails({
      ...paymentDetails,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = () => {
    notification.success({ message: "Booking confirmed!" });
  };

  return (
    <div className="checkout">
      <h2 style={{ fontFamily: "Bebas Neue", fontSize: "40px" }}>
        Review and Pay
      </h2>

      <div className="checkout-container">
        <Steps
          current={step}
          onChange={setStep}
          size="small"
          style={{ marginBottom: 40 }}
        >
          <Step title="Passenger Details" icon={<UserOutlined />} />
          <Step title="Payment Details" icon={<CreditCardOutlined />} />
          <Step title="Review & Pay" icon={<CheckCircleOutlined />} />
        </Steps>

        <div className="step-content">
          {step === 0 && (
            <Form layout="vertical">
              <Form.Item label="First Name">
                <Input
                  placeholder="Enter First Name"
                  value={passengerDetails.firstName}
                  onChange={handlePassengerDetailsChange}
                  name="firstName"
                />
              </Form.Item>
              <Form.Item label="Last Name">
                <Input
                  placeholder="Enter Last Name"
                  value={passengerDetails.lastName}
                  onChange={handlePassengerDetailsChange}
                  name="lastName"
                />
              </Form.Item>
              <Form.Item label="Date of Birth">
                <Input
                  placeholder="Enter Date of Birth"
                  value={passengerDetails.dob}
                  onChange={handlePassengerDetailsChange}
                  name="dob"
                />
              </Form.Item>
              <Form.Item label="Gender">
                <Input
                  placeholder="Enter Gender"
                  value={passengerDetails.gender}
                  onChange={handlePassengerDetailsChange}
                  name="gender"
                />
              </Form.Item>
              <Form.Item label="Email">
                <Input
                  placeholder="Enter Email"
                  value={passengerDetails.email}
                  onChange={handlePassengerDetailsChange}
                  name="email"
                />
              </Form.Item>
              <Form.Item label="Phone">
                <Input
                  placeholder="Enter Phone Number"
                  value={passengerDetails.phone}
                  onChange={handlePassengerDetailsChange}
                  name="phone"
                />
              </Form.Item>
              <Button
                type="primary"
                onClick={handleNextStep}
                style={{ width: "100%" }}
              >
                Next
              </Button>
            </Form>
          )}

          {step === 1 && (
            <Form layout="vertical">
              <Form.Item label="Card Number">
                <Input
                  placeholder="Enter Card Number"
                  value={paymentDetails.cardNumber}
                  onChange={handlePaymentDetailsChange}
                  name="cardNumber"
                  maxLength={16}
                />
              </Form.Item>
              <Form.Item label="CVV">
                <Input
                  placeholder="Enter CVV"
                  value={paymentDetails.cvv}
                  onChange={handlePaymentDetailsChange}
                  name="cvv"
                  maxLength={3}
                  type="password"
                />
              </Form.Item>
              <Form.Item label="Expiration Date (MM/YY)">
                <Input
                  placeholder="Enter Expiry Date"
                  value={paymentDetails.expirationDate}
                  onChange={handlePaymentDetailsChange}
                  name="expirationDate"
                  maxLength={5}
                />
              </Form.Item>
              <div className="buttons">
                <Button onClick={handlePrevStep} style={{ width: "48%" }}>
                  Back
                </Button>
                <Button
                  type="primary"
                  onClick={handleNextStep}
                  style={{ width: "48%" }}
                >
                  Next
                </Button>
              </div>
            </Form>
          )}

          {step === 2 && (
            <div className="review-section">
              <div>
                <h3 style={{fontFamily: 'Bebas Neue', fontSize: '25px'}}>Passenger Details</h3>
                <p>First Name: {passengerDetails.firstName}</p>
                <p>Last Name: {passengerDetails.lastName}</p>
                <p>Date of Birth: {passengerDetails.dob}</p>
                <p>Gender: {passengerDetails.gender}</p>
                <p>Email: {passengerDetails.email}</p>
                <p>Phone: {passengerDetails.phone}</p>
              </div>
              <div>
                <h3 style={{fontFamily: 'Bebas Neue', fontSize: '25px'}}>Payment Details</h3>
                <p>
                  Card Number: XXXX XXXX XXXX{" "}
                  {paymentDetails.cardNumber.slice(-4)}
                </p>
                {/* <p>CVV: XXX</p> */}
                <p>Expiration Date: {paymentDetails.expirationDate}</p>
              </div>
              <div className="buttons">
                <Button onClick={handlePrevStep} style={{ width: "48%" }}>
                  Back
                </Button>
                <Button
                  type="primary"
                  onClick={handleSubmit}
                  style={{ width: "48%" }}
                >
                  Book Now
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Checkout;
