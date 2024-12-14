import React from 'react';
import './booking.css'; // Assuming you have a CSS file for styling
import Header from '../Header';

const BookingSummary = ({ bookingDetails }) => {
  // const {
  //   referenceNumber,
  //   passengerName,
  //   tripName,
  //   startDate,
  //   endDate,
  //   totalGuests,
  //   stateroomType,
  //   totalPrice,
  //   paymentMethod,
  //   packagesIncluded,
  // } = bookingDetails;

const mockData = {
  referenceNumber: 'OEUR0976290',
  passengerName: 'John Doe',
  tripName: 'Dream Island Adventure',
  startDate: '2025-01-03',
  endDate: '2025-01-07',
  totalGuests: 2,
  stateroomType: ['Inside Stateroom', 'Studio Stateroom'],
  totalPrice: 2616.99,
  paymentMethod: 'Credit Card',
  packagesIncluded: ['Water and Non-Alcoholic', 'Unlimited Internet', 'Specialty Dining', 'Unlimited Bar', 'Internet 200 minutes, 100 GB'],
};


  return (
    <>
    <Header />
    <div className="booking-confirmation">
      <header className="booking-summary-header">
        <h1>Thank You for Your Booking!</h1>
        <p style={{fontSize: '20px', margin: '5px'}}>Your cruise adventure awaits!</p>
      </header>
<hr />
      <div className="booking-reference-section">
        <h2>Booking Reference</h2>
        <p className="reference-number">Your booking reference number is <strong>{mockData.referenceNumber}.</strong></p>
      </div>
<hr />
      <div className="booking-details-section">
        <h2>Booking Details</h2>
        <ul>
          <li><strong>Passenger Name:</strong> {mockData.passengerName}</li>
          <li><strong>Trip Name:</strong> {mockData.tripName}</li>
          <li><strong>Start Date:</strong> {mockData.startDate}</li>
          <li><strong>End Date:</strong> {mockData.endDate}</li>
          <li><strong>Total Guests:</strong> {mockData.totalGuests}</li>
          {/* <li><strong>Stateroom Type:</strong> {mockData.stateroomType.map(room => <span>{room} </span>)}</li> */}
        </ul>
      </div>
<hr />
      <div className="payment-summary-section">
        <h2>Payment Summary</h2>
        <ul>
          <li><strong>Total Price:</strong> ${mockData.totalPrice}</li>
          <li><strong>Payment Method:</strong> {mockData.paymentMethod}</li>
        </ul>
      </div>
<hr />
      <div className="packages-included-section">
        <h2>Packages Included</h2>
        {mockData.packagesIncluded.length > 0 ? (
          <ul>
            {mockData.packagesIncluded.map((pkg, index) => (
              <li key={index}>{pkg}</li>
            ))}
          </ul>
        ) : (
          <p>No additional packages included.</p>
        )}
      </div>
<br />
<hr/>
      <footer className="booking-summary-footer">
        <p>If you have any questions, feel free to contact our support team.</p>
        <button className="btn btn-primary" onClick={() => window.print()}>Print This Page</button>
      </footer>
    </div>
    </>

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
