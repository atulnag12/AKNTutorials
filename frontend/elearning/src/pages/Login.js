import React, { useState } from 'react';
import './Login.css';

function Login() {
  const [isLogin, setIsLogin] = useState(true);

  const toggleForm = () => setIsLogin(!isLogin);

  return (
    <div className="login-container">
      <h2 className="login-heading">
        {isLogin
          ? 'Access Your Courses – Login or Sign Up'
          : 'Join the Future of Learning with AKNTutorials'}
      </h2>

      <div className="login-card">
        <form>
          {!isLogin && (
            <>
              <label htmlFor="fullname">Full Name</label>
              <input type="text" id="fullname" placeholder="Enter your full name" />
            </>
          )}

          <label htmlFor="email">Email or Phone</label>
          <input type="text" id="email" placeholder="Enter email or phone number" />

          <label htmlFor="password">Password</label>
          <input type="password" id="password" placeholder="Enter your password" />

          {isLogin && (
            <div className="remember-me">
              <input type="checkbox" id="remember" />
              <label htmlFor="remember">Remember me</label>
            </div>
          )}

          <button type="submit" className="login-btn">
            {isLogin ? 'Login' : 'Sign Up'}
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

        <div className="login-footer">
          {isLogin ? (
            <>
              New to AKNTutorials?
              <span onClick={toggleForm} className="toggle-link"> Sign up</span>
            </>
          ) : (
            <>
              Already have an account?
              <span onClick={toggleForm} className="toggle-link"> Log in</span>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;
