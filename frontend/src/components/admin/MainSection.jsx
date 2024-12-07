// src/components/Dashboard.js
import React, { useState, useEffect } from "react";
import EditableTable from "./EditableTable";
import { getEntity } from "./api.js";
import Overview from "./Overview";
import ManageShips from "./ManageShips.jsx";


const MainSection = ({ selected }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      let result = [];
      try {
        if(selected !== 'overview') {
            result = await getEntity(selected);
        }
        // if (selected === "users") {
        //   result = await getEntity("users");
        // } else if (selected === "trips") {
        //     result = await getEntity("trips");
        // } else if (selected === "ships") {
        //   result = await getShips();
        // } else if (selected === "ports") {
        //   result = await getPorts();
        // } else if (selected === "restaurants") {
        //   result = await getRestaurants();
        // } else if (selected === "activities") {
        //   result = await getActivities();
        // } else if (selected === "packages") {
        //     result = await getPackages();
        // }
        setData(result); // Update the state with fetched data
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false); // Set loading to false when API call is complete
      }
    };

    fetchData(); // Trigger the API call
  }, [selected]); // Re-run the effect whenever `selected` changes

  if (loading) {
    return <div>Loading...</div>; // Show loading indicator while data is being fetched
  }

  function displayContent(selected) {
    if(selected === 'overview') {
        return (
            <Overview />
        )
    } else if(selected === 'ships') {
        return (
            <ManageShips data={data}/>
        )
    }
     else {
        return (
            <EditableTable data={data} entity={selected} />
        )
    }
  }

  return (
    <div className="dashboard-content">
      <h1>{selected.charAt(0).toUpperCase() + selected.slice(1)}</h1>
      {displayContent(selected)}
    </div>
  );
};

export default MainSection;
