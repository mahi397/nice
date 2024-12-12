import React, { useEffect, useState } from 'react';
import logo from '../assets/react.svg';
import '../style.css';
import './navbar.css';
import { Link, useNavigate } from 'react-router-dom';
import cruiselogo from '../assets/cruiselogo.png';
// import cruiselogo from '../assets/white-ship-2.png';
import { FaRegUserCircle } from "react-icons/fa";

const isLoggedIn = () => {
  return localStorage.getItem('token') ? true : false; // Check if token exists in localStorage
};

function Header() {
 const [isAuthenticated, setIsAuthenticated] = useState(false);
 const [dropdownOpen, setDropdownOpen] = useState(false); // To control the dropdown visibility
  
  const navigate = useNavigate();

  useEffect(() => {
    setIsAuthenticated(isLoggedIn());
  }, []);

  const handleLogout = async () => {
    try {
      // Perform logout on the server (optional for cleanup purposes)
      await axios.post('/nice/logout/'); // Add this endpoint in your Django backend for cleanup, if needed.
    } catch (error) {
      console.error('Error during logout:', error);
    }

    // Remove token from localStorage and update auth state
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    navigate('/');
  };

  const toggleDropdown = () => {
    setDropdownOpen((prevState) => !prevState); // Toggle the dropdown state
  };


  return (
    <nav>
        <img src={cruiselogo} className='nav--logo'></img>

        <ul className='nav--list'>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>Discover</li>
            <li>Services</li>
            <li>About Us</li>
            <li>Contact</li>
        </ul>

        <div className="navbar-links">
          {isAuthenticated ? (
            <div className="profile-dropdown" onClick={toggleDropdown}>
              <div className="profile-circle">
                <FaRegUserCircle size={30} />
              </div>
              {dropdownOpen && (
                <div className="dropdown-content">
                  <Link to="/nice/profile">My Profile</Link>
                  <button onClick={handleLogout}>Logout</button>
                </div>
              )}
            </div>
          ) : (
          <button className='nav--button'>
          <Link to="/nice/login" style={{ textDecoration: 'none', color: 'inherit' }}>
            Login/Register
          </Link>
        </button>
          )}
        </div>
        
    </nav>
  )
}

export default Header
