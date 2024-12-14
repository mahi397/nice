import React from "react";
import manhImg from "../../assets/manhattan.avif";
import bahamas from '../../assets/bahamas.webp';
import la from '../../assets/la.webp';
import dubai from '../../assets/dubai.jpg';
import aus from '../../assets/aus.avif';

const ItineraryCard = ({cruise}) => {
  const mockText1 = (
    <>
      <strong>Day 1: Los Angeles, California</strong>
      <br />
      <strong>Departs at 12:00 PM</strong>
      <br />
      <br />
      Begin your adventure in the bustling Port of Los Angeles, the largest port in the United States. 
      Nestled in the heart of Southern California, this vibrant city offers a unique blend of sun, sea, and urban excitement. 
      Explore the iconic landmarks such as the Hollywood Walk of Fame, Griffith Observatory, and the Getty Center. 
      Stroll along the famous Santa Monica Pier or relax on the sandy beaches of Malibu. 
      Los Angeles is a melting pot of cultures, offering a diverse culinary scene, world-class shopping, and endless entertainment options. 
    </>
  );

  const mockText2 = (
    <>
      <strong>Day 2: Adelaide</strong>
      <br />
      <strong>9:00 AM - 5:30 PM</strong>
      <br />
      <br />
      Discover the charm of Adelaide, the coastal capital of South Australia. Known for its vibrant arts scene, world-class wineries, and stunning beaches, Adelaide offers a perfect blend of culture and relaxation. 
      Visit the Adelaide Central Market, one of the largest fresh produce markets in the Southern Hemisphere, and indulge in the local flavors. 
      Whether you're a foodie, a nature lover, or a culture enthusiast, Adelaide has something for everyone.
    </>
  );

  const mockText3 = (
    <>
      <strong>Day 3: Dubai</strong>
      <br />
      <strong>12:00 AM - 2:00 PM</strong>
      <br />
      <br />
      Experience the opulence and grandeur of Dubai, a city that epitomizes luxury and innovation. 
      Known for its futuristic architecture, world-class shopping, and vibrant nightlife, Dubai offers an unparalleled travel experience. 
      Visit the iconic Burj Khalifa, the tallest building in the world, and enjoy breathtaking views from its observation deck. 
      Relax on the pristine beaches of Jumeirah or embark on a desert safari for an adventure of a lifetime. 
      Dubai is a city of contrasts, where tradition meets modernity, offering something for every traveler.
    </>
  );

  const mockText4 = (
    <>
      <strong>Day 4: New York</strong>
      <br />
      <strong>7:00 AM - 7:00 PM</strong>
      <br />
      <br />
      End your cruise at the city that defined 'cosmopolitan': New
      York City. This urban island overflows with art and architecture, lively
      ethnic neighborhoods, designer shops... and the best restaurants in the
      world, from the ultra-high-end to the comfy neighborhood hole-in-the-wall.
      As your cruise leaving from New York glides down the Hudson River towards
      sunny islands or historic New England harbors, you'll pass metropolitan
      must-sees, world-renowned icons like the Empire State Building and the
      Statue of Liberty.
    </>
  );


  return (
    <>
      <div style={styles.card}>
        <img
          src={la} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <p>{mockText1}</p>
        </div>
      </div>
      <div style={styles.card}>
        <img
          src={aus}
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <p>{mockText2}</p>
        </div>
      </div>
      <div style={styles.card}>
        <img
          src={dubai} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <p>{mockText3}</p>
        </div>
      </div>
      <div style={styles.card}>
        <img
          src={manhImg} // Placeholder image URL
          alt="Card Image"
          style={styles.image}
        />
        <div style={styles.textContent}>
          <p>{mockText4}</p>
        </div>
      </div>      
    </>
  );
};

const styles = {
  card: {
    display: "flex",
    width: "90%", // Takes up 90% of the screen width
    height: "300px",
    borderRadius: "16px", // Rounded corners
    overflow: "hidden", // Ensures no content overflows outside the card
    backgroundColor: "#f4f4f9", // Light background color
    margin: "30px auto", // Centered with a top-bottom margin
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)", // Subtle shadow for a nice 3D effect
  },
  image: {
    width: "50%", // Left half for the image
    height: "100%",
    objectFit: "cover", // Ensures the image covers its container
    // borderRadius: '16px 0 0 16px', // Rounded corners only on the left
  },
  textContent: {
    width: "50%", // Right half for the text
    padding: "20px", // Padding for some breathing room
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "justify",
    fontSize: "16px",
    color: "#333", // Darker color for readability
    marginTop: "20px",
    marginBottom: "20px",
  },
};

export default ItineraryCard;
