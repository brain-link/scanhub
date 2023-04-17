import * as React from 'react';
import { Link as RouterLink, useParams, useOutletContext } from 'react-router-dom';
import { useMutation, useQuery } from 'react-query';
import axios from 'axios';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
import Link from '@mui/material/Link';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import FormHelperText from '@mui/joy/FormHelperText';
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
import config from '../../utils/config';
import client from '../../client/queries';
import { Procedure, Device } from '../../client/interfaces'; 

function ProceduresList() {

    const { ref } = useOutletContext<{ ref: any }>();

    const params = useParams();
    const [activeProcedureId, setActiveProcedureId] = React.useState<number | null>(null);
    const [dialogOpen, setDialogOpen] = React.useState<boolean>(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const [contextOpen, setContextOpen] = React.useState<number | null>(null);
    // const [procedures, setProcedures] = React.useState<Procedure[] | undefined >(undefined);
    // const [devices, setDevices] = React.useState<Device[] | undefined>(undefined);
    const [procedure, setProcedure] = React.useState<Procedure>( // store intermediate state in record creation
        { id: 0, name: "", modality: "", status: "", records: [], datetime_created: new Date(), datetime_updated: new Date()}
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
            setActiveProcedureId(null)
        }
        else if (Number(params.recordId) !== activeProcedureId) {
            setActiveProcedureId(Number(params.procedureId))
        } 
    }

    const { data: procedures, isLoading: proceduresLoading, isError: proceduresError } = useQuery<Procedure[], Error>(
        ['procedures', params.examId], 
        () => client.procedures.getAll(Number(params.examId))
    );

    // Move this part to Record
    // const { data: devices, isLoading: devicesLoading, isError: devicesError } = useQuery<Device[], Error>(
    //     ['devices'], 
    //     () => client.devices.getAll()
    // );



    // Fetch a list of all records and assign them to records
    // async function fetchRecords() {
    //     await axios.get(`${config["baseURL"]}/${params.procedureId}/records`)
    //     .then((response) => {setProcedures(response.data)})
    // }

    // async function fetchDevices() {
    //     await axios.get(`${config.baseURL}/devices`)
    //     .then((response) => {setDevices(response.data)})
    // }
    
    // Trigger fetch records, listens to params.procedureId and record
    // React.useEffect(() => {
    //     fetchRecords();
    //     fetchDevices();
    //     updateActive();
    // }, [params.procedureId, params.recordId]);

    // Post a new record and refetch records table
    const mutation = useMutation(async() => {
        console.log("Posting procedure...")
        // await axios.post(`${config["baseURL"]}/${params.procedureId}/records/new`, record)
        // .then((response) => {
        //     setRecord(response.data)
        //     fetchRecords()
        //     console.log(response.data)
        // })
        // .catch((err) => {
        //     console.log(err)
        // })
    })

    // Use imperative handle to define a delete record function, which can be called from parent by ref
    React.useImperativeHandle(ref, () => ({
        async deleteProcedure() {
            // await axios.delete(`${config.baseURL}/patients/${params.patientId}/${params.procedureId}/records/${params.recordId}/`)
            await client.procedures.delete(Number(params.procedureId))
            // .then(() => { fetchRecords(); })
        }
    }))

    async function deleteProcedureById(procedureId: number) {
        // await axios.delete(`${config.baseURL}/patients/${params.patientId}/${params.procedureId}/records/${recordId}/`)
        // .then(() => { fetchRecords(); })
        await client.procedures.delete(procedureId)
    }

    return (
        <Box>
            <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <Typography level="h5"> Procedures </Typography>
                    <Badge badgeContent={procedures?.length} color="primary"/>
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
                                <FormLabel>Name</FormLabel>
                                <Input 
                                    name='name'
                                    onChange={(e) => setProcedure({...procedure, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />

                                {/* Data Input */}
                                <FormLabel>Status</FormLabel>
                                <Input 
                                    name='status'
                                    // placeholder='https://marketing.webassets.siemens-healthineers.com/fcc5ee5afaaf9c51/b73cfcb2da62/Vida_Head.MR.Comp_DR-Gain_DR.1005.1.2021.04.27.14.20.13.818.14380335.dcm'
                                    onChange={(e) => setProcedure({...procedure, [e.target.name]: e.target.value})} 
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

                                {/* Device Selection, TODO: Move to Record component... */}
                                {/* <FormLabel htmlFor="select-button" id='select-label'>Select Device</FormLabel>
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
                                </Select> */}
                                
                                <Button sx={{width: 100}} type="submit">Submit</Button>
                            </Stack>
                        </form>
                    </ModalDialog>
                </Modal>

            </Box>
                
            <Divider />

            <List size="sm" sx={{ pt: 0 }}>
                {procedures?.map((procedure, index) => (
                    <React.Fragment key={index}>

                        <ListItem>
                            <ListItemButton 
                                id="record-item"
                                component={RouterLink}
                                to={`${procedure.id}`}
                                selected={procedure.id === activeProcedureId}
                                onClick={() => setActiveProcedureId(procedure.id)}
                                variant={(procedure.id === activeProcedureId || procedure.id === contextOpen) ? "soft" : "plain" }
                                onContextMenu={(e) => handleContextOpen(e, procedure.id)}
                            >
                                <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                                    <FilterCenterFocusSharpIcon />
                                </ListItemDecorator>
                                <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                                    <Typography level="body2" textColor="text.tertiary">{procedure.id}</Typography>
                                    <Typography>{procedure.name}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ procedure.datetime_created.toLocaleString() }</Typography>
                                    <Typography level="body2" textColor="text.tertiary"> Modality: { procedure.modality }</Typography>
                                </Box>

                                <Menu   
                                    id="record-context"
                                    anchorEl={anchorEl}
                                    open={procedure.id === contextOpen}
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
                                    <MenuItem key="delete-record" color='danger' onClick={() => { deleteProcedureById(procedure.id); }}>
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

export default ProceduresList;