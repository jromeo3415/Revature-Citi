import { useState, useEffect } from "react";
import { Alert, CircularProgress, Select, FormControl, InputLabel, MenuItem, Box, Input } from "@mui/material";
import apiClient from "../../api/client";
import { DataGrid } from "@mui/x-data-grid";

const columns = [
    {field: 'id', headerName: 'Mission ID', width: 70},
    {field: 'title', headerName: 'Title', width: 150},
    {field: 'robot_facility_id', headerName: 'Robot Facility ID', width: 70},
    {field: 'operator_facility_id', headerName: 'Operator Facility ID', width: 70},
];

const PRIORITY_OPTIONS = ['', 'Low', 'Medium', 'Critical'];

function DiscrepancyDataGrid() {
    const [discrepancies, setDiscrepancies] = useState([]);
    const [priority, setPriority] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() =>{
        let isMounted = true;
        setLoading(true);

        async function fetchDiscrepancies() {
            try {
                const response = await apiClient.get('/missions/discrepancies', {
                    params: {priority: priority || undefined},
                });
                if (isMounted) setDiscrepancies(response.data)
            } catch {
                if (isMounted) setError('Could not load mission discrepancies');
            } finally {
                if (isMounted) setLoading(false);
            }
        }

        fetchDiscrepancies();
        return () => {
            isMounted = false;
        }
    }, []);

    return (
        <Box sx ={{height: 400, width: '100%'}}>
            <FormControl size="small" sx={{ mb: 2, minWidth: 180}}>

                <InputLabel id="priority-filter-label">Priority</InputLabel>

                <Select
                    labelid="priority-filter-label"
                    label="priority"
                    value={priority}
                    onChange={(event) => setPriority(event.target.value)}
                >
                    {PRIORITY_OPTIONS.map((option) => 
                    <MenuItem key={option || 'all'} value={option}>
                        {option === '' ? 'All' : option}
                    </MenuItem>)}
                </Select>

            </FormControl>

            {loading && <CircularProgress />}
            {error && <Alert serverity="error">{error}</Alert>}

            {!loading && !error && (
                <Box sx={{height: 400, width: '100%'}}>
                    <DataGrid rows={discrepancies} columns={columns} getRowId={(row) => row.id} />
                </Box>
            )}
        </Box>
    );
}

export default DiscrepancyDataGrid;