// src/App.js
import React, { useState } from "react";
import Sidebar from "./Sidebar";
import MainSection from "./MainSection";
import "./admin-styles.css";

function Dashboard() {
  const [selected, setSelected] = useState("overview");

  return (
    <div className="app">
      <Sidebar onSelect={setSelected} />
      <MainSection selected={selected} />
    </div>
  );
}

export default Dashboard;
