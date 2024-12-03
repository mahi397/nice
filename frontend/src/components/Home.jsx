import React from 'react'
import Header from './Header'
import Main from './Main'
import Trips from './Trips'

export default function Home() {
  return (
    <>
    <Header />
    <div className="container">
      <Main />
      {/* <Trips /> */}
    </div>
    </>
    
  )
}
