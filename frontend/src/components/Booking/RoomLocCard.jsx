import React from 'react';
import port from '../../assets/port.png';
import starboard from '../../assets/starboard.png';
import bow from '../../assets/bow.png';
import stern from '../../assets/stern2.png';

export default function RoomLocCard({ data, isSelected, onSelect, children, extraStyles = {} }) {
  const handleClick = () => onSelect && onSelect(data?.id);

  const calcImg = () => {
    if (data.id === 1) {
      return bow;
    } else if (data.id === 2) {
      return stern;
    } else if (data.id === 3) {
      return port;
    } else if (data.id === 4) {
      return starboard;
    }
  }

  return (
    <div className={`room-loc-card ${isSelected ? 'selected' : ''}`} 
    onClick={handleClick}
      style={extraStyles}>
      <img src={calcImg()} style={{objectFit: 'cover', width: '100%'}} />
    </div>
  )
}

