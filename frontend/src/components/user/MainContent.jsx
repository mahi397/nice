import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MainContent.css';

const MainContent = () => {
  const [userData, setUserData] = useState({});
  const [trips, setTrips] = useState([]);

  // Mock API data for the cruises
  const mockTrips = [
    { id: 1, name: 'Bahamas Cruise', startPort: 'Miami', endPort: 'Bahamas', startMonth: 'December', duration: 4, imageUrl: 'https://via.placeholder.com/150' },
    { id: 2, name: 'Caribbean Cruise', startPort: 'Miami', endPort: 'Jamaica', startMonth: 'January', duration: 7, imageUrl: 'https://via.placeholder.com/150' },
    { id: 3, name: 'Alaska Cruise', startPort: 'Seattle', endPort: 'Alaska', startMonth: 'June', duration: 10, imageUrl: 'https://via.placeholder.com/150' },
  ];


  useEffect(() => {

    axios.get('/api/user-profile')
      .then(response => setUserData(response.data))
      .catch(error => console.log(error));

    // Fetch user's upcoming trips
    axios.get('/api/upcoming-trips')
      .then(response => setTrips(response.data))
      .catch(error => console.log(error));
  }, []);

  return (
    <div className="main-content">
      {/* <h2>Welcome, {userData.name}</h2> */}
      <h3>Upcoming Trips</h3>
      <ul>
        {/* {trips.map((trip, index) => (
          <li key={index}>
            {trip.name} - {trip.startDate} to {trip.endDate}
          </li>
        ))} */}
        {mockTrips.map((trip, index) => (
          <li key={index}>
            {trip.name} - {trip.startPort} to {trip.endPort}
          </li>
        ))}

      </ul>
    </div>
  );
};

export default MainContent;
