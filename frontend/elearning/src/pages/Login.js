import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Hardcoded login check
    if (username === "atul" && password === "atul65023") {
      localStorage.setItem("auth", "true");
      navigate("/");    // Redirect after login
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-heading">Access Your Courses – Login</h2>

      <div className="login-card">
        <form onSubmit={handleSubmit}>
          <label htmlFor="email">Username</label>
          <input
            type="text"
            id="email"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && <p className="error-msg">{error}</p>}

          <button type="submit" className="login-btn">
            Login
          </button>

          <div className="divider">or</div>

          <button type="button" className="google-btn">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
              alt="Google Icon"
            />
            Continue with Google
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
