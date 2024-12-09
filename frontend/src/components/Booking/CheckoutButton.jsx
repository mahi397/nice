import React from "react";
import { Link } from "react-router-dom";
// import './styles/CheckoutButton.css';

const CheckoutButton = () => {
  
  return (
    <Link to="/payment-page">
      <button
        className="checkout-button"
      >
        Checkout
      </button>
    </Link>
  );
};

export default CheckoutButton;
