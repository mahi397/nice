import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ element: Component, ...rest }) => {
  const isAuthenticated = !!localStorage.getItem('token'); // Check if the user is authenticated
  const location = useLocation();

  return isAuthenticated ? (
    <Component {...rest} />
  ) : (
    <Navigate to="/nice/login" state={{ from: location }} />
  );
};

export default ProtectedRoute;
