import { Card, CardContent, Typography, Chip, Alert, Stack } from "@mui/material"

function DiscrepancyCard({discrepancy}) {
    return (
        <Card variant="outlined" sx={{minWidth: 240}}>
            <CardContent>

                <Typography variant="h7" component={"div"}>
                    {discrepancy.title}
                </Typography>

                <Stack direction={"row"} spacing={1}>

                    <Chip
                        label={`Robot Facility ID: ${discrepancy.robot_facility_id}`}
                        size="small"
                    />

                    <Chip
                        label={`Operator Facility ID: ${discrepancy.operator_facility_id}`}
                        size="small"
                    />

                </Stack>

                <Alert severity="warning" sx={{justifyContent: "center", marginTop: 2, marginBottom: -1}}>
                    Facilitly mismatch detected
                </Alert>

            </CardContent>
        </Card>
    );
}

export default DiscrepancyCard;