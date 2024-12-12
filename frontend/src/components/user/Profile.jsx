import React, { useEffect, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './profile.css';
import Header from '../Header';

const ProfilePage = () => {
  const [user, setUser] = useState({ completedBookings: [], upcomingBookings: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('/api/user-profile');
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      } finally {
        setLoading(false);
      }
    };

    // fetchUserData();
  }, []);

  const mockUser = {
    name: 'John Doe',
    email: 'abc@adc.com',
    phone: '1234567890',
    address: '123 Main St, City, Country',
    completedBookings: [
      { bookingId: 1, tripName: 'Trip 1', startDate: '2021-01-01', endDate: '2021-01-05', totalAmount: 500 },
      { bookingId: 2, tripName: 'Trip 2', startDate: '2021-02-01', endDate: '2021-02-05', totalAmount: 600 },
    ],
    upcomingBookings: [
      { bookingId: 3, tripName: 'Trip 3', startDate: '2021-03-01', endDate: '2021-03-05', totalAmount: 700 },
      { bookingId: 4, tripName: 'Trip 4', startDate: '2021-04-01', endDate: '2021-04-05', totalAmount: 800 },
    ],
  }

  const completedBookingColumns = [
    { headerName: 'Booking ID', field: 'bookingId' },
    { headerName: 'Trip Name', field: 'tripName' },
    { headerName: 'Start Date', field: 'startDate' },
    { headerName: 'End Date', field: 'endDate' },
    { headerName: 'Total Amount', field: 'totalAmount', valueFormatter: params => `$${params.value}` },
  ];

  const upcomingBookingColumns = [
    { headerName: 'Booking ID', field: 'bookingId' },
    { headerName: 'Trip Name', field: 'tripName' },
    { headerName: 'Start Date', field: 'startDate' },
    { headerName: 'End Date', field: 'endDate' },
    { headerName: 'Total Amount', field: 'totalAmount', valueFormatter: params => `$${params.value}` },
  ];

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
    <Header />
    <div className="profile-page">
      {/* User Basic Details */}
      <div className="user-details">
        <h2 className="section-title">My Profile</h2>
        <div className="user-info">
          <p><strong>Name:</strong> {mockUser.name}</p>
          <p><strong>Email:</strong> {mockUser.email}</p>
          <p><strong>Phone:</strong> {mockUser.phone}</p>
          <p><strong>Address:</strong> {mockUser.address}</p>
        </div>
      </div>
      
      {/* User Bookings */}
      <div className="user-bookings">
        <h2 className="section-title">My Bookings</h2>
        <div className="tabs">
          <button className="tab-button active" id="completed-tab">Completed</button>
          <button className="tab-button" id="upcoming-tab">Upcoming</button>
        </div>

        <div className="tab-content" id="completed-bookings">
          <h3>Completed Bookings</h3>
          <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
            <AgGridReact 
              rowData={mockUser.completedBookings} 
              columnDefs={completedBookingColumns} 
              defaultColDef={{ flex: 1, resizable: true }} 
            />
          </div>
        </div>

        <div className="tab-content hidden" id="upcoming-bookings">
          <h3>Upcoming Bookings</h3>
          <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
            <AgGridReact 
              rowData={mockUser.upcomingBookings} 
              columnDefs={upcomingBookingColumns} 
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

