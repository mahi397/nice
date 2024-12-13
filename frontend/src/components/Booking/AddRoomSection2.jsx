import React, { useState, useEffect } from "react";
import { FaMinus, FaPlus } from "react-icons/fa";
import axios from "axios";
import { getTripCapacityReserveURL } from "./booking_api";

const AddRoomSection = ({ rooms, setRooms }) => {
  const [bookingData, setBookingData] = useState(null);

  useEffect(() => {
    // Retrieve bookingData from sessionStorage
    const storedBookingData = sessionStorage.getItem("bookingData");
    if (storedBookingData) {
      setBookingData(JSON.parse(storedBookingData));
    }
    // console.log(storedBookingData);
  }, []);

  const addRoom = () => {
    if (rooms.length < 4) {
      setRooms([...rooms, { id: rooms.length + 1, guests: 1 }]);
    }
  };

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

  const handleConfirm = async () => {
    if (!bookingData) {
      console.error("No booking data available");
      return;
    }

    const tripid = bookingData.trip_details.tripid;
    const url = getTripCapacityReserveURL(tripid);

    const data = {
      rooms: rooms.map((room) => ({
        room_number: room.id,
        number_of_people: room.guests,
      })),
    };

    // console.log("Data to be sent: ", data);

    const token = localStorage.getItem("token"); // Assuming you have a token for authentication

    try {
      const response = await axios.patch(url, data, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      console.log("Patch sent successfully:", response.data);
    } catch (error) {
      console.error("Error sending patch:", error);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div style={styles.container} className="add-room-section">
        {/* <h2 style={{ marginTop: "50px" }}>ADD ROOMS</h2> */}
        <p style={{ marginBottom: "25px" }}>
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

            {/* Add/Remove Buttons Container */}
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
      <div style={styles.buttonContainer}>
        <button style={{ width: "40%" }} onClick={handleConfirm}>
          CONFIRM
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    // paddingTop: "20px"
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
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.2)",
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
  buttonContainer: {
    display: "flex",
    justifyContent: "center",
    marginTop: "20px", // Add some margin if needed
  },
};

export default AddRoomSection;
