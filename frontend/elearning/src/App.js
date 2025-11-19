import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';

import Home from './pages/Home';
import About from './pages/About';
import Courses from './pages/Courses';
import Login from './pages/Login';

import ProtectedRoute from './ProtectedRoute';

function App() {
  return (
    <>
      <Header />

      <main style={{ minHeight: '80vh', padding: '20px' }}>
        <Routes>
          {/* 🔓 PUBLIC ROUTE */}
          <Route path="/login" element={<Login />} />

          {/* 🔒 EVERYTHING ELSE IS PROTECTED */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/about" element={<About />} />
                  <Route path="/courses" element={<Courses />} />

                  {/* Add more protected pages here */}
                </Routes>
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>

      <Footer />
    </>
  );
}

export default App;
