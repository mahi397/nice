import React, { useState } from 'react';

const packagesData = [
  { id: 1, title: 'Water and Non-Alcoholic', price: '$40/person/night' },
  { id: 2, title: 'Unlimited Bar (for adults 21+)', price: '$80/person/night' },
  { id: 3, title: 'Internet 200 minutes, 100 GB', price: '$150/person for entire trip' },
  { id: 4, title: 'Unlimited Internet', price: '$250/person for entire trip' },
  { id: 5, title: 'Specialty Dining (Italian, La-carte, Mexican, Japanese, Chinese)', price: '$60/person/night' },
];

const PackageSelection = () => {
  const [selectedPackages, setSelectedPackages] = useState([]);

  // Handles selecting and unselecting a package
  const togglePackageSelection = (packageId) => {
    setSelectedPackages((prevSelected) => 
      prevSelected.includes(packageId) 
        ? prevSelected.filter((id) => id !== packageId) 
        : [...prevSelected, packageId]
    );
  };

  const handleReviewBooking = () => {
    console.log('Selected Packages:', selectedPackages);
    // Pass this data to the next page or store it in context/state
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>Select Packages</h2>

      {packagesData.map((pkg) => (
        <div 
          key={pkg.id} 
          style={{
            ...styles.card, 
            backgroundColor: selectedPackages.includes(pkg.id) ? '#DFF6FF' : '#fff', 
            border: selectedPackages.includes(pkg.id) ? '2px solid #00BFFF' : '1px solid #ccc'
          }}
          onClick={() => togglePackageSelection(pkg.id)}
        >
          <h3 style={styles.packageTitle}>{pkg.title}</h3>
          <p style={styles.packagePrice}>{pkg.price}</p>
        </div>
      ))}

      <button 
        style={styles.reviewButton} 
        onClick={handleReviewBooking}
      >
        Review Booking
      </button>
    </div>
  );
};

const styles = {
  container: {
    width: '100%',
    maxWidth: '648px',
    margin: '0 auto',
    padding: '16px',
  },
  header: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '16px',
  },
  card: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    padding: '16px',
    marginBottom: '12px',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s ease-in-out',
  },
  packageTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '8px',
    marginTop: '0',
  },
  packagePrice: {
    fontSize: '16px',
    color: '#555',
  },
  reviewButton: {
    width: '100%',
    padding: '16px',
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: '#00BFFF',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  }
};

export default PackageSelection;
