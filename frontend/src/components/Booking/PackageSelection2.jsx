import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const packagesData = [
  {
    packageid: 4,
    package_details: {
      description: "$40/person/night",
      package_name: "Water and Non-Alcoholic",
      price: 40,
    },
  },
  {
    packageid: 5,
    package_details: {
      description: "$80/person/night (for adults age over 21)",
      package_name: "Unlimited Bar",
      price: 80,
    },
  },
  {
    packageid: 6,
    package_details: {
      description: "$150/person for entire trip",
      package_name: "Internet 200 minutes, 100 GB",
      price: 150,
    },
  },
  {
    packageid: 7,
    package_details: {
      description: "$250/person for entire trip",
      package_name: "Unlimited Internet",
      price: 250,
    },
  },
  {
    packageid: 8,
    package_details: {
      description: "$60/person/night (Italian, La-carte, Mexican, Japanese, Chinese)",
      package_name: "Specialty Dining",
      price: 60,
    },
  },
  ];  


  // }"Water and Non-Alcoholic", price: "$40/person/night" },
  // { id: 2, title: "Unlimited Bar (for adults 21+)", price: "$80/person/night" },
  // {
  //   id: 3,
  //   title: "Internet 200 minutes, 100 GB",
  //   price: "$150/person for entire trip",
  // },
  // { id: 4, title: "Unlimited Internet", price: "$250/person for entire trip" },
  // {
  //   id: 5,
  //   title: "Specialty Dining (Italian, La-carte, Mexican, Japanese, Chinese)",
  //   price: "$60/person/night",
  // },


const PackageSelection2 = ({ guestIndex, onPackageSelect, pkg}) => {
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

  // Handles selecting and unselecting a package
  // const togglePackageSelection = (packageId) => {
  //   setSelectedPackages((prevSelected) =>
  //     prevSelected.includes(packageId)
  //       ? prevSelected.filter((id) => id !== packageId)
  //       : [...prevSelected, packageId]
  //   );
  // };
  // const togglePackageSelection = (pkg) => {
  //   setSelectedPackages((prevSelected) =>
  //     prevSelected.includes(pkg.package_id)
  //       ? prevSelected.filter((id) => id !== pkg.package_id)
  //       : [...prevSelected, pkg.package_id]
  //   );
  //   onPackageSelect(guestIndex, pkg.package_id, pkg.name);
  // };
  // const togglePackageSelection = (pkg) => {
  //   setSelectedPackages((prevSelectedPackages) => {
  //     if (prevSelectedPackages.includes(pkg.package_id)) {
  //       // Deselect package
  //       return prevSelectedPackages.filter((id) => id !== pkg.package_id);
  //     } else {
  //       // Select package
  //       return [...prevSelectedPackages, pkg.package_id];
  //     }
  //   });
  // };

  const togglePackageSelection = (packageId) => {
    setSelectedPackages((prevSelected) => 
      prevSelected.includes(packageId) 
        ? prevSelected.filter((id) => id !== packageId) 
        : [...prevSelected, packageId]
    );
  };

  // useEffect(() => {
  //   // Call onPackageSelect whenever selectedPackages changes
  //   onPackageSelect(guestIndex, selectedPackages);
  // }, [selectedPackages, guestIndex, onPackageSelect]);

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Select Packages for Guest {guestIndex + 1}</h2>

      {packagesData.map((pkg) => (
        <div
          key={pkg.package_id}
          style={{
            ...styles.card,
            backgroundColor: selectedPackages.includes(pkg.packageid)
              ? "#DFF6FF"
              : "#fff",
            border: selectedPackages.includes(pkg.packageid)
              ? "2px solid #00BFFF"
              : "1px solid #ccc",
          }}
          onClick={() => togglePackageSelection(pkg.packageid)}
        >
          <h3 style={styles.packageTitle}>{pkg.package_details.package_name}</h3>
          <p style={styles.packagePrice}>${pkg.package_details.price}</p>
        </div>
      ))}

      {/* <button style={styles.reviewButton}>
        <Link to={"/addpassengers"}>CONTINUE</Link>
      </button> */}
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
    // backgroundColor: '#00BFFF',
    backgroundColor: "rgb(16, 85, 154)",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
};

export default PackageSelection2;
