import React, { useState } from "react";
import "./booking.css";
import bahamas from "../../assets/bahamas.webp";
import "../CruiseDetails/cruise.css";
import BgImage from '../CruiseDetails/BgImage';
import Summary from '../CruiseDetails/Summary';
import RoomInfoCard from '../Booking/RoomInfoCard';
import ItinerarySummaryCard from '../Booking/ItinerarySummaryCard';
import PaymentSummaryCard from "./PaymentSummaryCard";
import HeaderLoggedIn from '../HeaderLoggedIn';


const ReviewBooking = () => {

    const room = 
        {
            number: 108,
            location: "Stern",
            category: "Interior",
            image: "https://via.placeholder.com/392x220.png?text=Room+101",
            amenities: [
              "Two twin beds",
              "Desk and seat",
              "Full bathroom with shower",
              "Ample closet space",
            ],
          }
    

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
<HeaderLoggedIn />  
<div className="booking-summary-container">
      <div className="booking-summary-left">
      <h1 style={{color: 'black', fontFamily: 'Bebas Neue', }}>BOOKING SUMMARY</h1>
      <br />
        <ItinerarySummaryCard />
        <br />
        {/* <br /> */}
        <h2 style={{fontFamily: 'Bebas Neue', fontSize: '35px'}}>ROOM SELECTED</h2>
        <RoomInfoCard room={room}/>
      </div>
      <div className="booking-summary-right">
        <PaymentSummaryCard />
      </div>
    </div>
</>
    
  );
};

export default ReviewBooking;
