import React, { useState } from "react";
import { FaUser, FaLock } from "react-icons/fa";
import { Link } from "react-router-dom";

function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/api/auth/login/",
        formData
      );
      localStorage.setItem("accessToken", response.data.access); // Store token in localStorage
      alert("Login successful");
      // Redirect to dashboard or home page
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="container">
    
    <div className="wrapper">
      <form onSubmit={handleSubmit}>
        <h1>Login</h1>

        <div className="input-box">
          <input
            type="text"
            name="username"
            placeholder="Username"
            required
            onChange={handleChange}
          />
          <FaUser className="icon" />
        </div>

        <div className="input-box">
          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            onChange={handleChange}
          />
          <FaLock className="icon" />
        </div>

        {error && <p>{error}</p>}

        <div className="remember-forgot">
          <label htmlFor="">
            <input type="checkbox" />
            Remember me
          </label>
          <a href="#">Forgot Password?</a>
        </div>

        <button type="submit">Login</button>

        <div className="register-link">
          <p>
            Don't have an account? {' '}
            <Link to="/register">Register</Link>
          </p>
        </div>
      </form>
    </div>
    </div>
  );
}

export default Login;
