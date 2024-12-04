// src/components/SearchBar.js
import React from 'react';

const SearchBar = ({ filters, handleFilterChange, handleSearch }) => {
  return (
    <div className="search-bar">
      <div className="search-input">
        <label htmlFor="startPort">Starting Port</label>
        <select
          id="startPort"
          name="startPort"
          value={filters.startPort}
          onChange={handleFilterChange}
        >
          <option value="">Select Port</option>
          <option value="Miami">Miami</option>
          <option value="Seattle">Seattle</option>
          <option value="Los Angeles">Los Angeles</option>
        </select>
      </div>

      <div className="search-input">
        <label htmlFor="endPort">Ending Port</label>
        <select
          id="endPort"
          name="endPort"
          value={filters.endPort}
          onChange={handleFilterChange}
        >
          <option value="">Select Port</option>
          <option value="Bahamas">Bahamas</option>
          <option value="Jamaica">Jamaica</option>
          <option value="Alaska">Alaska</option>
        </select>
      </div>

      <div className="search-input">
        <label htmlFor="startMonth">Start Month</label>
        <select
          id="startMonth"
          name="startMonth"
          value={filters.startMonth}
          onChange={handleFilterChange}
        >
          <option value="">Select Month</option>
          <option value="December">December</option>
          <option value="January">January</option>
          <option value="June">June</option>
        </select>
      </div>

      <div className="search-input">
        <label htmlFor="duration">Duration (Days)</label>
        <select
          id="duration"
          name="duration"
          value={filters.duration}
          onChange={handleFilterChange}
        >
          <option value="">Select Duration</option>
          <option value="4">4</option>
          <option value="7">7</option>
          <option value="10">10</option>
        </select>
      </div>

      <button onClick={handleSearch} className="search-button">
        Search
      </button>
    </div>
  );
};

export default SearchBar;
