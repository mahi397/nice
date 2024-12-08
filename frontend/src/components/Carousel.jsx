import React from "react";
import Slider from "react-slick";
import img1 from '../assets/cover.png';
import img2 from '../assets/cruisenyc.jpg';
import img3 from '../assets/nyc.jpg';
import img4 from '../assets/nyccruise.webp';
import './Carousel.css';

function Carousel() {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1
  };

  return (
    <div className="slider-container">
      <Slider {...settings}>
        <div>
          {/* <h3>1</h3> */}
          <img src={img1} alt="" />
        </div>
        <div>
          {/* <h3>2</h3> */}
          <img src={img2} alt="" />
        </div>
        <div>
          {/* <h3>3</h3> */}
          <img src={img3} alt="" />
        </div>
        <div>
          {/* <h3>4</h3> */}
          <img src={img4} alt="" />
        </div>
      </Slider>
    </div>
  );
}

export default Carousel;
