// src/pages/HomePage.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import "./trip.css";
import { Link } from "react-router-dom";

const HomePage = () => {
  const [trips, setTrips] = useState([]);
  const [filteredTrips, setFilteredTrips] = useState([]);
  const [filters, setFilters] = useState({
    startPort: "",
    endPort: "",
    startMonth: "",
    duration: "",
  });

  useEffect(() => {
    // Mock API data for the cruises
    const mockTrips = [
      {
        id: 1,
        name: "Bahamas Cruise",
        startPort: "Miami",
        endPort: "Bahamas",
        startMonth: "December",
        duration: 4,
        imageUrl: "https://via.placeholder.com/150",
      },
      {
        id: 2,
        name: "Caribbean Cruise",
        startPort: "Miami",
        endPort: "Jamaica",
        startMonth: "January",
        duration: 7,
        imageUrl: "https://via.placeholder.com/150",
      },
      {
        id: 3,
        name: "Alaska Cruise",
        startPort: "Seattle",
        endPort: "Alaska",
        startMonth: "June",
        duration: 10,
        imageUrl: "https://via.placeholder.com/150",
      },
    ];

    setTrips(mockTrips);
    setFilteredTrips(mockTrips); // Initially display all trips
  }, []);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const handleSearch = () => {
    let filtered = trips;

    // Apply filters
    if (filters.startPort) {
      filtered = filtered.filter(
        (trip) => trip.startPort === filters.startPort
      );
    }
    if (filters.endPort) {
      filtered = filtered.filter((trip) => trip.endPort === filters.endPort);
    }
    if (filters.startMonth) {
      filtered = filtered.filter(
        (trip) => trip.startMonth === filters.startMonth
      );
    }
    if (filters.duration) {
      filtered = filtered.filter(
        (trip) => trip.duration === parseInt(filters.duration)
      );
    }

    setFilteredTrips(filtered);
  };

  return (
    <div>
      <h1 style={{ marginTop: "10px", marginLeft: "10px", color: 'gray' }}>
        Discover Cruises
      </h1>

      {/* Search Bar Component */}
      <SearchBar
        filters={filters}
        handleFilterChange={handleFilterChange}
        handleSearch={handleSearch}
      />

      {/* Display Filtered Trips */}
      <div className="trip-cards">
        {filteredTrips.length > 0 ? (
          filteredTrips.map((trip) => (
            <div key={trip.id} className="trip-card">
              <img src={trip.imageUrl} alt={trip.name} />
              <div className="card-content">
                <h2>{trip.name}</h2>
                <p>Start Port: {trip.startPort}</p>
                <p>End Port: {trip.endPort}</p>
                <p>Start Month: {trip.startMonth}</p>
                <p>Duration: {trip.duration} days</p>
                <p>Price: {trip.tripCostPerPerson}</p>
              </div>
              <button>
                <Link
                  to={`nice/trips/${trip.id}`}
                  style={{ textDecoration: "none", color: "inherit" }}
                >
                  View Details
                </Link>
              </button>
            </div>
          ))
        ) : (
          <p>No cruises found based on your search criteria</p>
        )}
      </div>
    </div>
  );
};

export default HomePage;
