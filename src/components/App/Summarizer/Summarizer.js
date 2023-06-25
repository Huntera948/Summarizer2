import React, { useState } from "react";
import NewsComponent from "../../API/newsAPI";

function Summarizer() {
  const [showNewsComponent, setShowNewsComponent] = useState(false);
  function toggleNewsComponent() {
    setShowNewsComponent((prevState) => !prevState);
  }

  return (
    <div className="wrapper">
      <button onClick={toggleNewsComponent}>Get Latest Headlines</button>
      {showNewsComponent && <NewsComponent />}
    </div>
  );
}

export default Summarizer;
