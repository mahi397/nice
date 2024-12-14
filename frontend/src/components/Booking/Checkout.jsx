import React, { useState } from "react";
import { Input, Button, Form, Steps, notification, DatePicker } from "antd";
import {
  CreditCardOutlined,
  UserOutlined,
  CheckCircleOutlined,
} from "@ant-design/icons";
import "./checkout.css";
import Header from "../Header";
import { Link } from "react-router-dom";

const { Step } = Steps;

const Checkout = () => {
  const [step, setStep] = useState(0); // 0 for Step 1, 1 for Step 2, 2 for Step 3
  const [passengerDetails, setPassengerDetails] = useState({
    firstname: "",
    lastname: "",
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
      <Header />
      <h2
        style={{
          fontFamily: "Bebas Neue",
          fontSize: "40px",
          marginTop: "20px",
          color: "rgb(16, 85, 154)",
        }}
      >
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
          <Step title="Checkout" icon={<CheckCircleOutlined />} />
        </Steps>

        <div className="step-content">
          {step === 0 && (
            <Form layout="vertical">
              <Form.Item
                label="First Name"
                rules={[
                  { required: true, message: "Please enter the first name" },
                ]}
              >
                <Input
                  value={passengerDetails.firstname}
                  onChange={handlePassengerDetailsChange}
                  name="firstname"
                />
              </Form.Item>
              <Form.Item
                label="Last Name"
                rules={[
                  { required: true, message: "Please enter the last name" },
                ]}
              >
                <Input
                  value={passengerDetails.lastname}
                  onChange={handlePassengerDetailsChange}
                  name="lastname"
                />
              </Form.Item>
              <Form.Item label="Email">
                <Input
                  value={passengerDetails.email}
                  onChange={handlePassengerDetailsChange}
                  name="email"
                />
              </Form.Item>
              <Form.Item
                label="Contact Number"
                rules={[
                  {
                    required: true,
                    message: "Please enter the contact number",
                  },
                ]}
              >
                <Input
                  type="tel"
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
              <Form.Item label="Card Number" rules={[
                  {
                    required: true,
                    message: "Please enter your card number",
                  },
                ]}>
                <Input
                  placeholder="Enter Card Number"
                  value={paymentDetails.cardNumber}
                  onChange={handlePaymentDetailsChange}
                  name="cardNumber"
                  maxLength={16}
                />
              </Form.Item>
              <Form.Item label="CVV" rules={[
                  {
                    required: true,
                    message: "Please enter your CVV",
                  },
                ]}>
                <Input
                  placeholder="Enter CVV"
                  value={paymentDetails.cvv}
                  onChange={handlePaymentDetailsChange}
                  name="cvv"
                  maxLength={3}
                  type="password"
                />
              </Form.Item>
              <Form.Item label="Expiration Date (MM/YY)" rules={[
                  {
                    required: true,
                    message: "Please enter the card expiry date",
                  },
                ]}>
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
                <h3 style={{ fontFamily: "Bebas Neue", fontSize: "25px" }}>
                  Passenger Details
                </h3>
                <p>First Name: {passengerDetails.firstname}</p>
                <p>Last Name: {passengerDetails.lastname}</p>
                <p>Email: {passengerDetails.email}</p>
                <p>Phone: {passengerDetails.phone}</p>
              </div>
              <div>
                <h3 style={{ fontFamily: "Bebas Neue", fontSize: "25px" }}>
                  Payment Details
                </h3>
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
                  // onClick={handleSubmit}
                  style={{ marginLeft: "10px" }}
                >
                  <Link to="/bookingsummary">Confirm Payment</Link>
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
