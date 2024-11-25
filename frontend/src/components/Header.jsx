import { React, useState } from 'react';
import logo from '../assets/react.svg';
import '../style.css';
import { Link } from 'react-router-dom';

function Header() {

  // const [isModalVisible, setIsModalVisible] = useState(false);

  // const toggleModal = () => {
  //   setIsModalVisible(isModalVisible => !isModalVisible);
 // }

  return (
    <nav>
        <img src={logo} className='nav--logo'></img>
        <ul className='nav--list'>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>Discover</li>
            <li>Services</li>
            <li>About Us</li>
            <li>Contact</li>
        </ul>
        <button className='nav--button'>
          <Link to="/login" style={{ textDecoration: 'none', color: 'inherit' }}>
            Sign In
          </Link>
        </button>
    </nav>
  )
}

export default Header
