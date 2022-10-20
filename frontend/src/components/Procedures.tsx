import * as React from 'react';
import { Link as RouterLink, useLocation, useParams } from 'react-router-dom';
import { useMutation } from 'react-query';
import axios from 'axios';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import DocumentScannerOutlinedIcon from '@mui/icons-material/DocumentScannerOutlined';
import ContentPasteSharpIcon from '@mui/icons-material/ContentPasteSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
import Divider from '@mui/material/Divider';
import Badge from '@mui/material/Badge';
import config from '../utils/config';
import { useQuery } from "react-query";

import { Procedure } from './Interfaces';
import { format_date } from '../utils/formatter';

export default function Procedures() {

    const params = useParams();
    const [activeProcedureId, setActiveProcedureId] = React.useState<number | undefined>(undefined);

    React.useEffect(() => {
        if (params.procedureId && Number(params.procedureId) !== activeProcedureId){
            setActiveProcedureId(Number(params.procedureId));
        }
    }, [params.procedureId]);

    // Is this single procedure variable necessary?
    const [procedure, setProcedure] = React.useState<Procedure>({ id: 0, patient_id: 0, reason: "", date: "" });
    const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);

    // Define fetch function for procedures table
    async function fetchProcedures () {
        console.log(`${config['baseURL']}/patients/${params.patientId}/procedures`)
        await axios.get(`${config['baseURL']}/patients/${params.patientId}/procedures`).then((response) => {
            setProcedures(response.data)
        })
        // const {data, isSuccess} = useQuery<Procedure[]>(`/patients/${params.patientId}/procedures`);
        // isSuccess ? setProcedures(data) : () => {}
    };

    // fetch procedures
    React.useEffect(() => {
        fetchProcedures();
    }, []);

    const mutation = useMutation(async() => {
        await axios.post(`${config['baseURL']}/patients/${params.patientId}/procedures/new`, procedure)
        .then((response) => {
            setProcedure(response.data) // required?
            fetchProcedures()
        })
        .catch((err) => {
            console.log(err)
        })
    })

    return (
        <Box>
            <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <Typography level="h5"> Procedures </Typography>
                    <Badge badgeContent={procedures?.length} color="primary"/>
                </Box>

                <IconButton size='sm' variant='outlined'>
                    <AddSharpIcon />
                </IconButton>

            </Box>
                
            <Divider />

            <List sx={{ pt: 0 }}>
                {procedures?.map((procedure, index) => (
                    <React.Fragment key={index}>

                        <ListItem>
                            <ListItemButton 
                                component={RouterLink}
                                to={`${procedure.id}`}
                                selected={procedure.id === activeProcedureId}
                                onClick={() => setActiveProcedureId(procedure.id)}
                                variant={activeProcedureId === procedure.id ? "soft" : "plain"}
                            >
                                <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                                    <ContentPasteSharpIcon />
                                </ListItemDecorator>
                                <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                                    <Typography level="body2" textColor="text.tertiary">{procedure.id}</Typography>
                                    <Typography>{procedure.reason}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ format_date(procedure.date) }</Typography>
                                </Box>
                                
                            </ListItemButton>   
                        </ListItem>

                        <ListDivider sx={{ m: 0 }} />
                    </React.Fragment>
                ))}
            </List>
        </Box>
    );  
}
