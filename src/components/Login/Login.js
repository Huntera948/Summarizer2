import React, { useState } from "react";
import PropTypes from "prop-types";
import "./Login.scss";
import Background from "../Background/Background";
import { ReactComponent as Icon } from "../../assets/icon2.svg";

async function loginUser(credentials) {
  return fetch("http://localhost:8080/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  }).then((data) => data.json());
}

export default function Login({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = await loginUser({
      username,
      password,
    });
    setToken(token);
  };

  return (
    <div className="page--wrapper">
      <Icon className="icon" />
      <div className="login--wrapper">
        <h1>Welcome back</h1>
        <form onSubmit={handleSubmit}>
          <label>
            <p>Email Address</p>
            <input
              className="email--input"
              type="text"
              onChange={(e) => setUserName(e.target.value)}
            />
          </label>
          <label>
            <p>Password</p>
            <input
              className="password--input"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <div>
            <button type="submit">Submit</button>
          </div>
        </form>
        <Background />
      </div>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired,
};
