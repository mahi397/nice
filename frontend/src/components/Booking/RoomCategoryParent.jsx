import React, { useState, useEffect } from "react";
import RoomCategorySection2 from "./RoomCategorySection2";
import { getRoomReserveURL } from "./booking_api";

const RoomCategoryParent = ({ rooms }) => {
  const [selectedCategories, setSelectedCategories] = useState({});

  const handleCategorySelect = (roomId, category) => {
    setSelectedCategories((prevCategories) => ({
      ...prevCategories,
      [roomId]: category,
    }));
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
    const url = getRoomReserveURL(tripid); 

    // Count the occurrences of each category
    const categoryCounts = Object.values(selectedCategories).reduce((acc, category) => {
        acc[category] = (acc[category] || 0) + 1;
        return acc;
      }, {});

    // Construct the roomSelections array
    const roomSelections = Object.entries(categoryCounts).map(([category, count]) => ({
        room_type: category,
        number_of_rooms: count,
      }));

    const data = {
      room_selections: roomSelections,
    };

    try {
      const response = await axios.patch(url, data, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      console.log('Room categories patch sent successfully:', response.data);
    } catch (error) {
      console.error('Error updating rooms:', error);
    }
  };


  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center"}}>
      <div style={styles.container}>
        {rooms.map((room) => (
          <RoomCategorySection2 key={room.id} room={room} onCategorySelect={handleCategorySelect} />
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

export default RoomCategoryParent;

const styles = {
  container: {
    width: "100%",
    display: "flex",
    // flexWrap: "wrap",
    gap: "25px",
    alignItems: "center",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    marginTop: "20px",
}};
