// src/components/SearchBar.js
import React from "react";
import "./searchbar2.css";
import "./Booking/booking.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const SearchBar = ({ filters, handleFilterChange, handleSearch }) => {
  return (
    <div className="search-container">
      
      <select id="room-dropdown" className="room-dropdown">
        <option value="">
          Start Date
        </option>
        <option value="Miami">Miami</option>
        <option value="Seattle">Seattle</option>
        <option value="Los Angeles">Los Angeles</option>
      </select>

      <select id="room-dropdown" className="room-dropdown">
        <option value="">
        Duration (Days)
        </option>
        <option value="Bahamas">Bahamas</option>
        <option value="Jamaica">Jamaica</option>
        <option value="Alaska">Alaska</option>
      </select>

      <select id="room-dropdown" className="room-dropdown">
        <option value="">
          Cost per Person
        </option>
        <option value="December">December</option>
        <option value="January">January</option>
        <option value="June">June</option>
      </select>

      <select id="room-dropdown" className="room-dropdown">
        <option value="">
          Start Port
        </option>
        <option value="4">4</option>
        <option value="7">7</option>
        <option value="10">10</option>
      </select>

      <select id="room-dropdown" className="room-dropdown">
        <option value="">
          City
        </option>
        <option value="4">4</option>
        <option value="7">7</option>
        <option value="10">10</option>
      </select>

      <select id="room-dropdown" className="room-dropdown">
        <option value="">
          Country
        </option>
        <option value="4">4</option>
        <option value="7">7</option>
        <option value="10">10</option>
      </select>

      <button onClick={handleSearch} className="search-button-2">
        SEARCH CRUISES
      </button>
      {/* </div> */}
    </div>
  );
};

export default SearchBar;
