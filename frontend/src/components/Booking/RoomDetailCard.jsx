import React from 'react';

const RoomCard = ({ room }) => {
  if (!room) return null;

  return (
    <div className="room-card">
      <h2 className="room-title">Room {room.number}</h2>
      <img 
        src={room.image} 
        alt={`Room ${room.number}`} 
        className="room-image" 
      />
      <div className="room-description">
        <h3>Room Includes:</h3>
        <ul>
          {room.amenities.map((amenity, index) => (
            <li key={index}>{amenity}</li>
          ))}
        </ul>
      </div>
      {/* Button added below the amenities list */}
      <button className="room-button">
        Select Room
      </button>
    </div>
  );
};

export default RoomCard;
