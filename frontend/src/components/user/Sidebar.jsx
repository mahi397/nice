import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <ul>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/my-trips">My Trips</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/payment-history">Payment History</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
