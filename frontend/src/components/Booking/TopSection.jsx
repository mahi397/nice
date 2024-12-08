/** This is the Add Room page */
import React, { useState } from "react";
import { FaMinus, FaPlus } from "react-icons/fa";
import RoomCategoryCard from "./RoomCategoryCard";
import RoomLocCard from "./RoomLocCard";
import RoomCategorySection from "./RoomCategorySection";
import RoomLocationSection from "./RoomLocationSection";
import RoomNumberSection from "./RoomNumberSection";
import PackageSelection from "./PackageSelection";

const App = () => {
  // State to track rooms and guests for each room
  const [rooms, setRooms] = useState([
    { id: 1, guests: 2 }, // Initial room with 2 guests
  ]);

    // Function to add a new room
  const addRoom = () => {
    if (rooms.length < 4) {
      setRooms([...rooms, { id: rooms.length + 1, guests: 1 }]);
    }
  };

  // Function to remove a room
  const removeRoom = (roomId) => {
    if (rooms.length > 1) {
      const updatedRooms = rooms.filter((room) => room.id !== roomId);
      setRooms(updatedRooms.map((room, index) => ({ ...room, id: index + 1 }))); // Reset room numbering
    }
  };

  // Function to update the guest count for a specific room
  const updateGuestCount = (roomId, increment) => {
    setRooms((prevRooms) =>
      prevRooms.map((room) =>
        room.id === roomId
          ? {
              ...room,
              guests: Math.min(4, Math.max(1, room.guests + increment)),
            }
          : room
      )
    );
  };

  // Calculate total number of guests
  const totalGuests = rooms.reduce((total, room) => total + room.guests, 0);

  return (
    <div className="room-list-container">
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

      {/* Room Cards */}
      <div style={styles.container} className="add-room-section">
        <h2 style={{ marginTop: "50px" }}>ADD ROOMS</h2>
        <p style={{ marginBottom: "20px" }}>
          You can add up to 3 rooms and up to 4 guests per room
        </p>
        {rooms.map((room) => (
          <div key={room.id} style={styles.roomCard}>
            {/* Top Section */}
            <div style={styles.topOfCard}>
              <div style={styles.leftSection}>
                <h3 style={styles.roomLabel}>Room {room.id}</h3>
              </div>

              <div style={styles.rightSection}>
                <button
                  onClick={() => updateGuestCount(room.id, -1)}
                  disabled={room.guests === 1}
                  style={{
                    ...styles.counterButton,
                    ...(room.guests === 1
                      ? styles.disabledButton
                      : { backgroundColor: "rgb(16, 85, 154)" }),
                  }}
                >
                  <FaMinus />
                </button>
                <span style={styles.guestCount}>{room.guests}</span>
                <span style={styles.guestLabel}>&nbsp;guests</span>

                <button
                  onClick={() => updateGuestCount(room.id, 1)}
                  disabled={room.guests === 4}
                  style={{
                    ...styles.counterButton,
                    ...(room.guests === 4
                      ? styles.disabledButton
                      : { backgroundColor: "rgb(16, 85, 154)" }),
                  }}
                >
                  <FaPlus />
                </button>
              </div>
            </div>

            {/* Bottom Section */}
            <div style={styles.bottomSection}>
              {rooms.length > 1 && (
                <button
                  onClick={() => removeRoom(room.id)}
                  style={styles.removeButton}
                >
                  Remove
                </button>
              )}
              {rooms.length < 3 && (
                <button onClick={addRoom} style={styles.addRoomButton}>
                  Add Room
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Room Category Section */}
      {/* <div className="room-category-section">
        <h2 style={{ marginTop: "50px" }}>Select Room Category</h2>
        {categories.map((category) => (
          <div key={category.id}>
            <RoomCategoryCard category={category} />
          </div>
        ))}
      </div> */}
      <RoomCategorySection />

      {/* Location Section */}
      <RoomLocationSection />

      <RoomNumberSection />

      <PackageSelection />
    </div>
  );
};

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

export default App;
