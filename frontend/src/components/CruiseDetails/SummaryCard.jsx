import React from "react";

export default function SummaryCard() {
  return (
    <div className="trip-card">
      <div className="card-content">
        <h2>{trip.name}</h2>
        <p>Start: {trip.startPort} `&gt;` </p>
        <p>End: {trip.endPort}</p>
        <p>
          {trip.startDate} - {trip.endDate}
        </p>
      </div>

      <div>
      <p>Price: {trip.tripCostPerPerson}</p>
      <button>
        <Link
          to={`nice/trips/${trip.id}`}
          style={{ textDecoration: "none", color: "inherit" }}
        >
          START BOOKING
        </Link>
      </button>  
      </div>
      
    </div>
  );
}
