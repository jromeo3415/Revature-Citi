import { Card, CardContent, Typography, Chip, Stack } from "@mui/material"

const LOW_BATTERY_THRESHOLD = 20;

{/**
    RobotCard function is a React component that takes in a 'robot' object as a prop (aka parameter)
    the component uses MUI components to create a card that displays the robot's data and it also checks if 
    the robot's battery level is below a certain threshold (LOW_BATTERY_THRESHOLD), if it is below that 
    threshold, it will change the color of the battery level chip accordingly.      
*/}

function RobotCard({robot}) {
    const isLowBattery = robot.batteryLevel < LOW_BATTERY_THRESHOLD;

return (
    <Card variant='outlined' sx={{minWidth: 240}}>
        <CardContent>

            <Typography variant="h6" component="div">
                {robot.serialNumber}
            </Typography>

            <Typography color="text.secondary" gutterBottom>
                {robot.model}
            </Typography>

            {/** The stack component is a layout component that arranges its children in a row or column */}
            <Stack direction="row" spacing={1} sx={{justifyContent: "center", alignContent: "center", alignItems: "center"}}>

                {/**Chip component is a small, interactive element that can display information or trigger actions */}
                <Chip
                    label={`${robot.batteryLevel}% battery`}
                    color={isLowBattery ? 'error' : 'success'}
                    size='small'
                />

                <Chip
                    label={robot.status}
                    variant="outlined"
                    size="small"
                />

            </Stack>

        </CardContent>
    </Card>

);
}

export default RobotCard;