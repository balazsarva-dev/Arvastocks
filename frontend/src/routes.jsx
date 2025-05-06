import React, { lazy } from "react";

const HomePage = lazy(() => import("./components/others/Home"));
const News = lazy(() => import("./components/stocks/News"));
const AreaChart = lazy(() => import("./components/stocks/AreaChart"));
const LineChart = lazy(() => import("./components/stocks/LineChart"));
const CandlestickChart = lazy(() => import("./components/stocks/CandlestickChart"));
const Contact = lazy(() => import("./components/others/Contact"));
const About = lazy(() => import("./components/others/About"));
const Terms = lazy(() => import("./components/others/Terms"));
const Register = lazy(() => import("./components/users/Register"));
const Login = lazy(() => import("./components/users/Login"));
const Logout = lazy(() => import("./components/users/Logout"));
const Profile = lazy(() => import("./components/users/Profile"));
const ChangeEmail = lazy(() => import("./components/users/ChangeEmail"));
const ChangePassword = lazy(() => import("./components/users/ChangePassword"));
const Delete = lazy(() => import("./components/users/Delete"));

const routes = [
    { path: "/", element: <HomePage /> },
    { path: "/home", element: <HomePage /> },
    { path: "/news", element: <News /> },
    { path: "/area-chart", element: <AreaChart /> },
    { path: "/line-chart", element: <LineChart /> },
    { path: "/candlestick-chart", element: <CandlestickChart /> },
    { path: "/contact", element: <Contact /> },
    { path: "/about", element: <About /> },
    { path: "/terms", element: <Terms /> },
    { path: "/register", element: <Register /> },
    { path: "/login", element: <Login /> },
    { path: "/logout", element: <Logout /> },
    { path: "/profile", element: <Profile /> },
    { path: "/update_email", element: <ChangeEmail /> },
    { path: "/change_password", element: <ChangePassword /> },
    { path: "/delete_account", element: <Delete /> },
    // Add more routes as needed
];

export default routes;