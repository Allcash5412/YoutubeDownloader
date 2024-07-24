import '../App.css';
import React from "react";
import { Routes, Route } from 'react-router-dom';
import Layout from "./LayOut"
import Register from "./Register"
import Login from "./Login"
import Home from "./Home"
import backgroundImage from '../assets/backgroundImage.png';
import Missing from "./Missing";
import Unauthorized from "./Unauthorized";
import RequireAuth from "./RequireAuth";
import Profile from "./Profile";


export default function App() {
      document.body.className = "h-14 bg-gradient-to-r from-blue-500 via-orange-200 to-amber-200"
      return (
          <Routes>
              <Route path={"/"} element={<Layout/>}>

                {/* public routes */}
                <Route path="login" element={<Login />} />
                <Route path="register" element={<Register />} />
                {/*<Route path="linkpage" element={<LinkPage />} />*/}
                <Route path="unauthorized" element={<Unauthorized />} />
                <Route path="/" element={<Home />} />

                {/* we want to protect these routes */}
                <Route element={<RequireAuth  />}>
                <Route path="profile" element={<Profile/>} />
                </Route>
                <Route path="*" element={<Missing />} />
              </Route>
          </Routes>
          )
}

