import React, { useState } from "react";
import axios from "axios";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/nice/password-reset/", { email });
      setMessage("Password reset link has been sent to your email.");
    } catch (error) {
      setMessage("Error sending password reset link.");
    }
  };

  return (
    <div className="form-container">
      <div className="wrapper">
        <h2>Forgot Password</h2>
        <form onSubmit={handleForgotPassword}>
          <div className="input-box">
            <label>
              Email:
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
          </div>
          <button type="submit">Send Reset Link</button>
        </form>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
};

export default ForgotPassword;
