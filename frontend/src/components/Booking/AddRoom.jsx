import React, { useState } from 'react';
import { FaMinus, FaPlus } from 'react-icons/fa'; // For - and + icons

const Card = ({ roomNumber, onRemove, onAdd, cardCount, guestCount, onGuestCountChange }) => {

  // Function to handle the decrement
  const decrement = () => {
    if (guestCount > 1) {
      onGuestCountChange(guestCount - 1);
    }
  };

  // Function to handle the increment
  const increment = () => {
    if (guestCount < 4) {
      onGuestCountChange(guestCount + 1);
    }
  };

  return (
    <div style={styles.card}>
      {/* Top Section (70% of height) */}
      <div style={styles.topSection}>
        {/* Left Section */}
        <div style={styles.leftSection}>
          <h3>{`Room ${roomNumber}`}</h3>
        </div>

        {/* Right Section (Counter) */}
        <div style={styles.rightSection}>
          <button
            style={{
              ...styles.counterButton,
              backgroundColor: guestCount === 1 ? '#ddd' : 'rgb(16, 85, 154)', // Grey out if disabled
            }}
            onClick={decrement}
            disabled={guestCount === 1}
          >
            <FaMinus />
          </button>
          <span style={styles.count}>{guestCount}</span>
          <span style={styles.guests}>&nbsp;guests</span>
          <button
            style={{
              ...styles.counterButton,
              backgroundColor: guestCount === 4 ? '#ddd' : 'rgb(16, 85, 154)', // Grey out if disabled
            }}
            onClick={increment}
            disabled={guestCount === 4}
          >
            <FaPlus />
          </button>
        </div>
      </div>

      {/* Bottom Section (30% of height) */}
      <div style={styles.bottomSection}>
        {/* Conditional rendering based on the number of cards */}
        {cardCount === 1 && (
          <button style={styles.addRoomButton} onClick={onAdd}>
            Add Room
          </button>
        )}
        {cardCount > 1 && cardCount < 3 && (
          <>
            <button style={styles.removeButton} onClick={onRemove}>
              Remove
            </button>
            <button style={styles.addRoomButton} onClick={onAdd}>
              Add Room
            </button>
          </>
        )}
        {cardCount === 3 && (
          <button style={styles.removeButton} onClick={onRemove}>
            Remove
          </button>
        )}
      </div>
    </div>
  );
};

const styles = {
  card: {
    width: '648px',
    height: '135px',
    borderRadius: '8px',
    backgroundColor: '#f4f4f9',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    marginBottom: '16px',
    padding: '16px',
  },
  topSection: {
    height: '70%',
    display: 'flex',
  },
  leftSection: {
    width: '50%',
    padding: '16px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center', // aligns text left
    borderRight: '1px solid #ddd',
  },
  rightSection: {
    width: '50%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  },
  counterButton: {
    // padding: '8px',
    fontSize: '18px',
    color: 'white',
    border: 'none',
    borderRadius: '50%',
    height: '40px',
    width: '40px',
    cursor: 'pointer',
    margin: '0 8px',
    transition: 'background-color 0.3s',
  },
  count: {
    fontSize: '20px',
    fontWeight: 'bold',
  },
  guests: {
    fontSize: '12px',
    color: '#555',
  },
  bottomSection: {
    height: '30%',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0 16px',
  },
  removeButton: {
    padding: '8px 16px',
    backgroundColor: '#ff4d4d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  addRoomButton: {
    padding: '8px 16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
};

export default Card;
