import React, { useState } from "react";
import axios from "axios";
import "../../style.css";
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
      const response = await axios.post("http://localhost:8000/nice/admin/login", {
        username,
        password,
      });

      // Log the entire response to inspect it
      console.log("Response from server:", response);

      // Check if access token is present in response
      if (response.data.access) {
        // Store access and refresh tokens in localStorage
        localStorage.setItem("authToken", response.data.access);
        localStorage.setItem("refreshToken", response.data.refresh);
        console.log("Access token set in localStorage:", response.data.access);

        // Redirect to the employee dashboard
        navigate("/admin-dashboard");
      } else {
        console.error("Access token not found in response");
      }
    } catch (error) {
      setErrorMessage(error.response.data.error || "An error occurred");
      console.error("Error during login:", error);
    }
  };

  return (
    <div className="form-container">
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
