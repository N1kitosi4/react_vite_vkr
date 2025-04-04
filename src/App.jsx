import "./styles/main.css";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import gitHub from "./img/icons/gitHub.svg"
// import gitHub_black from "./img/icons/gitHub-black.svg"

import NavBar from "./components/NavBar/NavBar";
import Footer from "./components/Footer/Footer";
import Home from "./pages/Home";
import MyReviews from "./pages/myreviews";
import Profile from "./pages/Profile";
import Review from "./pages/Review";

import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import Logout from "./pages/Auth/Logout";

import ScrollToTop from "./utils/ScrollToTop";
import ProtectedRoute from "./utils/ProtectedRoute";
import CreateReview from "./components/CreateReview/CreateReview";
import CreateBook from "./components/CreateBook/CreateBook";
import Recommendations from "./pages/Recommendations";
import NavBarLogin from "./components/NavBarLogin/NavBarLogin";

//import PrivateRoute from './utils/PrivateRoute';

function App() {
  return (
    <>
      <div className="App">
        <Router>
          <ScrollToTop />
          <NavBar />

          <Routes>
            <Route path="/" element={<Home />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/myreviews" element={<MyReviews />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/create-review" element={<CreateReview />} />
              <Route path="/create-book" element={<CreateBook />} />
              <Route path="/recommendations" element={<Recommendations />} />
            </Route>

            <Route path="/review/:id" element={<Review />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/logout" element={<Logout />} />
          </Routes>

          <Footer />
        </Router>
      </div>
    </>
  );
}

export default App;
