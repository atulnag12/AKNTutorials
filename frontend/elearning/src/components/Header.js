import React from 'react';
import './Header.css';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="home-header">
      <nav className="home-navbar">
        <div className="home-left">
          <div className="home-logo">
            <Link to="/" style={{ textDecoration: 'none', color: '#00866c' }}>AKNTutorials</Link>
          </div>
          <ul className="home-menu">
            <li><Link to="/courses">Courses</Link></li>
            <li><Link to="/tutorials">Tutorials</Link></li>
            <li><Link to="/practice">Practice</Link></li>
            <li><Link to="/about">About</Link></li>
            <li><Link to="/login">Login/SignUp</Link></li>
          </ul>
        </div>
        <div className="home-search-wrapper">
          <input type="text" placeholder="Search..." className="home-search" />
        </div>
      </nav>
    </header>
  );
}

export default Header;
