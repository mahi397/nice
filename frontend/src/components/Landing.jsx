import React, { useState, useEffect } from "react";
import SearchBar from "./SearchBar";
import "./trip.css";
import "../components/CruiseDetails/cruise.css";
import { Link } from "react-router-dom";
import ItineraryCard from "./CruiseDetails/ItineraryCard";
import Header from "./Header";
import BgImage from "./CruiseDetails/BgImage";
import TripSummaryCard from "./TripSummaryCard";


const HomePage = () => {
  const mockTrips = [
    {
      trip: {
        tripid: 1,
        tripname: "Bahamas Cruise",
        startPort: "Miami",
        endPort: "Bahamas",
        startMonth: "December",
        startdate: "12/01/2021",
        enddate: "12/05/2021",
        description: "some text",
        duration: 4,
        tripcostperperson: 979,
      
      },
      trip: {
        tripid: 2,
        tripname: "Caribbean Cruise",
        startPort: "Miami",
        endPort: "Jamaica",
        startMonth: "January",
        startdate: "12/01/2021",
        enddate: "12/05/2021",
        description: "some text",
        duration: 4,
        tripcostperperson: 979,
      
      },
      trip: {
        tripid: 3,
        tripname: "Alaska Cruise",
        startPort: "Miami",
        endPort: "Bahamas",
        startMonth: "December",
        startdate: "12/01/2021",
        enddate: "12/05/2021",
        description: "some text",
        duration: 4,
        tripcostperperson: 979,
      
      }
      //   imageUrl: landing1,
    },
  ];

  const [trips, setTrips] = useState([]);
  const [searchResults, setSearchResults] = useState([]);

  const handleSearchResults = (results) => {
    setSearchResults(results);
  };
  
  // const [filteredTrips, setFilteredTrips] = useState([]);
  // const [filters, setFilters] = useState({
  //   startPort: "",
  //   endPort: "",
  //   startDate: "",
  //   endDate: "",
  //   duration: "",
  // });

  // useEffect(() => {
  //   // Mock API data for the cruises
  //   setTrips(mockTrips);
  //   setFilteredTrips(mockTrips); // Initially display all trips
  // }, []);

  // const handleFilterChange = (e) => {
  //   const { name, value } = e.target;
  //   setFilters((prevFilters) => ({
  //     ...prevFilters,
  //     [name]: value,
  //   }));
  // };

  // const handleSearch = () => {
  //   let filtered = trips;

  //   // Apply filters
  //   if (filters.startPort) {
  //     filtered = filtered.filter(
  //       (trip) => trip.startPort === filters.startPort
  //     );
  //   }
  //   if (filters.endPort) {
  //     filtered = filtered.filter((trip) => trip.endPort === filters.endPort);
  //   }
  //   if (filters.startMonth) {
  //     filtered = filtered.filter(
  //       (trip) => trip.startMonth === filters.startMonth
  //     );
  //   }
  //   if (filters.duration) {
  //     filtered = filtered.filter(
  //       (trip) => trip.duration === parseInt(filters.duration)
  //     );
  //   }

  //   setFilteredTrips(filtered);
  // };

  return (
    <div className="cruise-details">
      <Header />
      <BgImage />
      <SearchBar
        // filters={filters}
        // onFilterChange={handleFilterChange}
        // onSearch={handleSearch}
        handleSearchResults={handleSearchResults}
      />
      <div className="trip-container">
      {searchResults.length > 0 ? (
        searchResults.map((trip, idx) => (
          <div key={idx}>
            <TripSummaryCard trip={trip} />
          </div>
        ))
      ) : (
        <p>No search results found.</p>
      )}
      </div>
    </div>
  );
};

export default HomePage;
