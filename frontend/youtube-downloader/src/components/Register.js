import {useState, useRef, useEffect} from "react";
import { IoCheckmark } from "react-icons/io5";
import { ImCross, ImInfo} from "react-icons/im";

import { IoEyeOutline, IoEyeOffOutline } from "react-icons/io5";
import axios from "../http/axios";
import getFormByObject from "../utils";

const USER_REGEX = /^[a-zA-Z][a-zA-Z0-9 -_]{3,23}$/;
const PWD_REGEX=/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;
const EMAIL_REGEX=/^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/;
const REGISTER_URL = "auth/register/"

const Register = () => {
    const userRef = useRef();
    const emailRef = useRef();
    const errRef = useRef();

    const [user, setUser] = useState('');
    const [validName, setValidName] = useState(false);
    const [userFocus, setUserFocus] = useState(false);

    const [email, setEmail] = useState('');
    const [validEmail, setValidEmail] = useState(false);
    const [emailFocus, setEmailFocus] = useState(false);

    const [pwd, setPwd] = useState('');
    const [validPwd, setValidPwd] = useState(false);
    const [pwdFocus, setPwdFocus] = useState(false);

    const [showPwd, setShowPwd] = useState(false)
    const [showMatchPwd, setShowMatchPwd] = useState(false)

    const [matchPwd, setMatchPwd] = useState('');
    const [validMatch, setValidMatch] = useState(false);
    const [matchFocus, setMatchFocus] = useState(false);

    const [errMsg, setErrMsg] = useState('');
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        const result = USER_REGEX.test(user)
        console.log(`result = ${result}\nuser = ${user}`)

        setValidName(result);
    }, [user])

    useEffect(() => {
        const result = EMAIL_REGEX.test(email)
        console.log(`result = ${result}\nuser = ${email}`)

        setValidEmail(result);
    }, [email])

    useEffect(() => {
        setValidPwd(PWD_REGEX.test(pwd));
        const result = pwd === matchPwd
        console.log(`pwd = ${pwd}\n validPwd = ${validPwd}\n
        matchPwd = ${matchPwd}\n
        validMatch = ${validMatch}`)
        setValidMatch(pwd === matchPwd);
        console.log(`pwd === matchPwd = ${result}`)
    }, [pwd, matchPwd])

    useEffect(() => {
        setErrMsg('');
    }, [user, email, pwd, matchPwd])

    const toggleShowPassword = () => {
        setShowPwd(!showPwd)
    }
    const toggleShowMatchPassword = () => {
        setShowMatchPwd(!showMatchPwd)
    }
    console.log("render")
    const handleSubmit = async (e) => {
        e.preventDefault()
        // if button enabled with JS hack
        const validateUser = USER_REGEX.test(user);
        const validatePwd = PWD_REGEX.test(pwd);
        const validateEmail = EMAIL_REGEX.test(email);
        if (!validateUser || !validatePwd || !validateEmail) {
            setErrMsg("Invalid Entry");
            return;
        }
        try {
            // const response = axios.get()
            const dataForForm = {
                username: user,
                password: pwd,
                email: email
            }
            const form = getFormByObject(dataForForm)
            console.log('form = ' + form)
            const response = await axios.post(REGISTER_URL,
                form,
                {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    withCredentials: true
                }
            );
            console.log(response?.data);
            console.log(response?.accessToken);
            console.log(JSON.stringify(response))
            setSuccess(true);
            //clear state and controlled inputs
            //need value attrib on inputs for this
            setUser('');
            setPwd('');
            setEmail('');
            setMatchPwd('');
        } catch (err) {
            console.log(err?.response)
            if (!err?.response) {
                setErrMsg('No Server Response');
            } else if (err.response?.status === 409) {
                setErrMsg('Username Taken');
            } else {
                setErrMsg('Registration Failed')
            }
            errRef.current.focus();
        }
    }
    return (
        <div className='relative w-screen h-screen text-white flex justify-center items-center bg-cover'>
        <div className="bg-slate-800 border border-slate-400 rounded-md p-8 shadow-lg backdrop-filter backdrop-blur-sm bg-opacity-30 relative">
            <p ref={errRef} className={errMsg ? "text-red-600" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <h1 className="text-4xl text-white font-bold text-center mb-6">Register</h1>
            <form onSubmit={handleSubmit}>
                <div className="relative my-4">
                    <input
                        id="username"
                        type="text"
                        className="block w-72 py-2.5 px-0 text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:text-white focus:border-blue-600 peer"
                        placeholder=""
                        ref={userRef}
                        autoComplete="off"
                        onChange={(e) => setUser((e.target.value))}
                        required
                        aria-invalid={validName ? "false" : "true"}
                        aria-describedby="uidnote"
                        onFocus={() => setUserFocus(true)}
                        onBlur={() => setUserFocus(true)}
                    />
                    <label
                        className="absolute text-sm text-white duration-300 transform -translate-y-6 left-0 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
                        htmlFor="username">
                        Your Username
                    </label>
                     <IoCheckmark className={`absolute top-3 right-1 text-green-500 w-5 h-5
                      ${validName ? "valid" : "hidden"}`}/>
                     <ImCross className={`absolute top-4 right-1 text-red-600 w-3 h-5"
                      ${validName || !user ? "hidden" : "invalid"}`}/>

                    <p id="uidnote" className={`right-1 text-xs flex relative bg-purple-500 border-slate-400 rounded-md p-2 m-1 shadow-lg backdrop-filter backdrop-blur-sm bg-opacity-30 
                    ${userFocus && user && !validName ? "" : "hidden"}`}>
                            <ImInfo className={"relative right-1 top-0.5"}/>
                            4 to 24 characters.<br/>
                            Must begin with a letter.<br/>
                            Letters, numbers, underscores, hyphens allowed.
                    </p>
                </div>

                <div className="relative my-4">
                    <input
                        type="email"
                        className="block w-72 py-2.5 px-0 text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:text-white focus:border-blue-600 peer"
                        placeholder=""
                        ref={emailRef}
                        autoComplete="off"
                        onChange={(e) => setEmail((e.target.value))}
                        required
                        aria-invalid={validEmail ? "false" : "true"}
                        aria-describedby="uidnote"
                        onFocus={() => setEmailFocus(true)}
                        onBlur={() => setEmailFocus(true)}
                    />
                    <label htmlFor=""
                           className="absolute text-sm text-white duration-300 transform -translate-y-6 left-0 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">
                        Your Email
                    </label>
                    <IoCheckmark className={`absolute top-3 right-1 text-green-500 w-5 h-5
                      ${validEmail ? "valid" : "hidden"}`}/>
                     <ImCross className={`absolute top-4 right-1 text-red-600 w-3 h-5"
                      ${validEmail || !email ? "hidden" : "invalid"}`}/>
                </div>
                <div className="relative my-4">
                    <input
                        type={showPwd ? 'text' : 'password'}
                        id="password"
                        className="block w-72 py-2.5 px-0 text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:text-white focus:border-blue-600 peer"
                        placeholder=""
                        value={pwd}
                        onChange={(e) => setPwd((e.target.value))}
                        required
                        aria-invalid={validPwd ? "false" : "true"}
                        aria-describedby="pwdnote"
                        onFocus={() => setPwdFocus(true)}
                        onBlur={() => setPwdFocus(false)}
                    />

                    <label htmlFor=""
                           className="absolute text-sm text-white duration-300 transform -translate-y-6 left-0 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">
                        Your Password
                    </label>

                    <IoCheckmark className={`absolute top-3 right-1 text-green-500 w-5 h-5
                      ${validPwd ? "valid" : "hidden"}`}/>
                    <ImCross className={`absolute top-4 right-1 text-red-600 w-3 h-5"
                      ${validPwd || !pwd ? "hidden" : "invalid"}`}/>
                    <button
                      type="button"
                      onClick={toggleShowPassword}
                      className="absolute top-4 right-6 text-gray-200">

                      {pwd ? showPwd ? <IoEyeOutline/> : <IoEyeOffOutline/> : null}
                    </button>
                    <p id="pwdnote" className={`right-1 text-xs flex relative bg-purple-500 border-slate-400 rounded-md p-2 m-1 shadow-lg backdrop-filter backdrop-blur-sm bg-opacity-30 
                    ${pwdFocus && !validPwd ? "" : "hidden"}`}>
                        <ImInfo className={"relative right-1 top-0.5"}/>
                        <span>
                            8 to 24 characters.<br/>
                            Must include uppercase and lowercase letters,<br/> a number and a special character.<br/>
                            Allowed special characters: ! @ # $ %
                        </span>
                    </p>
                </div>
                <div className="relative my-4">
                    <input
                        type={showMatchPwd ? 'text' : 'password'}
                        className="block w-72 py-2.5 px-0 text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:text-white focus:border-blue-600 peer"
                        placeholder=""
                        id="confirm_pwd"
                        onChange={(e) => setMatchPwd(e.target.value)}
                        value={matchPwd}
                        required
                        aria-invalid={validMatch ? "false" : "true"}
                        aria-describedby="confirmnote"
                        onFocus={() => setMatchFocus(true)}
                        onBlur={() => setMatchFocus(false)}
                    />
                    <label htmlFor="confirm_pwd" className="absolute text-sm text-white duration-300 transform -translate-y-6 left-0 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">
                        Confirm Your Password
                    </label>
                    <IoCheckmark className={`absolute top-3 right-1 text-green-500 w-5 h-5
                      ${validMatch && matchPwd ? "" : "hidden"}`}/>
                    <ImCross className={`absolute top-4 right-1 text-red-600 w-3 h-5"
                      ${validMatch || !matchPwd ? "hidden" : ""}`}/>
                    <button
                      type="button"
                      onClick={toggleShowMatchPassword}
                      className="absolute top-4 right-6 text-gray-200">

                      {matchPwd ? showMatchPwd ? <IoEyeOutline/> : <IoEyeOffOutline/> : null}
                    </button>
                    <p id="confirmnote" className={`right-1 text-xs flex relative bg-purple-500 border-slate-400 rounded-md p-2 m-1 shadow-lg backdrop-filter backdrop-blur-sm bg-opacity-30 
                    ${matchFocus && !validMatch ? "" : "hidden"}`}>
                        <ImInfo className={"relative right-1 top-0.5"}/>
                        Must match the first password input field.
                    </p>

                </div>
                <button disabled={!validName || !validEmail ||!validPwd || !validMatch}
                    className={"w-full mb-4 text-[18px] mt-6 rounded-full bg-violet-600 text-white disabled:bg-violet-400 disabled:hover:text-white hover:bg-gray-200 hover:text-black py-2 transition-colors duration-300"}>Register</button>
            </form>
        </div>
      </div>
    )
}

export default Register