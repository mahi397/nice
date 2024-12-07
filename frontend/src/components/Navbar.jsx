// src/components/Navbar.js
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from '../axios'; // Import axios instance

// Dummy function to check if the user is logged in
const isLoggedIn = () => {
  return localStorage.getItem('token') ? true : false; // Check if token exists in localStorage
};

const Navbar = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate(); // useNavigate replaces useHistory

  useEffect(() => {
    setIsAuthenticated(isLoggedIn());
  }, []);

  const handleLogout = async () => {
    try {
      // Perform logout on the server (optional for cleanup purposes)
      await axios.post('/api/logout/'); // Add this endpoint in your Django backend for cleanup, if needed.
    } catch (error) {
      console.error('Error during logout:', error);
    }

    // Remove token from localStorage and update auth state
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    navigate('/login'); // Navigate to login page
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          MySite
        </Link>

        <div className="navbar-links">
          {isAuthenticated ? (
            <div className="profile-dropdown">
              <div className="profile-circle">
                {/* Display user profile image or initials */}
              </div>
              <div className="dropdown-content">
                <Link to="/profile">My Profile</Link>
                <button onClick={handleLogout}>Logout</button>
              </div>
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
