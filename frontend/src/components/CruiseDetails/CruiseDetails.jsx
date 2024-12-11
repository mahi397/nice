import React, { useEffect, useState } from "react";
import './cruise.css';
import { useParams } from "react-router-dom"; // Hook to get URL params
import axios from "axios"; // Axios to make HTTP requests
import { Card, Row, Col, Spin, Alert } from 'antd';
import SummaryCard from "./SummaryCard";
import DayWiseCard from "./DayWiseCard";
import ActivityCard from "./ActivityCard";
import RestaurantCard from "./RestaurantCard";
import { API_URL } from "../../constants";
import ItineraryCard from "./ItineraryCard";
import Summary from "./Summary";
import BgImage from "./BgImage";
import Header from "../Header";

const CruiseDetails = ({ tripid }) => {
  // const { id } = useParams(); // Get the cruise id from the URL
  const fallbackData = [
    {
      headline: 'Default Headline 1',
      subheading: 'Default Subheading 1',
      description: 'Fallback description in case of an error.',
      image: 'https://via.placeholder.com/300',
    },
    {
      headline: 'Default Headline 2',
      subheading: 'Default Subheading 2',
      description: 'Fallback description in case of an error.',
      image: 'https://via.placeholder.com/300',
    },
  ];

  const [cruise, setCruise] = useState(fallbackData);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    // Fetch the cruise details from the backend using the id
    const fetchCruiseDetails = async () => {
      try {
        const response = await axios.get(`${API_URL}/trips/list/${tripid}`);
        setCruise(response.data);
      } catch (error) {
        console.error('Error:', error);
        setError('Error fetching data');
        setCruise(fallbackData);  // Use fallback data if API call fails
      } finally {
        setLoading(false);
        console.log('Loading state set to false');
      }
    };

    fetchCruiseDetails();
  }, [tripid]); // Fetch details whenever the id changes

  // If the cruise data is still loading, display a loading state
  // if (!cruise) {
  //   return <div>Loading...</div>;
  // }
  // if (loading) {
  //   console.log('Loading is true, showing spinner');
  //   return <Spin size="large" />;
  // }

  // if (error) {
  //   return (
  //     <Alert
  //       message="Error"
  //       description="There was an issue fetching data from the API."
  //       type="error"
  //       showIcon
  //     />
  //   );
  // }


  const mockData = [
    {
      id: 1,
      name: "8-Day The Bahamas from Manhattan, New York City, NY",
      startPort: "Manhattan, New York City",
      portStops: "",
      endPort: "Manhattan, New York City",
      startDate: "Wed Jul 1, 2026",
      endDate: "Thu Jul 9, 2026",
      price: "$979",
      itinerary: {
        // day1:
        // day2:
      },
    },
  ];

  return (
    <div className="cruise-details">
      {/* <SummaryCard data={cruise} /> */}
      <Header />
      <BgImage />
      <Summary tripid={tripid}/>
      <h2 className="cruise-heading">Cruise Itinerary</h2>
      {/* <DayWiseCard tripdata={cruise} /> */}
      <ItineraryCard />
      {/* <Card data={cruise} /> */}
      <h2 className="cruise-heading">Activities Onboard</h2>
      <ActivityCard />
      <h2 className="cruise-heading">Dining Onboard</h2>
      <RestaurantCard />
    </div>
  );
};

export default CruiseDetails;
