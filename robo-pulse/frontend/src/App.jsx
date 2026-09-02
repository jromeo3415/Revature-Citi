import { Container, Typography, Box, Snackbar, Alert } from "@mui/material";
import { useState } from "react";
import AppHeader from "./components/layout/AppHeader";
import LoginForm from "./components/auth/LoginForm";
import RobotDataGrid from "./components/robots/RobotDataGrid";
import { AuthProvider, useAuth } from "./context/AuthContext";
import DiscrepancyDataGrid from "./components/missions/DiscrepancyDataGrid";

// main dashboard component that renders the application header and robot data grid
// to authenticated users
function Dashboard() {
    
    // stores the current user object and the logout function from the global auth context
    const{user, logout} = useAuth()
    const[notification, setNotification] = useState(null)

    return (
        <>
        
        <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
        
        <Container maxWidth="lg" sx={{ mt: 4 }}>

            <Typography variant="h5" component="h2" gutterBottom>
                Fleet Overview
            </Typography>

            <Box sx={{ mb: 4 }}>
                <RobotDataGrid onSuccess={setNotification} />
            </Box>

            <Typography variant="h5" component="h2" gutterBottom>
                Discrepancy Overview
            </Typography>

            <Box sx={{ mb: 4 }}>
                <DiscrepancyDataGrid />
            </Box>

        </Container>

        <Snackbar
            open={Boolean(notification)}
            autoHideDuration={4000}
            onClose={() => setNotification(null)}>
                <Alert severity="success" onClose={() => setNotification(null)}>{notification}</Alert>
            </Snackbar>
        
        </>
    );
}

// conditional layout switcher component that renders either the Dashboard of LoginForm based on 
// the user's authentication status that is tracked in the global AuthContext
function AppContent() {
    const{isAuthenticated} = useAuth();
    return isAuthenticated ? <Dashboard /> : <LoginForm />
}


// now acts as a root application component that wraps the entire app in the AuthProvider context
function App(){
    return (
    <AuthProvider>
        <AppContent />
    </AuthProvider>
    );

    // return (
    //     <>
    //         <AppHeader />
    //         <Container maxWidth='lg' sx={{mt: 4}}>
                
    //             <Typography variant="h5" component="h2" gutterBottom sx={{WebkitTextStroke: '0.1px #000000',}}>
    //                 Fleet Overview
    //             </Typography>

    //             <Box sx={{ mb: 4 }}>
    //                 <RobotList robots={mockRobots} />
    //             </Box>

    //             <Typography variant="h6" component="h2" gutterBottom sx={{WebkitTextStroke: '0.1px #000000',}}>
    //                 Co-Location Discrepancies
    //             </Typography>

    //             <Box>
    //                 <DiscrepancyList discrepancies={discrepancies} />
    //             </Box>
            
    //         </Container>
    //     </>
    // )
}

export default App;