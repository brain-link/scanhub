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
// import DocumentScannerOutlinedIcon from '@mui/icons-material/DocumentScannerOutlined';
import ContentPasteSharpIcon from '@mui/icons-material/ContentPasteSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import ClearSharpIcon from '@mui/icons-material/ClearSharp';
import IconButton from '@mui/joy/IconButton';
import Divider from '@mui/material/Divider';
import Button from '@mui/joy/Button';
import TextField from '@mui/joy/TextField';
import Badge from '@mui/material/Badge';
import config from '../utils/config';
import Stack from '@mui/joy/Stack';
import { useQuery } from "react-query";
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';

import { Procedure } from './Interfaces';
import { format_date } from '../utils/formatter';

export default function Procedures() {

    const params = useParams();
    const [activeProcedureId, setActiveProcedureId] = React.useState<number | undefined>(undefined);
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);
    const [procedure, setProcedure] = React.useState<Procedure>(
        { id: 0, patient_id: 0, reason: "", date: "" }
    );

    React.useEffect(() => {
        if (params.procedureId && Number(params.procedureId) !== activeProcedureId){
            setActiveProcedureId(Number(params.procedureId));
        }
    }, [params.procedureId]);

    // Define fetch function for procedures table
    async function fetchProcedures () {
        await axios.get(`${config['baseURL']}/patients/${params.patientId}/procedures`)
        .then((response) => { setProcedures(response.data) })
    };

    async function deleteProcedure() {
        await axios.delete(`${config.baseURL}/patients/${params.patientId}/${params.procedureId}`)
        .then(() => { fetchProcedures(); })
    }

    // fetch procedures
    React.useEffect(() => {
        fetchProcedures();
    }, [params.procedureId]);

    const mutation = useMutation(async() => {
        await axios.post(`${config['baseURL']}/patients/${params.patientId}/procedures/new`, procedure)
        .then((response) => {
            setProcedure(response.data)
            fetchProcedures()
        })
        .catch((err) => { console.log(err) })
    })

    return (
        <Box>
            <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <Typography level="h5"> Procedures </Typography>
                    <Badge badgeContent={procedures?.length} color="primary"/>
                </Box>

                <Box sx={{ display: 'flex', gap: 1 }}>
                    <IconButton
                        id="delete-record"
                        variant="outlined"
                        size="sm"
                        color="danger"
                        disabled={!params.procedureId}
                        onClick={() => { deleteProcedure(); }}
                    >
                        <ClearSharpIcon />
                    </IconButton>
                    <IconButton size='sm' variant='outlined'>
                        <AddSharpIcon onClick={() => setDialogOpen(true)}/>
                    </IconButton>
                </Box>
            

                <Modal 
                    keepMounted
                    open={dialogOpen}
                    color='neutral'
                    onClose={() => setDialogOpen(false)}
                    sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
                >
                    <ModalDialog
                        aria-labelledby="basic-modal-dialog-title"
                        aria-describedby="basic-modal-dialog-description"
                        sx={{ width: '50vh', borderRadius: 'md', p: 5 }}
                    >
                        <ModalClose
                            sx={{
                                top: '10px',
                                right: '10px',
                                borderRadius: '50%',
                                bgcolor: 'background.body',
                            }}
                        />
                        <Typography
                            id="basic-modal-dialog-title"
                            component="h2"
                            level="inherit"
                            fontSize="1.25em"
                            mb="0.25em"
                        >
                            Create new procedure
                        </Typography>
                        
                        <form
                            onSubmit={(event) => {
                                event.preventDefault();
                                mutation.mutate();
                                setDialogOpen(false);
                            }}
                        >
                            <Stack spacing={2}>
                                <TextField 
                                    label="Patient concern" 
                                    name='reason'
                                    onChange={(e) => setProcedure({...procedure, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />
                                <TextField 
                                    label="Date" 
                                    name='date'
                                    onChange={(e) => setProcedure({...procedure, [e.target.name]: e.target.value})} 
                                    required 
                                />
                                <Button type="submit">Submit</Button>
                            </Stack>
                        </form>
                    </ModalDialog>
                </Modal>


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
