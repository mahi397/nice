import React from 'react'

function RoomSummaryBar({rooms}) {

  const totalGuests = rooms.reduce((total, room) => total + room.guests, 0);

  return (
    <div className="room-summary-bar">
      {/* Top section containing the trip info, rooms, and guests */}
      <div style={styles.topSection}>
        {/* Section 1: Trip Name and Dates */}
        <div style={styles.section}>
          <h4 style={styles.tripName}>8-Day The Bahamas</h4>
          <p style={styles.tripDates}>Wed Jul 1, 2026 - Thu Jul 9, 2026</p>
        </div>

        {/* Section 2: Number of Selected Rooms */}
        <div style={styles.section}>
          <h4 style={styles.countLabel}>Selected Rooms</h4>
          <p style={styles.countValue}>{rooms.length}</p>
        </div>

        {/* Section 3: Number of Selected Guests */}
        <div style={styles.section}>
          <h4 style={styles.countLabel}>Total Guests</h4>
          <p style={styles.countValue}>{totalGuests}</p>
        </div>
      </div>  
    </div>
  )
}

const styles = {
    container: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      paddingTop: "20px",
    },
    topSection: {
      height: "92px",
      width: "100vw",
      backgroundColor: "#f0f0f0",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-around",
      borderBottom: "2px solid #ddd",
    },
    topOfCard: {
      height: "70%",
      display: "flex",
    },
    leftSection: {
      width: "50%",
      padding: "16px",
      display: "flex",
      alignItems: "center",
      justifyContent: "center", // aligns text left
      borderRight: "1px solid #ddd",
    },
    rightSection: {
      width: "50%",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
    },
    roomLabel: {
      width: "50%",
      fontSize: "16px",
      fontWeight: "bold",
      display: "flex",
      alignItems: "center",
    },
    section: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
    },
    tripName: {
      fontSize: "16px",
      fontWeight: "bold",
    },
    tripDates: {
      fontSize: "14px",
      color: "#555",
    },
    countLabel: {
      fontSize: "14px",
      fontWeight: "bold",
    },
    countValue: {
      fontSize: "24px",
      fontWeight: "bold",
      color: "#007bff",
    },
    roomCard: {
      width: "648px",
      height: "135px",
      backgroundColor: "#fff",
      borderRadius: "8px",
      boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      marginBottom: "16px",
      padding: "16px",
    },
    roomTitle: {
      fontSize: "16px",
      fontWeight: "bold",
    },
    counterContainer: {
      display: "flex",
      alignItems: "center",
      margin: "10px 0",
    },
    counterButton: {
      // backgroundColor: "#007bff",
      color: "#fff",
      border: "none",
      borderRadius: "50%",
      width: "32px",
      height: "32px",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      cursor: "pointer",
      margin: "0 8px",
      transition: "background-color 0.3s",
    },
    disabledButton: {
      backgroundColor: "#ddd",
      // cursor: "not-allowed",
    },
    guestCount: {
      fontSize: "20px",
      fontWeight: "bold",
      textAlign: "center",
    },
    guestLabel: {
      fontSize: "12px",
      textAlign: "center",
      color: "#555",
    },
    roomActions: {
      display: "flex",
      justifyContent: "space-between",
    },
    bottomSection: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "0 16px",
      height: "30%",
    },
    removeButton: {
      backgroundColor: "#ff4d4f",
      color: "#fff",
      border: "none",
      padding: "8px 16px",
      borderRadius: "4px",
      cursor: "pointer",
    },
    addRoomButton: {
      // backgroundColor: "#007bff", //bright blue
      backgroundColor: "#28a745",
      color: "#fff",
      border: "none",
      padding: "8px 16px",
      borderRadius: "4px",
      cursor: "pointer",
    },
  };
  

export default RoomSummaryBar
