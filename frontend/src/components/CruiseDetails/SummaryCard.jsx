import React from "react";
import { Link } from "react-router-dom";

export default function SummaryCard({ data }) {
  console.log("SummaryCard data", data);
  return (
    <div className="trip-card">
      <div className="card-content">
        <h2>{data.headline}</h2>
        <p>
          Start: {data.startPort} &gt; Celebration Key &gt; Nassau &gt;
          Half Moon Cay &gt; End: {data.endPort}
        </p>
        <p>
          {data.startDate} - {data.endDate}
        </p>
      </div>

      <div className="card-price">
        <p>Price: {data.description}</p>
        <button>
          <Link
            to={`nice/trips/${data.id}`}
            style={{ textDecoration: "none", color: "inherit" }}
          >
            START BOOKING
          </Link>
        </button>
      </div>
    </div>
  );
}
