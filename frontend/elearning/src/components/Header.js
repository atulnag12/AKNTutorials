import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => (
  <header className="header">
    <nav className="nav">
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      <Link to="/courses">Courses</Link>
      <Link to="/login">Login</Link>
    </nav>
  </header>
);

export default Header;