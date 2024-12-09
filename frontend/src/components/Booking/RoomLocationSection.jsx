import React, { useState } from "react";
import RoomLocCard from "./RoomLocCard";
import SelectLocationCard from "./SelectLocationCard";

export default function RoomLocationSection() {
  const locations = [
    { id: 1, name: "Bow (Forward)", availableRooms: 5 },
    { id: 2, name: "Stern (Back)", availableRooms: 3 },
    { id: 3, name: "Port Side", availableRooms: 2 },
    { id: 4, name: "Starboard Side", availableRooms: 4 },
  ];

  const [selectedCardId, setSelectedCardId] = useState(null);
  const selectedCard = locations.find((card) => card.id === selectedCardId);

  return (
    <div className="room-location-section">
      <h2 style={{ marginTop: "50px" }}>Select Room Location</h2>
      <div className="location-section">
        {locations.map((location) => (
          <div key={location.id}>
            <RoomLocCard
              data={location}
              isSelected={selectedCardId === location.id}
              onSelect={setSelectedCardId}
            />
          </div>
        ))}
      </div>
      {/* Bottom card that appears when a card is selected */}
      {selectedCardId && (
        <div className="bottom-row">
          <SelectLocationCard>
            <p style={{marginLeft: '20px'}}>You selected: <strong>{selectedCard.name}</strong></p>
            <span className="caption" style={{ fontWeight: 'bold', color: 'maroon' }}>
              Available Rooms: {selectedCard.availableRooms}
            </span>
            <button className="action-button" style={{ marginRight: "20px" }}>
              SELECT
            </button>
          </SelectLocationCard>
        </div>
      )}
    </div>
  );
}
