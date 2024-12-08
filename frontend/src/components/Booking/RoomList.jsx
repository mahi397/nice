import React, { useState } from 'react';
import Card from './AddRoom'; // Import the card component
import './booking.css';

const CardList = () => {
  const [cards, setCards] = useState([
    { roomNumber: 1, guestCount: 1 },
  ]); // Initialize with one card, containing guest count

  // Handle removing a card
  const handleRemove = (index) => {
    const newCards = cards.filter((_, i) => i !== index);
    setCards(newCards);
  };

  // Handle adding a new card
  const handleAdd = () => {
    setCards([...cards, { roomNumber: cards.length + 1, guestCount: 1 }]);
  };

  // Handle changing the guest count
  const handleGuestCountChange = (index, newCount) => {
    const updatedCards = [...cards];
    updatedCards[index].guestCount = newCount;
    setCards(updatedCards);
  };

  return (
    <div className='add-room-container'>
      {cards.map((card, index) => (
        <Card
          key={index}
          roomNumber={index + 1} // Pass the room number based on the index (starting from 1)
          guestCount={card.guestCount}
          onRemove={() => handleRemove(index)}
          onAdd={handleAdd}
          cardCount={cards.length} // Pass the current card count to each card
          onGuestCountChange={(newCount) => handleGuestCountChange(index, newCount)}
        />
      ))}
    </div>
  );
};

export default CardList;
