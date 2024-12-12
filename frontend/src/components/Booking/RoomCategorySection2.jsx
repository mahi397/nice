import React, { useEffect, useState } from "react";
import RoomCategoryCard from "./RoomCategoryCard";
import { getRoomReserveURL } from "./booking_api";
import axios from "axios";

export default function RoomCategorySection({ room, onCategorySelect }) {
  const [selectedCardId, setSelectedCardId] = useState(null);
  const [bookingData, setBookingData] = useState(null);
  const [availableCategories, setAvailableCategories] = useState([]);

  // Set the selected card
  const handleSelectCard = (id, category) => {
    setSelectedCardId(id);
    onCategorySelect(room.id, category);
  };

  useEffect(() => {
    // Retrieve bookingData from sessionStorage
    const storedBookingData = sessionStorage.getItem("bookingData");
    if (storedBookingData) {
      const parsedBookingData = JSON.parse(storedBookingData);
      setBookingData(parsedBookingData);
      setAvailableCategories(parsedBookingData.available_room_categories);
    }
    // console.log(storedBookingData);
  }, []);

  const categories = [
    {
      id: 1,
      type: "The Haven Suite",
      size: 1000,
      beds: 6,
      baths: 3,
      balconies: 2,
    },
    {
      id: 2,
      type: "Club Balcony Suite",
      size: 800,
      beds: 4,
      baths: 2,
      balconies: 2,
    },
    {
      id: 3,
      type: "Family Large Balcony",
      size: 600,
      beds: 4,
      baths: 2,
      balconies: 1,
    },
    {
      id: 4,
      type: "Family Balcony",
      size: 400,
      beds: 4,
      baths: 1.5,
      balconies: 1,
    },
    // {
    //   id: 5,
    //   type: "Oceanview window",
    //   size: 300,
    //   beds: 2,
    //   baths: 1,
    //   balconies: 0,
    // },
    // {
    //   id: 6,
    //   type: "Inside stateroom",
    //   size: 200,
    //   beds: 2,
    //   baths: 1,
    //   balconies: 0,
    // },
    // {
    //   id: 7,
    //   type: "Studio stateroom",
    //   size: 150,
    //   beds: 1,
    //   baths: 1,
    //   balconies: 0,
    // },
  ];

  return (
    <div style={styles.container}>
      <h2>Select Category for Room {room.id}</h2>
      {availableCategories.map((category, idx) => (
        <div
          key={idx}
          // style={{display: 'flex', flexDirection: 'column'}}
        >
          <RoomCategoryCard
            id={idx}
            category={category}
            isSelected={selectedCardId === idx}
            onSelect={handleSelectCard}
          />
        </div>
      ))}
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    marginTop: "20px",
  },
};
