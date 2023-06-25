import React, { useState } from "react";
import PropTypes from "prop-types";
import "./Login.scss";
import Background from "../Background/Background";
import { ReactComponent as Icon } from "../../assets/icon2.svg";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

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
          <TextField
            className="email--input"
            id="outlined-basic"
            label="Email Address"
            variant="outlined"
            onChange={(e) => setUserName(e.target.value)}
          />
          <br />
          <TextField
            id="outlined-password-input"
            label="Password"
            type="password"
            autoComplete="current-password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <div>
            <br />
            <Button variant="contained" type="submit">
              Submit
            </Button>
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
