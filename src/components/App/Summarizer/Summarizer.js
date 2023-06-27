import React, { useState } from "react";
import NewsComponent from "../../API/newsAPI";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Sidebar from "../Sidebar/Sidebar";
import "./Summarizer.scss";
import { ReactComponent as Icon } from "../../../assets/icon2.svg";

function Summarizer() {
  const [showNewsComponent, setShowNewsComponent] = useState(false);
  const [inputText, setInputText] = useState(""); // State to store the user input

  function toggleNewsComponent() {
    setShowNewsComponent((prevState) => !prevState);
  }

  function handleInputChange(event) {
    setInputText(event.target.value); // Update the inputText state with the user's input
  }

  return (
    <div className="page--container">
      <Sidebar />
      <h1 className="header">Summarizer</h1>
      <h2 className="sub--header">Summarize today's news about...</h2>
      <form className="summarizer--container">
        <TextField
          fullWidth
          placeholder="Bitcoin..."
          value={inputText} // Bind the value of the TextField to the inputText state
          onChange={handleInputChange} // Call handleInputChange on every change
        />
        <br />
        <Button className="go--button" onClick={toggleNewsComponent} variant="contained">
          Go!
        </Button>
        {showNewsComponent && <NewsComponent inputText={inputText} />}
        <Icon className="icon" />
      </form>
    </div>
  );
}

export default Summarizer;
