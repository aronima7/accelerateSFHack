import { createRoot } from "react-dom/client";
import { Chat } from "./app";
import { BrowserRouter, Route, Routes } from "react-router-dom";

const container = document.getElementById("root");
const root = createRoot(container!);
// const isLocalhost = window.location.hostname === "localhost";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Chat />} />
      </Routes>
    </BrowserRouter>
  );
};

root.render(<App />);
