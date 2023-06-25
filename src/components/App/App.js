import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.scss";
import Dashboard from "./Dashboard/Dashboard";
import Login from "../Login/Login";
import Preferences from "./Preferences/Preferences";
import useToken from "./useToken";
import Background from "../Background/Background";
import { ReactComponent as Icon } from "../../assets/icon2.svg";

function App() {
  const { token, setToken } = useToken();

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div className="wrapper">
      <h1>Summarizer</h1>
      <BrowserRouter>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/preferences" element={<Preferences />} />
        </Routes>
      </BrowserRouter>
      <Background />
    </div>
  );
}

export default App;
