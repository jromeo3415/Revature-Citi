import { AppBar, Toolbar, Typography, Box, Button } from "@mui/material"
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing'

{/*
  
    Every React component must return a single element. In this case, we are
    returning an AppBar component from MaterialUI, which acts as a top-level naviagation bar
    that typically contains the application title and other navigation elements. The AppBar 
    is wrapped in a Toolbar component which provides the alignment for the child elements. 
    Inside the Toolbar we have a PrecisionManufacturingIcon component which is an icon component
    from MUI's icon library. 

*/}


// Day 7 - Added username, role, and onLogout to function params
function AppHeader({username, role, onLogout}) {
    return (
        <AppBar position="static">
            <Toolbar>

                <PrecisionManufacturingIcon sx={{ mr: 2}} />
                <Typography variant="h6" component="h1">
                    Robopulse Fleet Command Center
                </Typography>

                {/* Day 7 code here */}
                {username && (
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyItems: 'right', gap: 2}}>
                        
                        <Typography variant="body2">{username} ({role})</Typography>

                        <Button color="inherit" onClick={onLogout}>Log Out</Button>
                    </Box>
                )}
                {/* End day 7 here*/}
                
            </Toolbar>
        </AppBar>
    );
}

export default AppHeader;