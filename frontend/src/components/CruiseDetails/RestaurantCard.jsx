import React, { act } from "react";
import restaurantImg from "../../assets/restaurant.avif";
import { FaCheckCircle, FaDollarSign, FaArrowCircleRight } from "react-icons/fa";
import { IoIosArrowDropright } from "react-icons/io";
import { AiFillDollarCircle } from "react-icons/ai";


const RestaurantCard = () => {
  const headline = "Water activities";
  const subtitle = "Additional";

  return (
    <div style={styles.rowContainer}>
      <div style={styles.card}>
        <img
          src={restaurantImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <h3 style={styles.headline}>{headline}</h3>
          <h5 style={styles.subtitle}>
          <AiFillDollarCircle style={styles.icon} /> {subtitle}
          </h5>
        </div>
      </div>
      
      <div style={styles.card}>
        <img
          src={restaurantImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <h3 style={styles.headline}>{headline}</h3>
          <h5 style={styles.subtitle}>
          <AiFillDollarCircle style={styles.icon} /> {subtitle}
          </h5>
        </div>
      </div>

      <div style={styles.card}>
        <img
          src={restaurantImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <h3 style={styles.headline}>{headline}</h3>
          <h5 style={styles.subtitle}>
            <AiFillDollarCircle style={styles.icon} /> {subtitle}
          </h5>
        </div>
      </div>

      <div style={styles.card}>
        <img
          src={restaurantImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <h3 style={styles.headline}>{headline}</h3>
          <h5 style={styles.subtitle}>
            <AiFillDollarCircle style={styles.icon} /> {subtitle}
          </h5>
        </div>
      </div>
      {/* <FaArrowCircleRight style={styles.icon} /> */}
      <IoIosArrowDropright style={styles.arrow} />
    </div>
  );
};

const styles = {
  card: {
    width: "312px",
    height: "261px",
    borderRadius: "16px", // Rounded corners
    overflow: "hidden", // Ensures no content overflows outside the card
    backgroundColor: "#f4f4f9", // Light background color
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)", // Subtle shadow for a nice 3D effect
    display: "flex",
    flexDirection: "column", // Stacks image and text vertically
  },
  image: {
    width: "100%", // Full width of the card
    height: "50%", // Top half of the card
    objectFit: "cover", // Ensures the image covers its container
  },
  textContent: {
    width: "100%",
    height: "50%", // Bottom half of the card
    paddingLeft: "16px", // Padding for breathing room
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between", // Places headline at the top, subtitle, and price at the bottom
  },
  headline: {
    fontSize: "18px", // Larger font for the headline
    fontWeight: "bold",
    color: "#333",
    marginBottom: "8px", // Small gap between the image and the headline
  },
  subtitle: {
    fontSize: "14px",
    color: "#555", // Slightly lighter color for the subtitle
    display: "flex",
    alignItems: "center", // Aligns the icon and text vertically
    marginTop: "16px", // Space between subtitle and price
    marginBottom: "20px", // Space between headline and subtitle
  },
  price: {
    fontSize: "14px",
    color: "#555", // Slightly lighter color for the price
    display: "flex",
    alignItems: "center", // Aligns the icon and text vertically
  },
  icon: {
    color: "rgb(16, 85, 154)", // Green color for the tick and dollar sign
    marginRight: "8px", // Space between icon and text
    fontSize: "16px", // Font size of the icon
  },
  rowContainer: {
    display: "flex",
    justifyContent: "space-around",
    flexWrap: "wrap",
    margin: "20px",
  },
  arrow: {
    marginTop: "120px",
    fontSize: "30px",
    color: 'gray'
  }
};

export default RestaurantCard;
