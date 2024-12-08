import React, { useState } from "react";
import RoomDetailCard from "./RoomDetailCard";
import "./booking.css";

const RoomSelection = () => {
  // Sample data for available rooms
  const availableRooms = [
    {
      number: 101,
      image: "https://via.placeholder.com/392x220.png?text=Room+101",
      amenities: [
        "Two twin beds",
        "Desk and seat",
        "Full bathroom with shower",
        "Ample closet space",
      ],
    },
    {
      number: 102,
      image: "https://via.placeholder.com/392x220.png?text=Room+102",
      amenities: [
        "One king bed",
        "Work desk",
        "En-suite bathroom with bathtub",
        "Spacious wardrobe",
      ],
    },
    {
      number: 103,
      image: "https://via.placeholder.com/392x220.png?text=Room+103",
      amenities: [
        "Queen-size bed",
        "Study table and chair",
        "Luxury bathroom",
        "Private balcony",
      ],
    },
    {
      number: 104,
      image: "https://via.placeholder.com/392x220.png?text=Room+104",
      amenities: [
        "Two double beds",
        "Mini fridge",
        "Full bathroom",
        "Plenty of storage",
      ],
    },
  ];

  // State to track the selected room
  const [selectedRoomNumber, setSelectedRoomNumber] = useState(null);

  // Get the room details from the availableRooms list
  const selectedRoom = availableRooms.find(
    (room) => room.number === Number(selectedRoomNumber)
  );

  return (
    <div className="room-selection-container">
      <h2>Select a Room</h2>
      <select
        id="room-dropdown"
        className="room-dropdown"
        value={selectedRoomNumber || ""}
        onChange={(e) => setSelectedRoomNumber(e.target.value)}
      >
        <option value="" disabled>
          Room number
        </option>
        {availableRooms.map((room) => (
          <option key={room.number} value={room.number}>
            Room {room.number}
          </option>
        ))}
      </select>

      {/* Room details card appears when a room is selected */}
      {selectedRoom && <RoomDetailCard room={selectedRoom} />}
    </div>
  );
};

export default RoomSelection;
