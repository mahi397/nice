import React from 'react';
import { Link } from 'react-router-dom';
import { IoLocationSharp } from "react-icons/io5";
import landing1 from '../assets/landing1.jpg';
import landing2 from '../assets/landing2.jpg';
import landing3 from '../assets/landing3.jpg';
import moment from 'moment'

const WideCard = (trip) => {
    console.log("TRIP:", trip.trip);
    // const { id, name, startPort, endPort, startMonth, startDate, endDate, description, duration, imageUrl } = trip;
  const leftHeading = trip.trip.tripname.toUpperCase();
  const leftParagraph1 = 'Start: Manhattan, New York City  >  Nassau  >  Half Moon Cay  > End: Manhattan, New York City';
  // const leftParagraph2 = "Wed Jul 1, 2025 - Thu Jul 9, 2025";
  const formattedStartDate = moment(trip.trip.startdate).format('ddd MMM D, YYYY');
  const formattedEndDate = moment(trip.trip.enddate).format('ddd MMM D, YYYY');
  const leftParagraph2 = `${formattedStartDate} - ${formattedEndDate}`;

  // const leftParagraph2 = `${trip.trip.startdate} - ${trip.trip.enddate}`;

  console.log('trip Summary Card rendered');
  return (
    <div style={styles.card}>
        {/**Image section */}
        <div style={styles.image}>
            <img src={landing1} alt="placeholder" style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      {/* Left Section (80%) */}
      <div style={styles.leftSection}>
        <h2 style={styles.heading}>{leftHeading}</h2>
        <p style={styles.paragraph}><span><IoLocationSharp /> </span>{leftParagraph1}</p>
        <p style={styles.dateText}>{leftParagraph2}</p>
      </div>

      {/* Right Section (20%) */}
      <div style={styles.rightSection}>
        {/* <p style={styles.fromText}>From</p> */}
        <p style={styles.priceText}>${trip.trip.tripcostperperson}</p>
        <p style={styles.priceDescription}>average per person, 2 person room</p>

        {/* Book Now Button */}
        <button style={styles.bookNowButton}>
            <Link to={`/cruisedetails/${trip.trip.tripid}`}>VIEW ITINERARY</Link></button>
      </div>
    </div>
  );
};

const styles = {
  card: {
    width: '1320px',
    height: '195px',
    borderRadius: '16px',
    backgroundColor: '#f4f4f9',
    display: 'flex', // Horizontal layout for left and right sections
    justifyContent: 'space-between',
    alignItems: 'center',
    // margin: '0 auto', // Center the card horizontally
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    overflow: 'hidden',
    color: 'black',
  },
  image: {
    width: '20%',
    height: '100%'
  },
  leftSection: {
    width: '60%',
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
    marginLeft: '80px', // Pushes the text to the right
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
