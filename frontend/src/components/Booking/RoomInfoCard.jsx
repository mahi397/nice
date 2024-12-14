import React from 'react';
import './booking.css';
import room9 from '../../assets/room9.png';
import room10 from '../../assets/room10.png';


const RoomCard = ({ rooms }) => {
  if (!rooms || rooms.length === 0) return null;


  const calcImg = (room) => {
    if (room.number === 108) {
      return room9;
    } else {
      return room10;
    }
  }

  return (
    <div className="room-card-container">
      {rooms.map((room, index) => (
        
        <div key={index} style={styles.roomcard}>
          <img 
            src={calcImg(room)} 
            alt={`Room ${room.number}`} 
            className="room-image" 
            style={styles.roomimg}
          />
      
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
    ))}
    </div>
  );
};

const styles = {
  roomcard: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '900px',
    padding: '1rem',
    border: '1px solid #ccc',
    borderRadius: '16px',
    marginLeft: '20px',
    marginBottom: '10px',
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
