import React from 'react'

export default function RoomLocCard({ data, isSelected, onSelect, children, extraStyles = {} }) {
  const handleClick = () => onSelect && onSelect(data?.id);

  return (
    <div className={`room-loc-card ${isSelected ? 'selected' : ''}`} 
    onClick={handleClick}
      style={extraStyles}>
      <img />
    </div>
  )
}

