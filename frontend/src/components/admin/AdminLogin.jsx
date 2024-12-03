import React, { useState } from "react";
import axios from "axios";
import "./AdminLogin.css";
import { useNavigate } from "react-router-dom";

const AdminLogin = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    try {
      const response = await axios.post("http://localhost:8000/admin-login/", {
        username,
        password,
      });

      // Store token in localStorage
      localStorage.setItem("authToken", response.data.token);
      alert(response.data.message);

      // Redirect to the employee dashboard
      navigate("/admin-dashboard");
    } catch (error) {
      setErrorMessage(error.response.data.error || "An error occurred");
    }
  };

  return (
    <div className="container">
      <div className="wrapper">
        <h1>Admin Login</h1>
        <form onSubmit={handleLogin}>
          <div className="input-box">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-box">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default AdminLogin;
