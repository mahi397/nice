import React from 'react'
import Header from '../Header'
import PassengerForm from './PassengerForm'
import './booking.css';

function AddPassengers() {
  return (
    <>
      <Header />
      <div className="add-passengers-container">
        <PassengerForm />
      </div>
    </>
  )
}

export default AddPassengers
