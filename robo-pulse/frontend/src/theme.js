/*

Day 6 - React and Material UI theme
createTheme function is used to create custom themes for materialUI components.
We will be creating a light mode theme with specific primary and seconday colors, 
as well as custom border radius for components

*/

import { createTheme } from "@mui/material";

const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#0d47a1'
        },
        secondary: {
            main: '#ff6f00'
        },
        background: {
            default: '#579aff'
        }
    },
    shape: {
        borderRadius: 8, 
    }
    
});

export default theme;