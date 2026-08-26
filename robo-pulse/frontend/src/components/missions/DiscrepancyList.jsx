import { Grid } from "@mui/material";

import { discrepancies } from "../../mockData/discrepancies";
import DiscrepancyCard from "./DiscrepancyCard";
import RobotCard from "../robots/RobotCard";

function DiscrepancyList({discrepancies}) {
    return (
        <Grid container spacing={2} direction={"row"} sx={{justifyContent: "center"}}>

            {discrepancies.map((discrepancy) => 
            <Grid item key={discrepancy.id}>
                <DiscrepancyCard discrepancy={discrepancy} />
            </Grid>)}
        </Grid>
    );
}

export default DiscrepancyList