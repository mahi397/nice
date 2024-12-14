import React, { useEffect, useState } from "react";
import "./booking.css";
import bahamas from "../../assets/bahamas.webp";
import "../CruiseDetails/cruise.css";
import BgImage from "../CruiseDetails/BgImage";
import Summary from "../CruiseDetails/Summary";
import RoomInfoCard from "./RoomInfoCard";
import ItinerarySummaryCard from "./ItinerarySummaryCard";
import PaymentSummaryCard from "./PaymentSummaryCard";
import HeaderLoggedIn from "../HeaderLoggedIn";
import Header from "../Header";

const ReviewBooking = () => {
  const rooms = [
    {
      number: 108,
      location: "Stern",
      category: "Inside Stateroom",
      image: "https://via.placeholder.com/392x220.png?text=Room+101",
      amenities: [
        "One twin bed",
        "Desk and seat",
        "Full bathroom with shower",
        "Ample closet space",
      ],
    },
    {
      number: 105,
      location: "Bow",
      category: "Studio Stateroom",
      image: "https://via.placeholder.com/392x220.png?text=Room+101",
      amenities: [
        "Single twin bed",
        "Full bathroom with shower",
        "Ample closet space",
      ],
    },
  ];
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
  return (
    // <div className="review-booking-container">
    //   {/* Left Section */}
    //   <div className="left-section">
    //     <div className="card itinerary-card">
    //       <div
    //         className="itinerary-image"
    //         style={{ backgroundImage: {bahamas} }}
    //       ></div>
    //       <div className="itinerary-text">
    //         <h3>8-Day The Bahamas from Manhattan, New York City, NY</h3>
    //         <p>Wed Jul 1, 2026 - Thu Jul 9, 2026</p>
    //         <p>Ship: Carnival Venezia</p>
    //       </div>
    //     </div>

    //     <div className="booking-card room-card">
    //       <div
    //         className="room-image"
    //         style={{ backgroundImage: `url('https://via.placeholder.com/436x574')` }}
    //       ></div>
    //       <div className="room-text">
    //         <h3>Room Information</h3>
    //         <p>Interior Upper/Lower - 1 Room, 2 Guests - $2,008.00</p>
    //       </div>
    //     </div>
    //   </div>

    //   {/* Right Section */}
    //   <div className="right-section">
    //     <div className="booking-card payment-card">
    //       <div className="payment-details">
    //         <h3>Payment Summary</h3>
    //         <p>8-Day The Bahamas from Manhattan, New York City, NY</p>
    //         <p>Wed Jul 1, 2026 - Thu Jul 9, 2026</p>
    //         <p>Ship: Carnival Venezia</p>
    //         <hr />
    //         <p>Room 1: $2,008.00</p>
    //         <p>Guest 1 Total: $1,004.00</p>
    //         <p>Guest 2 Total: $1,004.00</p>
    //         <p>Total: $2,008.00</p>
    //       </div>
    //       <button className="checkout-button">
    //         Review and Pay
    //       </button>
    //     </div>
    //   </div>

    // </div>
    <>
      <Header />
      <div className="booking-summary-container">
        <div className="booking-summary-left">
          <h1 style={{ color: "black", fontFamily: "Bebas Neue" }}>
            BOOKING SUMMARY
          </h1>
          <br />
          <ItinerarySummaryCard />
          <br />
          {/* <br /> */}
          <h2 style={{ fontFamily: "Bebas Neue", fontSize: "35px" }}>
            ROOM SELECTION
          </h2>
          <RoomInfoCard rooms={rooms} />
        </div>
        <div className="booking-summary-right">
          <PaymentSummaryCard />
        </div>
      </div>
    </>
  );
};

export default ReviewBooking;