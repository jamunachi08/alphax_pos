import React from "react";
import ReactDOM from "react-dom/client";
import { FrappeProvider } from "frappe-react-sdk";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <FrappeProvider>
      <App />
    </FrappeProvider>
  </React.StrictMode>
);
