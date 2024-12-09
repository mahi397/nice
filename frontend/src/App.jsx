import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./style.css";
import Home from "./components/Home";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/user/Profile";

import Dashboard from "./components/user/Dashboard";

import AdminLogin from "./components/admin/AdminLogin";
import AdminDashboard from "./components/admin/AdminDashboard";
import ProtectedRoute from "./components/admin/ProtectedRoute";
import CruiseDetails from "./components/CruiseDetails/CruiseDetails";
import Booking from "./components/Booking/Booking";

import BookingSummary from "./components/Booking/BookingSummary";
import Checkout from './components/Booking/Checkout';

function App() {
  return (
    <>
      <div className="App">
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/nice/login" element={<Login />} />
            <Route path="/nice/register" element={<Register />} />
            <Route path="/nice/profile" element={<Profile />} />

            <Route path="/dashboard" element={<Dashboard />} />

            <Route path="/nice/admin/login" element={<AdminLogin />} />
            <Route
              path="/admin-dashboard"
              element={
                // <ProtectedRoute>
                <AdminDashboard />
                // </ProtectedRoute>
              }
            />

            {/* <Route path="/admin/dashboard" element={<AdminDash />} /> */}
            <Route path="/cruise-details" element={<CruiseDetails tripid={56}/>} />

            <Route path="/booking" element={<Booking />} />
            <Route path="/booking-summary" element={<BookingSummary />} />
            <Route path="/payment-page" element={<Checkout />}></Route>
          </Routes>
        </Router>
      </div>
    </>
  );
}

export default App;
