import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const ResetPassword = () => {
  const { uidb64, token } = useParams();
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleResetPassword = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`/reset/${uidb64}/${token}/`, { password });
      setMessage('Password has been reset successfully.');
    } catch (error) {
      setMessage('Error resetting password.');
    }
  };

  return (
    <div className="form-container">
      <div className="wrapper">
      <h2>Reset Password</h2>
      <form onSubmit={handleResetPassword}>
      <div className="input-box">
          
        <label>
          New Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        </div>
          
        <button type="submit">Reset Password</button>
      </form>
      {message && <p>{message}</p>}
      </div>
    </div>
  );
};

export default ResetPassword;