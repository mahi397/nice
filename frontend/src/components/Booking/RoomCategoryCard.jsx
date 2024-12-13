import React from "react";
import manhImg from "../../assets/manhattan.avif";
import "./booking.css";
import room1 from '../../assets/room1.png';
import room2 from '../../assets/room2.png';
import room3 from '../../assets/room8.png';
import room4 from '../../assets/room10.png';
import room5 from '../../assets/room6.png';
import room6 from '../../assets/room9.png';
import room7 from '../../assets/room7.png';


const ItineraryCard = ({ id, category, isSelected, onSelect }) => {
  const handleClick = () => onSelect(id); // id should be given by api

  const mockText = (
    <>
      <strong>{category.stateroomtype}</strong>
      <br />
      <p>{category.roomsize} sqft</p>
      <br />
      <p>
        {category.numberofbeds} beds, {category.numberofbaths} baths, {category.numberofbalconies}{" "}
        balconies
      </p>
    </>
  );

  function calcImg() {
    if (id === 0) {
      return room1;
    } else if (id === 1) {
      return room2;
    } else if (id === 2) {
      return room3;
    } else if (id === 3) {
      return room4;
    } else if (id === 4) {
      return room5;
    } else if (id === 5) {
      return room6;
    } else if (id === 6) {
      return room7;
    }
  }

  return (
    <div onClick={handleClick}>
      <div
        // style={styles.card}
        className={`room-category-card ${isSelected ? "selected" : ""}`}
      >
        <img src={calcImg()} alt="Card Image" style={styles.image} />
        <div style={styles.textContent}>
          <p>{mockText}</p>
        </div>
      </div>
    </div>
  );
};

const styles = {
  card: {
    display: "flex",
    width: "100%",
    height: "128px",
    borderRadius: "8px", // Rounded corners
    overflow: "hidden", // Ensures no content overflows outside the card
    backgroundColor: "#f4f4f9", // Light background color
    margin: "30px auto", // Centered with a top-bottom margin
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)", // Subtle shadow for a nice 3D effect
    cursor: "pointer",
    transition: "all 0.3s ease-in-out",
  },
  image: {
    width: "20%",
    height: "100%",
    objectFit: "cover", // Ensures the image covers its container
    // borderRadius: '16px 0 0 16px', // Rounded corners only on the left
  },
  textContent: {
    width: "80%",
    padding: "20px",
    display: "flex",
    // justifyContent: "center",
    alignItems: "center",
    textAlign: "justify",
    fontSize: "16px",
    color: "#333", // Darker color for readability
    marginTop: "20px",
    marginBottom: "20px",
  },
};

export default ItineraryCard;
