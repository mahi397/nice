import React from "react";
import CheckoutButton from "./CheckoutButton";

const PaymentSummaryCard = () => {
  const leftHeading = 'Dream Island Adventure';
  const leftParagraph1 = 'Los Angeles  >  Adelaide  >  Dubai  > New York';
  const leftParagraph2 = 'Fri Jan 3, 2025 - Tue Jan 7, 2025';

  return (
    <div className="payment-summary-card">
      <h3>{leftHeading}</h3>
      <p>{leftParagraph2}</p>
      <h3 style={{fontSize: '20px', color: 'rgb(16, 85, 154)'}}>2 Rooms 2 Guests</h3>
      <h3>Add-on Packages: </h3>
      <ul>
        <li>Water & Non-alcoholic x2</li>
        <li>Unlimited Bar x1</li>
        <li>Internet 200 minutes, 100 GB x1</li>
        <li>Unlimited Internet x1</li>
        <li>Specialty Dining x1</li>
      </ul>
      <hr />
      <h2 style={{fontFamily: 'Bebas Neue', fontSize: '35px', marginTop: '20px'}}>PAYMENT SUMMARY</h2>
      {/* <div className="text-section"> */}
      <div style={styles.paymentsummary}>
        <div style={styles.paymentKeys}>
          {/* <p>Room 1:</p> */}
          <p>Guest Total:</p>
          <p>Add-ons Total:</p>
          
          <p>Taxes:</p>
          <h3>Total price (inclusive of taxes):</h3>
        </div>
        <div style={styles.paymentValues}>
          {/* <p>$1,900.00</p> */}
          <p>$1200.00</p>
          <p>$980.00</p>
          <p>$436.99</p>
          <h3>$2,616.99</h3>
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
    height: '100%',
    
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
