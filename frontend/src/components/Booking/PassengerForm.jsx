import React, { useState } from "react";
import {
  Form,
  Input,
  Button,
  Row,
  Col,
  notification,
  Steps,
  Select,
  DatePicker,
} from "antd";
import axios from "axios";
import moment from "moment";
import { getAddPassengerURL } from "./booking_api";

const { Step } = Steps;
const { Option } = Select;

const PassengerForm = () => {
  const dataToPost = {
    passengers: [
      {
        firstname: "John",
        lastname: "Doe",
        dateofbirth: "1990-05-15",
        gender: "M",
        contactnumber: "1234567890",
        emailaddress: "johndoe@example.com",
        streetaddr: "123 Main St",
        city: "Miami",
        state: "FL",
        country: "USA",
        zipcode: "33101",
        nationality: "American",
        passportnumber: "A12345678",
        emergencycontactname: "Jane Doe",
        emergencycontactnumber: "+1999999999",
      },
      {
        firstname: "Alice",
        lastname: "Smith",
        dateofbirth: "1995-10-10",
        gender: "F",
        contactnumber: "2345678901",
        emailaddress: "alicesmith@example.com",
        streetaddr: "456 Oak St",
        city: "Orlando",
        state: "FL",
        country: "USA",
        zipcode: "32801",
        nationality: "American",
        passportnumber: "B87654321",
        emergencycontactname: "Bob Smith",
        emergencycontactnumber: "1234567890",
      },
    ],
  };
  
  const [form] = Form.useForm();
  const [step, setStep] = useState(0);
  const [passengerDetails, setPassengerDetails] = useState(dataToPost.passengers);
  // const [passengerDetails, setPassengerDetails] = useState([
    // {
    //   firstname: "",
    //   lastname: "",
    //   dateofbirth: "",
    //   gender: "",
    //   contactnumber: "",
    //   emailaddress: "",
    //   streetaddr: "",
    //   city: "",
    //   state: "",
    //   country: "",
    //   zipcode: "",
    //   nationality: "",
    //   passportnumber: "",
    //   emergencycontactname: "",
    //   emergencycontactnumber: "",
    // },
    // {
    //   firstname: "",
    //   lastname: "",
    //   dateofbirth: "",
    //   gender: "",
    //   contactnumber: "",
    //   emailaddress: "",
    //   streetaddr: "",
    //   city: "",
    //   state: "",
    //   country: "",
    //   zipcode: "",
    //   nationality: "",
    //   passportnumber: "",
    //   emergencycontactname: "",
    //   emergencycontactnumber: "",
    // },
    // {
    //   firstname: "",
    //   lastname: "",
    //   dateofbirth: "",
    //   gender: "",
    //   contactnumber: "",
    //   emailaddress: "",
    //   streetaddr: "",
    //   city: "",
    //   state: "",
    //   country: "",
    //   zipcode: "",
    //   nationality: "",
    //   passportnumber: "",
    //   emergencycontactname: "",
    //   emergencycontactnumber: "",
    // },
  // ]);

  const handleInputChange = (index, field, value) => {
    const updatedDetails = [...passengerDetails];
    updatedDetails[index][field] = value;
    setPassengerDetails(updatedDetails);
  };

  const handleNextStep = () => {
    form
      .validateFields()
      .then(() => {
        setStep(step + 1);
      })
      .catch((errorInfo) => {
        notification.error({
          message: "Please fill in all passenger details.",
        });
      });
  };

  const handlePreviousStep = () => {
    setStep(step - 1);
  };

  
  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem("token");
      const storedBookingData = sessionStorage.getItem("bookingData");
      if (!storedBookingData) {
        console.error("No booking data available in session");
        return;
      }

      const bookingData = JSON.parse(storedBookingData);
      const tripid = bookingData.trip_details.tripid;
      const url = getAddPassengerURL(tripid);
      const data = {
        passengers: passengerDetails,
      };

      const response = await axios.post(url, dataToPost, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      console.log("Passenger Details to be submitted:", data);
      console.log("Passenger Details submitted successfully:", response.data);
      notification.success({
        message: "Passenger details submitted successfully!",
      });
    } catch (error) {
      console.error("Error submitting passenger details:", error);
      notification.error({ message: "Error submitting passenger details." });
    }
  };

  const formStyles = {
    width: "800px", // Set the maximum width of the form
    margin: "0 auto", // Center the form horizontally
    padding: "20px", // Add padding around the form
    border: "1px solid #ccc", // Add a border around the form
    borderRadius: "8px", // Add rounded corners to the form
    backgroundColor: "#fff", // Set the background color of the form
  };

  return (
    <div style={formStyles}>
      <Form form={form} 
      layout="vertical" 
      onFinish={handleSubmit}
      >
        <Steps current={step}>
          <Step title="Guest 1" />
          <Step title="Guest 2" />
          {/* <Step title="Guest 3" /> */}
        </Steps>
        {/* <h2 style={{ marginTop: "20px" }}>Fill in Guest {step + 1} details</h2> */}
        <br />
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="First Name"
              name={`firstname`}
              rules={[
                { required: true, message: "Please enter the first name" },
              ]}
            >
              {/* {console.log("dataToPost", dataToPost.passengers[step])}
              {console.log("passengerDetails", passengerDetails[step])} */}
              
              <Input
                value={passengerDetails[step]?.firstname}
                onChange={(e) =>
                  handleInputChange(step, "firstname", e.target.value)
                }
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Last Name"
              name={`lastname`}
              rules={[
                { required: true, message: "Please enter the last name" },
              ]}
            >
              <Input
                value={passengerDetails[step]?.lastname}
                onChange={(e) =>
                  handleInputChange(step, "lastname", e.target.value)
                }
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Date of Birth"
              name={`dateofbirth_${step}`}
              rules={[
                { required: true, message: "Please enter the date of birth" },
              ]}
            >
              <DatePicker
                value={
                  passengerDetails[step]?.dateofbirth
                    ? moment(passengerDetails[step]?.dateofbirth)
                    : null
                }
                onChange={(date, dateString) =>
                  handleInputChange(step, "dateofbirth", dateString)
                }
                format="YYYY-MM-DD"
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Gender"
              name={`gender_${step}`}
              rules={[{ required: true, message: "Please select the gender" }]}
            >
              <Select
                value={passengerDetails[step]?.gender}
                onChange={(value) => handleInputChange(step, "gender", value)}
              >
                <Option value="M">Male</Option>
                <Option value="F">Female</Option>
                <Option value="Other">Other</Option>
                
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Contact Number"
              name={`contactnumber_${step}`}
              rules={[
                { required: true, message: "Please enter the contact number" },
              ]}
            >
              <Input
                type="tel"
                value={passengerDetails[step]?.contactnumber}
                onChange={(e) =>
                  handleInputChange(step, "contactnumber", e.target.value)
                }
                maxLength={10}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Email Address"
              name={`emailaddress_${step}`}
              rules={[
                { required: true, message: "Please enter the email address" },
              ]}
            >
              <Input
                type="email"
                value={passengerDetails[step]?.emailaddress}
                onChange={(e) =>
                  handleInputChange(step, "emailaddress", e.target.value)
                }
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Street Address"
              name={`streetaddr_${step}`}
              rules={[
                { required: true, message: "Please enter the street address" },
              ]}
            >
              <Input
                value={passengerDetails[step]?.streetaddr}
                onChange={(e) =>
                  handleInputChange(step, "streetaddr", e.target.value)
                }
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="City"
              name={`city_${step}`}
              rules={[{ required: true, message: "Please enter the city" }]}
            >
              <Input
                value={passengerDetails[step]?.city}
                onChange={(e) =>
                  handleInputChange(step, "city", e.target.value)
                }
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="State"
              name={`state_${step}`}
              rules={[{ required: true, message: "Please enter the state" }]}
            >
              <Input
                value={passengerDetails[step]?.state}
                onChange={(e) =>
                  handleInputChange(step, "state", e.target.value)
                }
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Country"
              name={`country_${step}`}
              rules={[{ required: true, message: "Please enter the country" }]}
            >
              <Input
                value={passengerDetails[step]?.country}
                onChange={(e) =>
                  handleInputChange(step, "country", e.target.value)
                }
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Zip Code"
              name={`zipcode_${step}`}
              rules={[{ required: true, message: "Please enter the zip code" }]}
            >
              <Input
                value={passengerDetails[step]?.zipcode}
                onChange={(e) =>
                  handleInputChange(step, "zipcode", e.target.value)
                }
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Nationality"
              name={`nationality_${step}`}
              rules={[
                { required: true, message: "Please enter the nationality" },
              ]}
            >
              <Input
                value={passengerDetails[step]?.nationality}
                onChange={(e) =>
                  handleInputChange(step, "nationality", e.target.value)
                }
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Passport Number"
              name={`passportnumber_${step}`}
              rules={[
                { required: true, message: "Please enter the passport number" },
              ]}
            >
              <Input
                value={passengerDetails[step]?.passportnumber}
                onChange={(e) =>
                  handleInputChange(step, "passportnumber", e.target.value)
                }
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              label="Emergency Contact Name"
              name={`emergencycontactname_${step}`}
              rules={[
                {
                  required: true,
                  message: "Please enter the emergency contact name",
                },
              ]}
            >
              <Input
                value={passengerDetails[step]?.emergencycontactname}
                onChange={(e) =>
                  handleInputChange(
                    step,
                    "emergencycontactname",
                    e.target.value
                  )
                }
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              label="Emergency Contact Number"
              name={`emergencycontactnumber_${step}`}
              rules={[
                {
                  required: true,
                  message: "Please enter the emergency contact number",
                },
              ]}
            >
              <Input
                type="tel"
                value={passengerDetails[step]?.emergencycontactnumber}
                onChange={(e) =>
                  handleInputChange(
                    step,
                    "emergencycontactnumber",
                    e.target.value
                  )
                }
                maxLength={10}
              />
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            {step > 0 && <Button onClick={handlePreviousStep}>Previous</Button>}
            {step < 1 ? (
              <Button type="primary" onClick={handleNextStep}>
                Next
              </Button>
            ) : (
              <Button type="primary" htmlType="submit">
                Submit
              </Button>
            )}
          </div>
        </Form.Item>
      </Form>
    </div>
  );
};

export default PassengerForm;
