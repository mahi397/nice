// src/components/Overview.js
import React, { useRef, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import { Pie } from "react-chartjs-2";
import "./Overview.css"; // Create custom CSS to style the overview page
import { Chart as ChartJS, registerables } from 'chart.js';

// Register chart.js components (required for Chart.js 3.x)
ChartJS.register(...registerables);


const Overview = () => {
  const chartRef = useRef(null);

  // Example data for charts and stats
  const bookingData = {
    labels: ["January", "February", "March", "April", "May"],
    datasets: [
      {
        label: "Bookings",
        data: [200, 300, 250, 400, 350],
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const revenueData = {
    labels: ["January", "February", "March", "April", "May"],
    datasets: [
      {
        label: "Revenue",
        data: [50000, 70000, 60000, 80000, 75000],
        backgroundColor: "rgba(255, 159, 64, 0.2)",
        borderColor: "rgba(255, 159, 64, 1)",
        borderWidth: 1,
      },
    ],
  };

  const shipStatusData = {
    labels: ["Available", "Booked", "Maintenance"],
    datasets: [
      {
        data: [10, 5, 2],
        backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
        hoverBackgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"],
      },
    ],
  };

  useEffect(() => {
    // Cleanup chart instance when component is unmounted or data changes
    if (chartRef.current) {
      // Accessing the chart instance and destroy it if it exists
      const chartInstance = chartRef.current.chartInstance;
      if (chartInstance) {
        chartInstance.destroy();
      }
    }
  }, [bookingData, revenueData, shipStatusData]);  // Re-run effect if the data changes (or any other dependencies)


  return (
    <div className="overview-container">
      {/* <h1>Admin Dashboard - Overview</h1> */}
      <div className="overview-stats">
        <div className="stat-card">
          <h3>Total Trips</h3>
          <p>50</p>
        </div>
        <div className="stat-card">
          <h3>Total Bookings</h3>
          <p>1200</p>
        </div>
        <div className="stat-card">
          <h3>Total Revenue</h3>
          <p>$150,000</p>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart">
          <h3>Bookings Trend</h3>
          <Bar data={bookingData} ref={chartRef}
 />
        </div>
        <div className="chart">
          <h3>Revenue Trend</h3>
          <Bar data={revenueData} ref={chartRef} />
        </div>
        <div className="chart">
          <h3>Ship Availability</h3>
          <Pie data={shipStatusData} ref={chartRef} />
        </div>
      </div>

      <div className="recent-activities">
        <h3>Recent Activities</h3>
        <table>
          <thead>
            <tr>
              <th>Activity</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Booking - John Doe</td>
              <td>December 2, 2024</td>
            </tr>
            <tr>
              <td>User Sign-Up - Sarah Lee</td>
              <td>December 1, 2024</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Overview;
