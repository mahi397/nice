// src/components/Sidebar.js
import React, { useState } from "react";
import "./Sidebar.css";

const Sidebar = ({ onSelect }) => {
  const [selected, setSelected] = useState("overview");

  const handleClick = (option) => {
    setSelected(option);
    onSelect(option);
  };

  return (
    <div className="sidebar">
      <div
        className={`sidebar-item ${selected === "overview" ? "active" : ""}`}
        onClick={() => handleClick("overview")}
      >
        Overview
      </div>
      {/* <div
        className={`sidebar-item ${selected === "users" ? "active" : ""}`}
        onClick={() => handleClick("users")}
      >
        Manage Users
      </div> */}
      <div
        className={`sidebar-item ${selected === "trips" ? "active" : ""}`}
        onClick={() => handleClick("trips")}
      >
        Manage Trips
      </div>
      <div
        className={`sidebar-item ${selected === "ships" ? "active" : ""}`}
        onClick={() => handleClick("ships")}
      >
        Manage Ships
      </div>
      <div
        className={`sidebar-item ${selected === "ports" ? "active" : ""}`}
        onClick={() => handleClick("ports")}
      >
        Manage Ports
      </div>
      <div
        className={`sidebar-item ${selected === "restaurants" ? "active" : ""}`}
        onClick={() => handleClick("restaurants")}
      >
        Manage Restaurants
      </div>
      <div
        className={`sidebar-item ${selected === "activities" ? "active" : ""}`}
        onClick={() => handleClick("activities")}
      >
        Manage Activities
      </div>
      <div className='sidebar-item'>
        <button>Logout</button>
      </div>
    </div>
  );
};

export default Sidebar;
