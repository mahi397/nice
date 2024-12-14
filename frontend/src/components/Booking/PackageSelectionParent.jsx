import React, { useState, useEffect } from "react";
import PackageSelection2 from "./PackageSelection2";
import { getAddPassengerURL, getAddPkgURL } from "./booking_api";
import axios from 'axios';
import {Link} from "react-router-dom";

const PackageSelectionParent = ({ rooms, guests }) => {
    const passengerDetails = {
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
      
  const [selectedPackages, setSelectedPackages] = useState({});
  const [totalGuests, setTotalGuests] = useState(2); // Example number of guests
  //  const [totalGuests, setTotalGuests] = useState(Array.from({ length: guests }, (_, index) => index + 1));

    // useEffect(() => {
    //     const totalGuests = rooms.reduce((total, room) => total + room.guests, 0);
    //     setTotalGuests(Array.from({ length: totalGuests }, (_, index) => index + 1));
    // }, []);

  const handlePackageSelect = (guestIndex, packageId, packageName) => {
    setSelectedPackages((prevPackages) => {
      const updatedPackages = { ...prevPackages };
      if (!updatedPackages[packageId]) {
        updatedPackages[packageId] = { packageName, quantity: 0 };
      }
      updatedPackages[packageId].quantity += 1;
      return updatedPackages;
    });
  };

  const handleConfirm = async () => {
    const token = localStorage.getItem('token'); 
    const storedBookingData = sessionStorage.getItem('bookingData');
    if (!storedBookingData) {
      console.error('No booking data available in session');
      return;
    }

    const bookingData = JSON.parse(storedBookingData);
    const tripid = bookingData.trip_details.tripid;
    const url = getAddPkgURL(tripid); 
    const passURL = getAddPassengerURL(tripid);
    const packages = Object.entries(selectedPackages).map(([packageId, { packageName, quantity }]) => ({
      packageid: parseInt(packageId),
      packagename: packageName,
      quantity,
    }));

    const data = { packages };

    const dataToPost = {
        packages: [
            {
                packageid: 4,
                packagename: "Water and Non-Alcoholic",
                quantity: 2
            },
            {
                packageid: 5,
                packagename: "Unlimited Bar",
                quantity: 1
            },
            {
                packageid: 6,
                packagename: "Internet 200 minutes, 100 GB",
                quantity: 1
            },
            {
                packageid: 7,
                packagename: "Unlimited Internet",
                quantity: 1
            },
            {
                packageid: 8,
                packagename: "Specialty Dining",
                quantity: 1
            }
        ]
    }

    try {
        const passresponse = await axios.post(passURL, passengerDetails, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            });
        console.log('Passengers post sent successfully:', passresponse.data);
    } catch (error) {
        console.error('Error adding passengers:', error);
    }

    try {
      const response = await axios.post(url, dataToPost, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      console.log('Packages post sent successfully:', response.data);
    } catch (error) {
      console.error('Error adding pkgs:', error);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
      <div style={styles.container}>
        {Array.from({ length: totalGuests }).map((guest, index) => (
          <PackageSelection2 key={index} guestIndex={index} onPackageSelect={handlePackageSelect} />
        ))}
      </div>
      <div style={styles.buttonContainer}>
        <button onClick={handleConfirm}>
        <Link to={"/reviewbooking"}>CONTINUE</Link>
        </button>
      </div>
    </div>
  );
};

export default PackageSelectionParent;

const styles = {
  container: {
    width: "100%",
    display: "flex",
    gap: "25px",
    alignItems: "center",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    marginTop: "20px",
  },
};
