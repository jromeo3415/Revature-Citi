/**
 * Robopulse Command Center Day 7
 * Global auth state using React's context API
 */

import { createContext, useContext, useMemo, useState } from "react";
import apiClient from "../api/client";

// create a global React context which acts as a central store to hold 
// authentication state so any comonent can access it without 
// passing props down manually
const AuthContext = createContext(null);

// extracts and decodes the user payload from our JWT so that React
// can read it without calling the backend again
function decodeToken(token) {
    const payloadSegment = token.split('.')[1];
    return JSON.parse(atob(payloadSegment));
}

// AuthProvider is a component that wraps the application and manages authentication state
export function AuthProvider({children}) {

    // Initializing our token state from the browsers local storage to ensure a user 
    // stays logged in, even if they refresh the page. Allows us to read from storage
    // only once on initial render
    const [token, setToken] = useState(() => localStorage.getItem('roboPulseToken'));

    // Decode the JWT into a user object and cache the results and prevent redecoding the token
    // on every re-render. This only runs when the token actually changes.
    const user = useMemo(() => (token ? decodeToken(token) : null), [token]);

    // Authenticates the user credentials against the backend API by sending credentials,
    // saving the returned token token to localStorage and updates the React state
    const login = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await apiClient.post('/auth/token', formData, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        });

        localStorage.setItem('roboPulseToken', response.data.access_token);
        setToken(response.data.access_token);
    }

    // logout function clears the authentication session and reset the state to null
    const logout = () => {
        localStorage.removeItem('roboPulseToken');
        setToken(null);
    };

    // bundles all of our auth state variables and action functions into a single object
    // to define the exact interface exposed to components that are consuming this content
    const value = {token, user, isAuthenticated: Boolean(token), login, logout};

    // render the context provider that passes down the value object to make the auth state
    // and functions available to all nested child components
    return <AuthContext.Provider value={value}> {children} </AuthContext.Provider>;
}

// custom React hook that exposes the AuthContext to any component.
// this simplifies context usage in our child React components.
// (useAuth()) instead of useContext(AuthContext) and it throws an error is used outside of 
// the <AuthProvider>. This step does not have to be taken but you may encounter an error
export function useAuth() {
    const context = useContext(AuthContext);
    if (context === null) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    
    return context;
}