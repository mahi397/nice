import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./style.css";
import Home from "./components/Home";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/user/Profile";

import Dashboard from "./components/user/Dashboard";

import AdminLogin from "./components/admin/AdminLogin";
import AdminDashboard from "./components/admin/AdminDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import CruiseDetails from "./components/CruiseDetails/CruiseDetails";
import Booking from "./components/Booking/Booking";
import Booking2 from "./components/Booking/Booking2";

import AddPassengers from "./components/Booking/AddPassengers";
import ReviewBooking from "./components/Booking/ReviewBooking";
import Checkout from './components/Booking/Checkout';
import BookingSummary from "./components/Booking/BookingSummary";
import ForgotPassword from "./components/ForgotPassword";
import ResetPassword from "./components/ResetPassword";


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
            <Route path="/cruisedetails/:tripid" element={<CruiseDetails/>} />

            {/* <Route path="/booking" element={<Booking />} /> */}
            <Route path="/booking" element={<ProtectedRoute element={Booking2} />} />
            <Route path="/addpassengers" element={<AddPassengers />} />
            <Route path="/reviewbooking" element={<ReviewBooking />} />
            <Route path="/payment-page" element={<Checkout />}></Route>
            <Route path="/bookingsummary" element={<BookingSummary />}></Route>
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset/:uidb64/:token" element={<ResetPassword />} />
          
          </Routes>
        </Router>
      </div>
    </>
  );
}

export default App;
