import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import { IoLocationSharp } from "react-icons/io5";

const WideCard = () => {
  const leftHeading = 'Dream Island Adventure';
  const leftParagraph1 = 'Los Angeles  >  Adelaide  >  Dubai  > New York';
  const leftParagraph2 = 'Fri Jan 3, 2025 - Tue Jan 7, 2025';

  console.log('Itinerary Summary Card rendered');

  // const [tripDetails, setTripDetails] = useState({});

  // useEffect(() => {
  //   console.log('Entering useEffect');
  //   // Retrieve trip details from sessionStorage
  //   const storedTripDetails = sessionStorage.getItem("bookingData");
  //   console.log('Stored Trip Details:', storedTripDetails);
  //   if (storedTripDetails) {
  //     setTripDetails(JSON.parse(storedTripDetails));
  //   }
  // }, []);

  // const leftHeading = tripDetails.trip_details.tripname.toUpperCase();
  // const portStops = tripDetails.trip_details.port_stops.map(stop => stop.port_name).join(' > ');
  // const leftParagraph1 = `${portStops}`;
  // const formattedStartDate = new Date(tripDetails.trip_details.startdate).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  // const formattedEndDate = new Date(tripDetails.trip_details.enddate).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  // const leftParagraph2 = `${formattedStartDate} - ${formattedEndDate}`;


  return (
    <div style={styles.card}>
      {/* Left Section (80%) */}
      <div style={styles.leftSection}>
        <h2 style={styles.heading}>{leftHeading}</h2>
        <p style={styles.paragraph}><span><IoLocationSharp /> </span>{leftParagraph1}</p>
        <p style={styles.dateText}>{leftParagraph2}</p>
      </div>
    </div>
  );
};

const styles = {
  card: {
    width: '900px',
    height: '200px',
    borderRadius: '16px',
    backgroundColor: '#f4f4f9',
    display: 'flex', // Horizontal layout for left and right sections
    justifyContent: 'space-between',
    alignItems: 'center',
    // margin: '0 auto', // Center the card horizontally
    // boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
    color: 'black',
    // margin: '-40px auto 0 auto',
    zIndex: 2,
    position: 'relative',
    marginLeft: '20px',
    border: '1px solid #ccc',
  },
  leftSection: {
    width: '80%',
    padding: '24px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-start',
  },
  heading: {
    fontSize: '30px',
    fontWeight: 'bold',
    color: 'rgb(16, 85, 154)',
    marginBottom: '30px',
    fontFamily: 'Bebas Neue, cursive',
  },
  paragraph: {
    fontSize: '16px',
    color: '#555',
    marginBottom: '14px',
    lineHeight: '1.5',
  },
  dateText: {
    fontSize: '14px', 
    fontWeight: 'bold',
  },
  rightSection: {
    width: '20%',
    padding: '24px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between', // Space between content and button
    alignItems: 'flex-end',
    position: 'relative',
  },
  fromText: {
    fontSize: '16px',
    color: '#555',
    // marginBottom: '8px',
  },
  priceText: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#28a745', // Green color to make it stand out
    // marginBottom: '4px',
  },
  priceDescription: {
    fontSize: '14px',
    color: '#555',
    marginLeft: '40px', // Pushes the text to the right
  },
  bookNowButton: {
    marginTop: '10px', // Pushes the button to the bottom
    padding: '12px 24px',
    backgroundColor: '#007bff', // Blue button color
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  // bookNowButtonHover: {
  //   backgroundColor: '#0056b3', // Darker shade on hover
  // }
};

export default WideCard;
