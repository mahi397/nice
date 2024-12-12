import React from 'react';
import './booking.css'; // Assuming you have a CSS file for styling

const BookingSummary = ({ bookingDetails }) => {
  const {
    referenceNumber,
    passengerName,
    tripName,
    startDate,
    endDate,
    totalGuests,
    stateroomType,
    totalPrice,
    paymentMethod,
    packagesIncluded,
  } = bookingDetails;

  return (
    <div className="booking-summary-container">
      <header className="booking-summary-header">
        <h1>Thank You for Your Booking!</h1>
        <p>Your cruise adventure awaits!</p>
      </header>

      <section className="booking-reference-section">
        <h2>Booking Reference</h2>
        <p className="reference-number">{referenceNumber}</p>
      </section>

      <section className="booking-details-section">
        <h2>Booking Details</h2>
        <ul>
          <li><strong>Passenger Name:</strong> {passengerName}</li>
          <li><strong>Trip Name:</strong> {tripName}</li>
          <li><strong>Start Date:</strong> {startDate}</li>
          <li><strong>End Date:</strong> {endDate}</li>
          <li><strong>Total Guests:</strong> {totalGuests}</li>
          <li><strong>Stateroom Type:</strong> {stateroomType}</li>
        </ul>
      </section>

      <section className="payment-summary-section">
        <h2>Payment Summary</h2>
        <ul>
          <li><strong>Total Price:</strong> ${totalPrice}</li>
          <li><strong>Payment Method:</strong> {paymentMethod}</li>
        </ul>
      </section>

      <section className="packages-included-section">
        <h2>Packages Included</h2>
        {packagesIncluded.length > 0 ? (
          <ul>
            {packagesIncluded.map((pkg, index) => (
              <li key={index}>{pkg}</li>
            ))}
          </ul>
        ) : (
          <p>No additional packages included.</p>
        )}
      </section>

      <footer className="booking-summary-footer">
        <p>If you have any questions, feel free to contact our support team.</p>
        <button className="btn btn-primary" onClick={() => window.print()}>Print This Page</button>
      </footer>
    </div>
  );
};

export default BookingSummary;

// Sample Usage
// import BookingSummary from './BookingSummary';
// 
// const sampleBookingDetails = {
//   referenceNumber: 'ABC123456',
//   passengerName: 'John Doe',
//   tripName: 'Caribbean Explorer',
//   startDate: '2024-12-25',
//   endDate: '2025-01-01',
//   totalGuests: 4,
//   stateroomType: 'Ocean View Suite',
//   totalPrice: 3599.99,
//   paymentMethod: 'Credit Card',
//   packagesIncluded: ['Water and Non-Alcoholic Package', 'Unlimited Internet Package'],
// };
// 
// <BookingSummary bookingDetails={sampleBookingDetails} />
