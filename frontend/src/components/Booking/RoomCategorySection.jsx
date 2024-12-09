import React, {useState} from "react";
import RoomCategoryCard from "./RoomCategoryCard";

export default function RoomCategorySection() {
  const [selectedCardId, setSelectedCardId] = useState(null);

  // Set the selected card
  const handleSelectCard = (id) => setSelectedCardId(id);

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
    <div className="room-category-section">
      <h2 style={{ marginTop: "50px" }}>Select Room Category</h2>
      {categories.map((category) => (
        <div key={category.id}>
          <RoomCategoryCard
            category={category}
            isSelected={selectedCardId === category.id}
            onSelect={handleSelectCard}
          />
        </div>
      ))}
    </div>
  );
}
