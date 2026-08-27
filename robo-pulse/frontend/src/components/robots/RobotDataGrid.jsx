import { DataGrid} from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import { Alert, Box, CircularProgress } from "@mui/material";
import apiClient from "../../api/client";

// define DataGrid columns and map them to backend API resposne data
const columns = [
    {field: 'id', headerName: 'ID', width: 70},
    {field: 'serial_number', headerName: 'Serial Number', width: 150},
    {field: 'model', headerName: 'Model', width: 160},
    {field: 'battery_level', headerName: 'Battery Percent', width: 120, type: 'number'},
    {field: 'status', headerName: 'Status', width: 130},
    {field: 'facility_id', headerName: 'Facility ID', width: 110, type: 'number'},
];

// local state variables (local to this individual component) for tracking table rows, 
// loading status, and network errors to track the lifecycle of the async API request so
// the UI can render appropriately
function RobotDataGrid() {
    const [robots, setRobots] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // React effect hook that runs our async fetch to get the data
    useEffect(() => {
        // track the component mount status to prevent memory leaks via network request delays
        let isMounted = true;
        setLoading(true);

        // pull our robot fleet data from backend
        async function fetchRobots() {
            try {
                const response = await apiClient.get('/robots');
                if(isMounted) setRobots(response.data);
            } catch {
                if (isMounted) setError('Could not load fleet data');
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchRobots();
        return () => {
            isMounted = false;
        };
    }, []);

    // show a spinning progress indicator if we are loading data
    if (loading) return <CircularProgress />

    // show an error if the API call fails
    if (error) return <Alert severity="error"> {error} </Alert>

    // expected response, returns data grid
    return (
        <Box sx={{height: 400, width: '100%'}}>
            <DataGrid rows={robots} columns={columns} getRowId={(row) => row.id} />
        </Box>
    );
}

export default RobotDataGrid;