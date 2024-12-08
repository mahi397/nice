import React from 'react';
import bgImg from '../../assets/cover.png';

export default function BgImage() {
    console.log("BGImage rendered");
  return (
    <div style={style.imgContainer}>
      <img src={bgImg} style={style.img} />
    </div>
  )
}

const style = {
  imgContainer: {
    width: '100%',
    height: '470px',
    position: 'relative',
    overflow: 'hidden',
  },
  img: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  }
};
