import React from 'react';
import './card.css';

const Card = ({item}) => {
    // console.log("CARDPROPS", image, headline, subheading, description);
    console.log(item);
    // console.log(props.item.image);
  return (
    <div className="card">
      <div className="card-image">
        <img src={item.image} alt="Card" />
      </div>
      <div className="card-content">
        <h2 className="headline">{item.headline}</h2>
        <h4 className="subheading">{item.subheading}</h4>
        <p className="description">{item.description}</p>
      </div>
    </div>
  );
};

export default Card;
