import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import { Card, Row, Col, Spin, Alert } from 'antd';
import Card from './Card';
import { API_URL } from '../admin/api';

const { Meta } = Card;

const DayWiseCard = ({tripdata}) => {
  const [data, setData] = useState(tripdata);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fallback data in case of API error
  const fallbackData = [
    {
      headline: 'Default Headline 1',
      subheading: 'Default Subheading 1',
      description: 'Fallback description in case of an error.',
      image: 'https://via.placeholder.com/300',
    },
    {
      headline: 'Default Headline 2',
      subheading: 'Default Subheading 2',
      description: 'Fallback description in case of an error.',
      image: 'https://via.placeholder.com/300',
    },
  ];

  // Fetch data from your Django API using axios
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await axios.get(`${API_URL}/trips/list/${tripid}`);
  //       setData(response.data);  // Assuming response.data is an array
  //     } catch (error) {
  //       console.error('Error:', error);
  //       setError('Error fetching data');
  //       setData(fallbackData);  // Use fallback data if API call fails
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchData();
  // }, []);

  // if (loading) {
  //   return <Spin size="large" />;
  // }

  if (error) {
    return (
      <Alert
        message="Error"
        description="There was an issue fetching data from the API."
        type="error"
        showIcon
      />
    );
  }

  return (
    // <Row gutter={[16, 16]}>
    //   {data.map((item, index) => (
    //     <Col span={12} key={index}>
    //       <Card
    //         hoverable
    //         style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', height: '200px' }}
    //       >
    //         {/* Image on the left */}
    //         <div style={{ flex: '0 0 50%', padding: '8px' }}>
    //           <img
    //             alt="Card"
    //             src={item.image}
    //             style={{
    //               width: '100%',
    //               height: '100%',
    //               objectFit: 'cover',
    //               borderRadius: '8px',
    //             }}
    //           />
    //         </div>

    //         {/* Text on the right */}
    //         <div style={{ padding: '16px' }}>
    //           <h3>{item.headline}</h3>
    //           <h4>{item.subheading}</h4>
    //           <p>{item.description}</p>
    //         </div>
    //       </Card>
    //     </Col>
    //   ))}
    // </Row>
    <>
      {tripdata.map((item, idx) => (
        console.log("DWCARDITEM",item),
        <Card item={item}/>
      )
      )}
    </>
  );
};

export default DayWiseCard;
