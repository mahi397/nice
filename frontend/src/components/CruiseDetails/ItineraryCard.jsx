import React from "react";
import manhImg from "../../assets/manhattan.avif";

const ItineraryCard = () => {
  const mockText = (
    <>
      <strong>Day 1: Manhattan, New York City</strong>
      <br />
      <strong>Departs at 4:00 PM</strong>
      <br />
      <br />
      Start your Carnival cruise from the city that defined 'cosmopolitan': New
      York City. This urban island overflows with art and architecture, lively
      ethnic neighborhoods, designer shops... and the best restaurants in the
      world, from the ultra-high-end to the comfy neighborhood hole-in-the-wall.
      As your cruise leaving from New York glides down the Hudson River towards
      sunny islands or historic New England harbors, you'll pass metropolitan
      must-sees, world-renowned icons like the Empire State Building and the
      Statue of Liberty.
    </>
  );

  return (
    <>
      <div style={styles.card}>
        <img
          src={manhImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <p>{mockText}</p>
        </div>
      </div>
      <div style={styles.card}>
        <img
          src={manhImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <p>{mockText}</p>
        </div>
      </div>
    </>
  );
};

const styles = {
  card: {
    display: "flex",
    width: "90%", // Takes up 90% of the screen width
    height: "300px",
    borderRadius: "16px", // Rounded corners
    overflow: "hidden", // Ensures no content overflows outside the card
    backgroundColor: "#f4f4f9", // Light background color
    margin: "30px auto", // Centered with a top-bottom margin
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)", // Subtle shadow for a nice 3D effect
  },
  image: {
    width: "50%", // Left half for the image
    height: "100%",
    objectFit: "cover", // Ensures the image covers its container
    // borderRadius: '16px 0 0 16px', // Rounded corners only on the left
  },
  textContent: {
    width: "50%", // Right half for the text
    padding: "20px", // Padding for some breathing room
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "justify",
    fontSize: "16px",
    color: "#333", // Darker color for readability
    marginTop: "20px",
    marginBottom: "20px",
  },
};

export default ItineraryCard;
