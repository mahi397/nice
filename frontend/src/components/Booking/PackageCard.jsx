// GPT's PS2
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const PackageSelection2 = ({ guestIndex, onPackageSelect }) => {
  const [selectedPackages, setSelectedPackages] = useState([]);
  const [bookingData, setBookingData] = useState(null);
  const [availablePackages, setAvailablePackages] = useState([]);

  useEffect(() => {
    const storedBookingData = sessionStorage.getItem("bookingData");
    if (storedBookingData) {
      const parsedBookingData = JSON.parse(storedBookingData);
      setBookingData(parsedBookingData);
      setAvailablePackages(parsedBookingData.available_packages);
    }
  }, []);

  const togglePackageSelection = (pkg) => {
    setSelectedPackages((prevSelected) =>
      prevSelected.includes(pkg.package_id)
        ? prevSelected.filter((id) => id !== pkg.package_id)
        : [...prevSelected, pkg.package_id]
    );
    onPackageSelect(guestIndex, pkg.package_id, pkg.name);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Select Package Add-ons</h2>

      {availablePackages.map((pkg) => (
        <div
          key={pkg.package_id}
          style={{
            ...styles.card,
            backgroundColor: selectedPackages.includes(pkg.package_id)
              ? "#DFF6FF"
              : "#fff",
            border: selectedPackages.includes(pkg.package_id)
              ? "2px solid #00BFFF"
              : "1px solid #ccc",
          }}
          onClick={() => togglePackageSelection(pkg)}
        >
          <h3 style={styles.packageTitle}>{pkg.name}</h3>
          <p style={styles.packagePrice}>{pkg.price}</p>
        </div>
      ))}

      <button style={styles.reviewButton}>
        <Link to={"/reviewbooking"}> Continue</Link>
      </button>
    </div>
  );
};

const styles = {
  container: {
    width: "100%",
    maxWidth: "648px",
    margin: "0 auto",
    padding: "16px",
  },
  header: {
    fontSize: "24px",
    fontWeight: "bold",
    marginBottom: "16px",
  },
  card: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    padding: "16px",
    marginBottom: "12px",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "all 0.2s ease-in-out",
  },
  packageTitle: {
    fontSize: "18px",
    fontWeight: "bold",
    marginBottom: "8px",
    marginTop: "0",
  },
  packagePrice: {
    fontSize: "16px",
    color: "#555",
  },
  reviewButton: {
    width: "100%",
    padding: "16px",
    fontSize: "18px",
    fontWeight: "bold",
    color: "#fff",
    backgroundColor: "rgb(16, 85, 154)",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
};

export default PackageSelection2;
