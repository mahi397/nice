import React from 'react';
import TopSection from './TopSection';
import HeaderLoggedIn from '../HeaderLoggedIn';


export default function Booking() {
  return (
    <div className='room-list-container'>
      <HeaderLoggedIn />
      <TopSection />
      {/* <button style={{marginTop: '-30px'}}>CONTINUE</button> */}

      {/* <button>CONTINUE</button> */}
    </div>
  )
}
