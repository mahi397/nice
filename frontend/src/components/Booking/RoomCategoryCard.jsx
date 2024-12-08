import React from "react";
import manhImg from "../../assets/manhattan.avif";
import "./booking.css";

const ItineraryCard = ({ category, isSelected, onSelect }) => {
  const handleClick = () => onSelect(category.id);

  const mockText = (
    <>
      <strong>{category.type}</strong>
      <br />
      <p>{category.size} sqft</p>
      <br />
      <p>
        {category.beds} beds, {category.baths} baths, {category.balconies}{" "}
        balconies
      </p>
    </>
  );

  return (
    <div onClick={handleClick}>
      <div
        // style={styles.card}
        className={`room-category-card ${isSelected ? "selected" : ""}`}
      >
        <img src={manhImg} alt="Card Image" style={styles.image} />
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
    width: "100%", // Takes up 90% of the screen width
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
