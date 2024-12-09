import React from "react";
import CheckoutButton from "./CheckoutButton";

const PaymentSummaryCard = () => {
  return (
    <div className="payment-summary-card">
      <h3>8-Day The Bahamas from Manhattan, NYC</h3>
      <p>Wed Jul 1, 2026 - Thu Jul 9, 2026</p>
      <h3 style={{fontSize: '20px', color: 'rgb(16, 85, 154)'}}>1 Room 2 Guests</h3>
      <h3>Add-on Packages: </h3>
      <ul>
        <li>Water & Non-alcoholic</li>
        <li>Unlimited Bar</li>
        <li>Internet 200</li>
      </ul>
      <hr />
      <h2 style={{fontFamily: 'Bebas Neue', fontSize: '35px', marginTop: '20px'}}>PAYMENT SUMMARY</h2>
      {/* <div className="text-section"> */}
      <div style={styles.paymentsummary}>
        <div style={styles.paymentKeys}>
          <p>Room 1:</p>
          <p>Guest Total:</p>
          <p>Add-ons Total:</p>
          
          <p>Taxes:</p>
          <h3>Total:</h3>
        </div>
        <div style={styles.paymentValues}>
          <p>$1,900.00</p>
          <p>$15,200.00</p>
          <p>$1,980.00</p>
          <p>$1,009.99</p>
          <h3>$18,189.99</h3>
        </div>
      
      </div>
      <CheckoutButton />
    </div>
  );
};

const styles = {
  paymentsummary: {
    display: "flex",
    justifyContent: "space-between",
    width: '100%',
    height: '50%',
    
  },
  paymentKeys: {
    fontSize: "16px",
    color: "#555",
  },
  paymentValues: {
    fontSize: "16px",
    color: "#555",
    fontWeight: "bold",
    textAlign: "right",
  },
};

export default PaymentSummaryCard;
