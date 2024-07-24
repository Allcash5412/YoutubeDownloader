import { useState, useEffect } from "react";
import useAxiosPrivate from "../hooks/useAxiosPrivate";
import { useNavigate, useLocation } from "react-router-dom";

const Profile = () => {
    const [profile, setProfile] = useState();
    const axiosPrivate = useAxiosPrivate();
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        let isMounted = true;
        const controller = new AbortController();

        const getProfile = async () => {
            try {
                const response = await axiosPrivate.get('user/profile/', {
                    signal: controller.signal
                });
                console.log(`getProfile response.data = ${response.data}`);
                isMounted && setProfile(response.data);
            } catch (err) {
                console.log(`getProfile catch (err) = ${err}`);
                console.error(err);
                navigate('/login', { state: { from: location }, replace: true });
            }
        }

        getProfile();

        return () => {
            isMounted = false;
            controller.abort();
        }
    }, [])

    return (
        <div>
            Profile
            <div>
                Username {profile?.username}
            </div>
        </div>
    );
};


export default Profile;