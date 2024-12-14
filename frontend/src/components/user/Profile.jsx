import React, { useEffect, useState } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import "./profile.css";
import Header from "../Header";

const ProfilePage = () => {
  const [user, setUser] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
    completedBookings: [],
    upcomingBookings: [],
  });
  // const [loading, setLoading] = useState(true);
  const [completedBookings, setCompletedBookings] = useState([]);
  const [upcomingBookings, setUpcomingBookings] = useState([]);

  useEffect(() => {
    // const fetchUserData = async () => {
    //   try {
    //     const response = await fetch('/api/user-profile');
    //     const data = await response.json();
    //     setUser(data);
    //   } catch (error) {
    //     console.error('Error fetching user data:', error);
    //   } finally {
    //     setLoading(false);
    //   }
    // };

    // fetchUserData();
    setUser(mockUser);
    setCompletedBookings(mockUser.completedBookings);
    setUpcomingBookings(mockUser.upcomingBookings);
  }, []);

  const mockUser = {
    name: "Mahima Sachdeva",
    email: "ms15532@nyu.edu",
    phone: "1234567890",
    // address: "123 Main St, Jersey City, NJ, USA",
    completedBookings: [
      {
        bookingId: 24,
        tripName: "Caribbean Adventure",
        startDate: "2024-10-01",
        endDate: "2024-10-05",
        totalAmount: 1500.89,
      },
      {
        bookingId: 25,
        tripName: "Tropical Escape",
        startDate: "2023-12-31",
        endDate: "2024-01-05",
        totalAmount: 2600.98,
      },
      {
        bookingId: 35,
        tripName: "Behold Bermuda",
        startDate: "2023-03-01",
        endDate: "2023-03-05",
        totalAmount: 2700.09,
      },
      {
        bookingId: 14,
        tripName: "Mystic Shores",
        startDate: "2024-04-01",
        endDate: "2024-04-05",
        totalAmount: 1800.99,
      },
    ],
    upcomingBookings: [
      {
        bookingId: 34,
        tripName: "Dream Island Adventure",
        startDate: "2025-01-03",
        endDate: "2025-01-07",
        totalAmount: 2616.99,
      },
      
    ],
  };

  const completedBookingColumns = [
    { headerName: "Booking ID", field: "bookingId" },
    { headerName: "Trip Name", field: "tripName" },
    { headerName: "Start Date", field: "startDate" },
    { headerName: "End Date", field: "endDate" },
    {
      headerName: "Total Amount",
      field: "totalAmount",
      valueFormatter: (params) => `$${params.value}`,
    },
  ];

  const upcomingBookingColumns = [
    { headerName: "Booking ID", field: "bookingId" },
    { headerName: "Trip Name", field: "tripName" },
    { headerName: "Start Date", field: "startDate" },
    { headerName: "End Date", field: "endDate" },
    {
      headerName: "Total Amount",
      field: "totalAmount",
      valueFormatter: (params) => `$${params.value}`,
    },
  ];

  // if (loading) {
  //   return <div>Loading...</div>;
  // }

  return (
    <>
      <Header />
      <div className="profile-page">
        {/* User Basic Details */}
        <div className="user-details">
          <h2 className="section-title">My Profile</h2>
          <div className="user-info">
            <p>
              <strong>Name:</strong> {mockUser.name}
            </p>
            <p>
              <strong>Email:</strong> {mockUser.email}
            </p>
            <p>
              <strong>Phone:</strong> {mockUser.phone}
            </p>
            <p>
              <strong>Address:</strong> {mockUser.address}
            </p>
          </div>
        </div>

        {/* User Bookings */}
        <div className="user-bookings">
          <h2 className="section-title">My Bookings</h2>
          {/* <div className="tabs">
            <button className="tab-button active" id="completed-tab">
              Completed
            </button>
            <button className="tab-button" id="upcoming-tab">
              Upcoming
            </button>
          </div>

          <div className="tab-content" id="completed-bookings">
            <h3>Completed Bookings</h3>
            <div
              className="ag-theme-alpine"
              style={{ height: 400, width: "100%" }}
            >
              <AgGridReact
                rowData={user.completedBookings}
                columnDefs={completedBookingColumns}
                defaultColDef={{ flex: 1, resizable: true }}
              />
            </div>
          </div>

          <div className="tab-content hidden" id="upcoming-bookings">
            <h3>Upcoming Bookings</h3>
            <div
              className="ag-theme-alpine"
              style={{ height: 400, width: "100%" }}
            >
              <AgGridReact
                rowData={user.upcomingBookings}
                columnDefs={upcomingBookingColumns}
                defaultColDef={{ flex: 1, resizable: true }}
              />
            </div>
          </div> */}
          <div>
            <h3>Upcoming Bookings</h3>
            <br />
            <div
              className="ag-theme-alpine"
              style={{ height: 100, width: "100%" }}
            >
              <AgGridReact
                rowData={upcomingBookings}
                columnDefs={upcomingBookingColumns}
                defaultColDef={{ flex: 1, resizable: true }}
              />
            </div>
          </div>
          <hr />
          <div>
            <h3>Completed Bookings</h3>
            <br />
            <div
              className="ag-theme-alpine"
              style={{ height: 250, width: "100%" }}
            >
              <AgGridReact
                rowData={completedBookings}
                columnDefs={completedBookingColumns}
                defaultColDef={{ flex: 1, resizable: true }}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProfilePage;
