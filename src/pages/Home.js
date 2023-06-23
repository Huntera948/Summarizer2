import React from "react";
import "./App.css";

function App() {
  return (
    <div className="App">
      <body>
        <div className="main-container">
          <form>
            <h1 className="App-header">News Article Summarizer</h1>
            <textarea
              id="articleInput"
              rows="10"
              cols="50"
              placeholder="Enter the news article here..."
              onkeydown="summarize(event)"
            ></textarea>
            <br />
            <button>Summarize</button>
            <br />
            <h2>Summary:</h2>
            <p className="summaryResult"></p>
          </form>
        </div>
        <div className="background-container">
          <div className="background"></div>
        </div>
      </body>
    </div>
  );
}

export default App;
