import React from 'react';
import './booking.css';
import roomImg from '../../assets/room2.png';

const RoomCard = ({ room }) => {
  if (!room) return null;

  return (
    // <div className="room-card">
    <div style={styles.roomcard}>
      {/* <h2 className="room-title">Room {room.number}</h2> */}
      <img 
        src={roomImg} 
        alt={`Room ${room.number}`} 
        // className="room-image" 
        style={styles.roomimg}
      />
      {/* <div className="room-description"> */}
        <div style={styles.roomdesc}>
          <p><b>Room No. </b>{room.number}</p>
          <p><b>Location:</b> {room.location}</p>
          <p><b>Category:</b> {room.category}</p>
        <h3>Amenities:</h3>
        <ul>
          {room.amenities.map((amenity, index) => (
            <li key={index}>{amenity}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

const styles = {
  roomcard: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '1096px',
    padding: '1rem',
    border: '1px solid #ccc',
    borderRadius: '16px',
    margin: '1rem',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f4f4f9',
  },
  roomimg: {
    width: '50%',
    // height: 'auto',
    borderRadius: '5px',
    objectFit: 'cover',
    marginRight: 'auto'
  },
  roomdesc: {
    width: '50%',
    padding: '1rem',
    color: '#333',
    marginLeft: '30px'
  }
};

export default RoomCard;
