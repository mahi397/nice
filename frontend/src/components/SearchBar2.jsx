import React, { useState } from 'react';

const FilteredSearchBar = () => {
  const [filters, setFilters] = useState({
    filter1: '',
    filter2: '',
    filter3: '',
    filter4: ''
  });

  const handleSearch = () => {
    console.log(filters); // Handle the search logic here
  };

  return (
    <div className="search-bar">
      <select
        value={filters.filter1}
        onChange={(e) => setFilters({ ...filters, filter1: e.target.value })}
        className="dropdown"
      >
        <option value="">Filter 1</option>
        {/* Add your options here */}
      </select>
      <select
        value={filters.filter2}
        onChange={(e) => setFilters({ ...filters, filter2: e.target.value })}
        className="dropdown"
      >
        <option value="">Filter 2</option>
        {/* Add your options here */}
      </select>
      <select
        value={filters.filter3}
        onChange={(e) => setFilters({ ...filters, filter3: e.target.value })}
        className="dropdown"
      >
        <option value="">Filter 3</option>
        {/* Add your options here */}
      </select>
      <select
        value={filters.filter4}
        onChange={(e) => setFilters({ ...filters, filter4: e.target.value })}
        className="dropdown"
      >
        <option value="">Filter 4</option>
        {/* Add your options here */}
      </select>
      <button className="search-button" onClick={handleSearch}>Search</button>
    </div>
  );
};

export default FilteredSearchBar;
