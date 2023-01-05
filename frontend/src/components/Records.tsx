import * as React from 'react';
import { Link as RouterLink, useParams, useOutletContext } from 'react-router-dom';
import { useMutation } from 'react-query';
import axios from 'axios';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import TextField from '@mui/joy/TextField';
import Link from '@mui/material/Link';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import FormHelperText from '@mui/joy/FormHelperText';
import FormLabel from '@mui/joy/FormLabel';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import MenuItemSelect from '@mui/material/MenuItem';
import FilterCenterFocusSharpIcon from '@mui/icons-material/FilterCenterFocusSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
// import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import Badge from '@mui/material/Badge';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import ClearSharpIcon from '@mui/icons-material/ClearSharp';
import EditSharpIcon from '@mui/icons-material/EditSharp';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import Stack from '@mui/joy/Stack';
import config from '../utils/config';
import { Record, Device } from './Interfaces';
import { format_date } from '../utils/formatter';

export default function Records() {

    const { ref } = useOutletContext<{ ref: any }>();

    const params = useParams();
    const [activeRecordId, setActiveRecordId] = React.useState<number | null>(null);
    const [dialogOpen, setDialogOpen] = React.useState<boolean>(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const [contextOpen, setContextOpen] = React.useState<number | null>(null);
    const [records, setRecords] = React.useState<Record[] | undefined >(undefined);
    const [devices, setDevices] = React.useState<Device[] | undefined>(undefined);
    const [record, setRecord] = React.useState<Record>( // store intermediate state in record creation
        { id: 0, procedure_id: 0, device_id: 0, date: "", thumbnail: "", data: "", comment: "" }
    );

    const handleContextClose = () => {
        setAnchorEl(null);
        setContextOpen(null);
    }

    const handleContextOpen = (e, recordId) => {
        e.preventDefault();
        setAnchorEl(e.currentTarget);
        setContextOpen(recordId);
    }

    // Set active procedure if component is rendered
    function updateActive() {
        if (params.recordId === undefined) {
            setActiveRecordId(null)
        }
        else if (Number(params.recordId) !== activeRecordId) {
            setActiveRecordId(Number(params.recordId))
        } 
    }





    // Fetch a list of all records and assign them to records
    async function fetchRecords() {
        await axios.get(`${config["baseURL"]}/${params.procedureId}/records`)
        .then((response) => {setRecords(response.data)})
    }

    async function fetchDevices() {
        await axios.get(`${config.baseURL}/devices`)
        .then((response) => {setDevices(response.data)})
    }
    
    // Trigger fetch records, listens to params.procedureId and record
    React.useEffect(() => {
        fetchRecords();
        fetchDevices();
        updateActive();
    }, [params.procedureId, params.recordId]);

    // Post a new record and refetch records table
    const mutation = useMutation(async() => {
        console.log("Post record...")
        await axios.post(`${config["baseURL"]}/${params.procedureId}/records/new`, record)
        .then((response) => {
            setRecord(response.data)
            fetchRecords()
            console.log(response.data)
        })
        .catch((err) => {
            console.log(err)
        })
    })

    // Use imperative handle to define a delete record function, which can be called from parent by ref
    React.useImperativeHandle(ref, () => ({
        async deleteRecord() {
            await axios.delete(`${config.baseURL}/patients/${params.patientId}/${params.procedureId}/records/${params.recordId}/`)
            .then(() => { fetchRecords(); })
        }
    }))

    async function deleteRecordId(recordId) {
        await axios.delete(`${config.baseURL}/patients/${params.patientId}/${params.procedureId}/records/${recordId}/`)
        .then(() => { fetchRecords(); })
    }

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
                        sx={{
                            width: '50vw', 
                            // height: '50vh',
                            borderRadius: 'md',
                            p: 5,
                            // boxShadow: 'lg',
                        }}
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
                            Create new record
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
                                    label='Comment' 
                                    name='comment'
                                    onChange={(e) => setRecord({...record, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />

                                {/* Data Input */}
                                <TextField 
                                    label='Data'
                                    name='data'
                                    placeholder='https://marketing.webassets.siemens-healthineers.com/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm'
                                    onChange={(e) => setRecord({...record, [e.target.name]: e.target.value})} 
                                    required 
                                />
                                <FormHelperText>
                                    Enter a DICOM URL (placeholder)
                                </FormHelperText>
                                <Link
                                    href="https://marketing.webassets.siemens-healthineers.com/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm"
                                    underline='hover'
                                >
                                    Example DICOM URL, click to download
                                </Link>

                                {/* Device Selection */}
                                <FormLabel htmlFor="select-button" id='select-label'>Select Device</FormLabel>
                                <Select
                                    placeholder='Select device...'
                                    onChange={(event, value) => { record.device_id = Number(value) }}
                                >
                                    {
                                        devices?.map((device, index) => (
                                            <Option key={device.id} value={device.id}>
                                                {device.address}
                                            </Option>
                                        ))
                                    }
                                </Select>
                                
                                <Button sx={{width: 100}} type="submit">Submit</Button>
                            </Stack>
                        </form>
                    </ModalDialog>
                </Modal>

            </Box>
                
            <Divider />

            <List size="sm" sx={{ pt: 0 }}>
                {records?.map((record, index) => (
                    <React.Fragment key={index}>

                        <ListItem>
                            <ListItemButton 
                                id="record-item"
                                component={RouterLink}
                                to={`${record.id}`}
                                selected={record.id === activeRecordId}
                                onClick={() => setActiveRecordId(record.id)}
                                variant={(record.id === activeRecordId || record.id === contextOpen) ? "soft" : "plain" }
                                onContextMenu={(e) => handleContextOpen(e, record.id)}
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

                                <Menu   
                                    id="record-context"
                                    anchorEl={anchorEl}
                                    open={record.id === contextOpen}
                                    onClose={() => handleContextClose()}
                                    sx={{ zIndex: 'snackbar' }}
                                    placement='auto'
                                >
                                    <MenuItem key="edit-record" variant='plain' disabled>
                                        <ListItemDecorator>
                                            <EditSharpIcon />
                                        </ListItemDecorator>{' '}
                                            Edit record
                                    </MenuItem>
                                    <ListDivider />
                                    <MenuItem key="delete-record" color='danger' onClick={() => { deleteRecordId(record.id); }}>
                                        <ListItemDecorator>
                                            <ClearSharpIcon />
                                        </ListItemDecorator>{' '}
                                            Delete record
                                    </MenuItem>

                                </Menu>
                                
                            </ListItemButton>  

                        </ListItem>

                        <ListDivider sx={{ m: 0 }} />
                    </React.Fragment>
                ))}
            </List>

        </Box>
    );  
}
