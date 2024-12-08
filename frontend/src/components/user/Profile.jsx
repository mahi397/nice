// src/pages/Profile.js
import React, { useEffect, useState } from 'react';
import axios from '../../axios'; // Import the Axios instance

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/profile/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`, // Pass the token in Authorization header
          },
        });
        setProfileData(response.data);
      } catch (error) {
        setError('Failed to load profile data');
        console.error('Profile fetch error:', error);
      }
    };

    fetchProfile();
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>My Profile</h2>
      {profileData ? (
        <div>
          <p>Username: {profileData.username}</p>
          <p>Email: {profileData.email}</p>
        </div>
      ) : (
        <div>Loading profile...</div>
      )}
    </div>
  );
};

export default Profile;
