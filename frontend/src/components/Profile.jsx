import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const Profile = () => {
    const [profile, setProfile] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                // Redirect to login if no token is found
                navigate('/login');
                return;
            }

            try {
                const response = await axios.get('http://localhost:8000/api/profile/', {
                    headers: {
                        Authorization: `Token ${token}`,
                    },
                });
                setProfile(response.data);
            } catch (err) {
                setError('Unable to fetch profile data.');
            }
        };

        fetchProfile();
    }, [navigate]);

    if (error) return <div>{error}</div>;

    if (!profile) return <div>Loading...</div>;

    return (
        <div>
            <h2>My Profile</h2>
            <div>
                <h3>Contact Information</h3>
                <p><strong>Username:</strong> {profile.username}</p>
                <p><strong>Full Name:</strong> {profile.first_name} {profile.last_name}</p>
                <p><strong>Email:</strong> {profile.email}</p>
            </div>
            <div>
                <h3>Your Trips</h3>
                {profile.trips && profile.trips.length > 0 ? (
                    <ul>
                        {profile.trips.map((trip, index) => (
                            <li key={index}>
                                <strong>{trip.name}</strong> - {trip.destination} on {new Date(trip.date).toLocaleDateString()}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>You have no trips booked.</p>
                )}
            </div>
        </div>
    );
};

export default Profile;
