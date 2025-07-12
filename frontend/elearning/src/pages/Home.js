import React from 'react';
import './Home.css';
import { FaSearch } from 'react-icons/fa';

const Home = () => {
  return (
    <div className="landing-container">
      <h1>Hello, What Do You Want To Learn?</h1>

      <div className="search-bar">
        <input type="text" placeholder="Data" />
        <button><FaSearch /></button>
      </div>

      <div className="course-buttons">
        <button className="outlined">Full Stack Live Classes</button>
        <button className="outlined">DSA: Basic To Advanced Course</button>
        <button className="outlined">Master DS & ML</button>
      </div>
    </div>
  );
};

export default Home;
