import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './style.css';
import Home from './components/Home'
import Login from './components/Login';
import Register from './components/Register';
import Profile from './components/Profile';

function App() {
  
  return (
    <>
      <div className='App'>
          <Router>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path='/login' element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </Router>
      </div>
    </>
  )
}

export default App
