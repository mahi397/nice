import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();  // Using useNavigate instead of useHistory

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/api/login/', {
                username,
                password,
            });

            if (response.status === 200) {
                localStorage.setItem('token', response.data.token);  // Save token in local storage
                navigate('/');  // Redirect to home page after login
            }
        } catch (err) {
            setError("Invalid username or password");
        }
    };

    return (
      <div className="container">
        
        <div className='wrapper'>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className='input-box'>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className='input-box'>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit">Login</button>

                <div className="register-link">
          <p>
            Don't have an account? {' '}
            <Link to="/register">Register</Link>
          </p>
        </div>
            </form>
            {error && <div style={{ color: 'red' }}>{error}</div>}
        </div>
        </div>
    );
};

export default Login;
