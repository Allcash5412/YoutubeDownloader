// src/icons/CheckIcon.jsx
import React from 'react';

const CheckIcon = (position) => {
    return (
    <svg className={`w-6 h-6 text-green-500 ${position.toString()}`} aria-hidden="true"
         xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" strokeOpacity="4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
              d="M5 11.917 9.724 16.5 19 7.5"/>
    </svg>
    )
};

export default CheckIcon;
