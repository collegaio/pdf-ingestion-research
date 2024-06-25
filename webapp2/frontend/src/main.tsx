import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { Helmet } from "react-helmet";
// import './index.css'

// initialScale: 1,
//   width: 'device-width',
//   viewportFit: 'cover',

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Helmet>
      <title>Collega</title>
      <meta
        name="viewport"
        content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover, user-scalable=no"
      />
    </Helmet>

    <App />
  </React.StrictMode>,
);
