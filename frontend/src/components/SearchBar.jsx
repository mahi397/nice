// src/components/SearchBar.js
import React, {useState} from "react";
import "./searchbar2.css";
import "./Booking/booking.css";
import { DatePicker, Space, Slider, Input } from "antd";
import { API_URL } from "../constants";
import axios from "axios";

const { RangePicker } = DatePicker;

const SearchBar = ({ filters, handleFilterChange, handleSearchResults }) => {
  const [dateRange, setDateRange] = useState([]);
  const [priceRange, setPriceRange] = useState([1000, 2000]);
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");

  const handleDateChange = (dates) => {
    setDateRange(dates);
  };

  const handlePriceChange = (value) => {
    setPriceRange(value);
  };

  const handleCityChange = (e) => {
    setCity(e.target.value);
  };

  const handleCountryChange = (e) => {
    setCountry(e.target.value);
  };

  const handleSearch = async () => {
    const queryParams = new URLSearchParams();

    if (dateRange.length === 2) {
      queryParams.append("startdate_min", dateRange[0].format("YYYY-MM-DD"));
      queryParams.append("startdate_max", dateRange[1].format("YYYY-MM-DD"));
    }
    queryParams.append("tripcostperperson_min", priceRange[0]);
    queryParams.append("tripcostperperson_max", priceRange[1]);
    if (city) queryParams.append("port_city", city);
    if (country) queryParams.append("port_country", country);

    const queryString = queryParams.toString();
    const url = `${API_URL}/trips/list?${queryString}`;
    const plainURL = `${API_URL}/trips/list`;
    try {
      const response = await axios.get(url);
      // const response = await axios.get(plainURL);
      handleSearchResults(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  return (
    <div className="search-container">
      <div className="search-item">
        <label htmlFor="date-picker">Start Date Range</label>
        <Space className="search-item">
          <RangePicker id="date-picker" onChange={handleDateChange} />
        </Space>
      </div>

      <div className="search-item">
        <label htmlFor="price-slider">Cost per head</label>
        <Slider
          id="price-slider"
          range
          defaultValue={priceRange}
          min={500}
          max={10000}
          step={1000}
          tooltip={{
            open: true,
            placement: "bottom",
          }}
          onChange={handlePriceChange}
        />
        
      </div>

      <Input
        className="search-item"
        placeholder="Departure City"
        value={city}
        onChange={handleCityChange}
      />
      <Input className="search-item" placeholder="Departure Country" value={country}
        onChange={handleCountryChange} />

      {/* <select id="room-dropdown" className="room-dropdown">
        <option value="">
          Start Date
        </option>
        <option value="Miami">Miami</option>
        <option value="Seattle">Seattle</option>
        <option value="Los Angeles">Los Angeles</option>
      </select> */}

      {/* <select id="room-dropdown" className="room-dropdown">
        <option value="">
        Duration (Days)
        </option>
        <option value="Bahamas">Bahamas</option>
        <option value="Jamaica">Jamaica</option>
        <option value="Alaska">Alaska</option>
      </select> */}

      {/* <select id="room-dropdown" className="room-dropdown">
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
      </select> */}
      {/* 
        <input type="text">City</input>
        <input type="text">Country</input> */}

      <button onClick={handleSearch} className="search-button-2">
        SEARCH CRUISES
      </button>
      {/* </div> */}
    </div>
  );
};

export default SearchBar;
