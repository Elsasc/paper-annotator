import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.js";
import { BrowserRouter as Router, Routes, Route } from 'react-router';


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Router>
    <Routes>
      <Route path="/*" element={<App />} />
    </Routes>
    </Router>
  </React.StrictMode>
);