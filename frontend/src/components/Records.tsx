import * as React from 'react';
import { Link as RouterLink, useParams } from 'react-router-dom';
import { useMutation } from 'react-query';
import axios from 'axios';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import FilterCenterFocusSharpIcon from '@mui/icons-material/FilterCenterFocusSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
import Divider from '@mui/material/Divider';
import Badge from '@mui/material/Badge';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import Sheet from '@mui/joy/Sheet';
import config from '../utils/config';
import { Record } from './Interfaces';
import { format_date } from '../utils/formatter';

export default function Records() {

    const params = useParams();
    const [activeRecordId, setActiveRecordId] = React.useState<number | undefined>(undefined);

    // Set active procedure if component is rendered
    if (params.recordId && Number(params.recordId) !== activeRecordId) {
        setActiveRecordId(Number(params.recordId))
    }

    const [dialogOpen, setDialogOpen] = React.useState(false)

    // Is this single procedure variable necessary?
    const [record, setRecord] = React.useState<Record>({ id: 0, procedure_id: 0, device_id: 0, date: "", thumbnail: "", data: "", comment: "" });
    const [records, setRecords] = React.useState<Record[] | undefined >(undefined);

    async function fetchRecords() {
        console.log(`${config["baseURL"]}/patients/${params.patientId}/${params.procedureId}/records`)
        await axios.get(`${config["baseURL"]}/patients/${params.patientId}/${params.procedureId}/records`)
        .then((response) => {setRecords(response.data)})
    }

    // Trigger fetch records, listens to params.procedureId and record
    React.useEffect(() => {
        fetchRecords()
    }, [params.procedureId, record]);

    // Post a new record and refetch records table
    const mutation = useMutation(async() => {
        await axios.post(`${config["baseURL"]}/patients/${params.patientId}/${params.procedureId}/records/new/`, record)
        .then((response) => {
            setRecord(response.data)
            fetchRecords()
        })
        .catch((err) => {
            console.log(err)
        })
    })

    return (
        <Box>
            <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <Typography level="h5"> Records </Typography>
                    <Badge badgeContent={records?.length} color="primary"/>
                </Box>

                <IconButton size='sm' variant='outlined'>
                    <AddSharpIcon onClick={() => setDialogOpen(true)}/>
                </IconButton>

                {/* Model */}
                <Modal
                    keepMounted
                    open={dialogOpen}
                    color='neutral'
                    onClose={() => setDialogOpen(false)}
                    sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}
                >
                    <Sheet
                        variant="outlined"
                        sx={{ width: '50vh', height: '50vh', borderRadius: 'md', p: 3 }}
                    >
                        <ModalClose
                            sx={{
                                top: '10px',
                                right: '10px',
                                borderRadius: '50%',
                                bgcolor: 'background.body',
                            }}
                        />
                        <Typography level="h4" textColor="inherit">
                            Add New Record
                        </Typography>
                        <Typography id="modal-desc" textColor="text.tertiary">
                            Parameters...
                        </Typography>
                    </Sheet>
                </Modal>


            </Box>
                
            <Divider />

            <List sx={{ pt: 0 }}>
                {records?.map((record, index) => (
                    <React.Fragment key={index}>

                        <ListItem>
                            <ListItemButton 
                                component={RouterLink}
                                to={`${record.id}`}
                                selected={record.id === activeRecordId}
                                onClick={() => setActiveRecordId(record.id)}
                                variant={record.id === activeRecordId ? "soft" : "plain"}
                            >
                                <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                                    <FilterCenterFocusSharpIcon />
                                </ListItemDecorator>
                                <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                                    <Typography level="body2" textColor="text.tertiary">{record.id}</Typography>
                                    <Typography>{record.comment}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ format_date(record.date) }</Typography>
                                    <Typography level="body2" textColor="text.tertiary"> Device ID: { record.device_id }</Typography>
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
