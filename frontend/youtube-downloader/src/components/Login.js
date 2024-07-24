import {useState, useRef, useEffect, } from "react";

import axios from "../http/axios";

import getFormByObject from "../utils";
import useAuth from "../hooks/useAuth";
import {Link, useLocation, useNavigate} from "react-router-dom";



const LOGIN_URL = "auth/login/"

const Login = () => {
    const { auth, setAuth } = useAuth()

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";

    const userRef = useRef();
    const errRef = useRef();

    const [user, setUser] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        userRef.current.focus();
    }, [])

     useEffect(() => {
        setErrMsg('');
    }, [user, pwd])

    const handleSubmit = async (e) => {
        e.preventDefault();
        const dataForForm = {
                username: user,
                password: pwd
        }

        const form = getFormByObject(dataForForm)
        try {
            const response = await axios.post(LOGIN_URL,
               form,
                {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
                    withCredentials: true
                }
            );
            console.log(JSON.stringify(response?.data));
            //console.log(JSON.stringify(response));
            const accessToken = response?.data?.access_token;
            // const roles = response?.data?.roles;
            setAuth({ user, pwd, accessToken });

            console.log(`handleSubmit Login auth.accessToken = ${auth.accessToken}`)
            setUser('');
            setPwd('');

            navigate(from, { replace: true });
        } catch (err) {
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 400) {
                setErrMsg('Missing Username or Password');
            } else if (err.response?.status === 401) {
                setErrMsg('Unauthorized');
            } else {
                setErrMsg('Login Failed');
            }
            errRef.current.focus();
        }
    }
    return (
        <div className='relative w-screen h-screen text-white flex justify-center items-center bg-cover'>
             <div className="bg-slate-800 border border-slate-400 rounded-md p-8 shadow-lg backdrop-filter backdrop-blur-sm bg-opacity-30 relative">
                <p ref={errRef} className={errMsg ? "text-red-600" : "offscreen"} aria-live="assertive">{errMsg}</p>
                <h1 className="text-4xl text-white font-bold text-center mb-6">Login</h1>
                <form onSubmit={handleSubmit}>
                    <div className="relative my-4">
                        <input
                            id="username"
                            type="text"
                            className="block w-72 py-2.5 px-0 text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:text-white focus:border-blue-600 peer"
                            placeholder=""
                            ref={userRef}
                            onChange={(e) => setUser((e.target.value))}
                            required
                        />
                        <label
                            className="absolute text-sm text-white duration-300 transform -translate-y-6 left-0 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
                            htmlFor="username">
                            Your Username
                        </label>
                    </div>
                    <div className="relative my-4">
                        <input
                            type="password"
                            id="password"
                            className="block w-72 py-2.5 px-0 text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:text-white focus:border-blue-600 peer"
                            placeholder=""
                            value={pwd}
                            onChange={(e) => setPwd((e.target.value))}
                            required
                        />
                        <label htmlFor=""
                               className="absolute text-sm text-white duration-300 transform -translate-y-6 left-0 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">
                            Your Password
                        </label>
                    </div>
                    {/*<button className={"w-full mb-4 text-[18px] mt-6 rounded-full bg-violet-600 text-white hover:bg-gray-200 hover:text-black py-2 transition-colors duration-300"}>Login</button>*/}
                    <button className={"w-full h-18 mb-4 text-xl py-1 rounded-full bg-gradient-to-r bg-clip from-violet-500 to-fuchsia-500 animate-text"}>
                        <span className={"hover:text-black py-2 transition-colors duration-500"}>Login</span></button>
                </form>
                <p className={"relative text-xs right-20"}>
                    Need an Account?<br />
                    <span className="line">
                        {/*<Link to="/register" className={"hover:bg-gradient-to-r from-violet-500 to-fuchsia-500 transition: background-position 0.5s ease bg-clip-text hover:text-transparent animate-spin"}>Register</Link>*/}
                        <Link to="/register" className={""}>Register</Link>
                    </span>
                </p>
            </div>
        </div>
    )
}

export default Login