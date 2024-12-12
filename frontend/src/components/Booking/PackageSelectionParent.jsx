import React, { useState, useEffect } from "react";
import PackageSelection2 from "./PackageSelection2";
import { getAddPkgURL } from "./booking_api";
import axios from 'axios';

const PackageSelectionParent = ({ rooms, totalGuests }) => {
  const [selectedPackages, setSelectedPackages] = useState({});
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
    
    const packages = Object.entries(selectedPackages).map(([packageId, { packageName, quantity }]) => ({
      packageid: parseInt(packageId),
      packagename: packageName,
      quantity,
    }));

    const data = { packages };

    try {
      const response = await axios.post(url, data, {
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
        {totalGuests.map((guest, index) => (
          <PackageSelection2 key={index} guestIndex={index} onPackageSelect={handlePackageSelect} />
        ))}
      </div>
      <div style={styles.buttonContainer}>
        <button onClick={handleConfirm}>
          CONFIRM
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
