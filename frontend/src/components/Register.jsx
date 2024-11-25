import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate(); // Using useNavigate instead of useHistory

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [email, setEmail] = useState("");
  const [fName, setFName] = useState("");
  const [lName, setLName] = useState("");
  const [errors, setErrors] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Frontend validation for username and password
    const validationErrors = [];
    if (username.length < 5)
      validationErrors.push("Username must be at least 5 characters long.");
    if (password.length < 8)
      validationErrors.push("Password must be at least 8 characters.");
    if (!/[A-Z]/.test(password))
      validationErrors.push(
        "Password must contain at least one uppercase letter."
      );
    if (!/[0-9]/.test(password))
      validationErrors.push("Password must contain at least one number.");
    if (password !== confirmPassword)
      validationErrors.push("Passwords do not match.");

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Send the registration request to the Django backend
    try {
      const response = await axios.post("http://localhost:8000/api/register/", {
        username,
        password,
      });
      if (response.status === 201) {
        navigate("/login"); // Use navigate instead of history.push
      }
    } catch (error) {
      setErrors([
        error.response.data.detail || "An error occurred during registration.",
      ]);
    }
  };

  return (
    <div className="container">
      <div className="wrapper">
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-box">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="input-box">
            <label>First Name:</label>
            <input
              type="text"
              value={fName}
              onChange={(e) => setFName(e.target.value)}
            />
          </div>
          <div className="input-box">
            <label>Last Name:</label>
            <input
              type="text"
              value={lName}
              onChange={(e) => setLName(e.target.value)}
            />
          </div>
          <div className="input-box">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          
          <div className="input-box">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="input-box">
            <label>Confirm Password:</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>
          <button type="submit">Register</button>
        </form>
        {errors.length > 0 && (
          <ul>
            {errors.map((error, idx) => (
              <li key={idx} style={{ color: "red" }}>
                {error}
              </li>
            ))}
          </ul>
        )}

        <p>
          Already registered?
          <br />
          <span className="line">
            <Link to="/login">Sign In</Link>
          </span>
        </p>
      </div>
    </div>
  );
};

export default Register;
