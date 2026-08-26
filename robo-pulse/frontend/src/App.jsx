import { Container, Typography, Box } from "@mui/material";
import RobotList from "./components/robots/RobotList";
import AppHeader from "./components/layout/AppHeader";
import { mockRobots } from "./mockData/robots";
import DiscrepancyList from "./components/missions/DiscrepancyList";
import { discrepancies } from "./mockData/discrepancies";

function App(){
    return (
        <>
            <AppHeader />
            <Container maxWidth='lg' sx={{mt: 4}}>
                
                <Typography variant="h5" component="h2" gutterBottom sx={{WebkitTextStroke: '0.1px #000000',}}>
                    Fleet Overview
                </Typography>

                <Box sx={{ mb: 4 }}>
                    <RobotList robots={mockRobots} />
                </Box>

                <Typography variant="h6" component="h2" gutterBottom sx={{WebkitTextStroke: '0.1px #000000',}}>
                    Co-Location Discrepancies
                </Typography>

                <Box>
                    <DiscrepancyList discrepancies={discrepancies} />
                </Box>
            
            </Container>
        </>
    )
}

export default App;