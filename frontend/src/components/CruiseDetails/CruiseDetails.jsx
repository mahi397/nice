import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom"; // Hook to get URL params
import axios from "axios"; // Axios to make HTTP requests
import SummaryCard from "./SummaryCard";
import DayWiseCard from './DayWiseCard';
import ActivityCard from "./ActivityCard";
import RestaurantCard from './RestaurantCard';
import OtherPackages from "./OtherPackages";


const CruiseDetails = () => {
  const { id } = useParams(); // Get the cruise id from the URL
  const [cruise, setCruise] = useState(null);

  useEffect(() => {
    // Fetch the cruise details from the backend using the id
    const fetchCruiseDetails = async () => {
      try {
        const response = await axios.get(`/nice/trips/${id}/`);
        setCruise(response.data);
      } catch (error) {
        console.error("Error fetching cruise details:", error);
      }
    };

    fetchCruiseDetails();
  }, [id]); // Fetch details whenever the id changes

  // If the cruise data is still loading, display a loading state
  if (!cruise) {
    return <div>Loading...</div>;
  }


  const mockData = [
    {
      id: 1,
      name: '8-Day The Bahamas from Manhattan, New York City, NY',
      startPort: 'Manhattan, New York City',
      portStops: '',
      endPort: 'Manhattan, New York City',
      startDate: 'Wed Jul 1, 2026',
      endDate: 'Thu Jul 9, 2026',
      price: '$979',
      itinerary: {
        // day1: 
        // day2: 
      }
    }
  ]

  return (
    // <div className="cruise-details">
    //   <h2>{cruise.name}</h2>
    //   <img src={cruise.image} alt={cruise.name} />
    //   <p><strong>Destination:</strong> {cruise.destination}</p>
    //   <p><strong>Duration:</strong> {cruise.duration} days</p>
    //   <p><strong>Price:</strong> ${cruise.price}</p>
    //   <p><strong>Description:</strong> {cruise.description}</p>
    //   <button>Book Now</button>
    // </div>
    <>
      <SummaryCard />
      <h2>Cruise Itinerary</h2>
      <DayWiseCard />
      <h2>Activities Onboard</h2>
      <ActivityCard />
      <h2>Dining Onboard</h2>
      <RestaurantCard />
      <OtherPackages />
    </>
  );
};

export default CruiseDetails;

