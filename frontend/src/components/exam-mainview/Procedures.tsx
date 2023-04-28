import * as React from 'react';
import { Link as RouterLink, useParams, useOutletContext } from 'react-router-dom';
import { useMutation, useQuery } from 'react-query';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
// import Link from '@mui/material/Link';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
// import FormHelperText from '@mui/joy/FormHelperText';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
// import MenuItemSelect from '@mui/material/MenuItem';
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
// import Select from '@mui/joy/Select';
// import Option from '@mui/joy/Option';
import Stack from '@mui/joy/Stack';
import Grid from '@mui/joy/Grid';
// import client from '../../client/queries';
import { ProcedureApiService } from '../../client/queries';
import { Procedure } from '../../client/interfaces'; 

const createProcedureForm = [
    {key: 'name', label: 'Procedure Name', placeholder: 'MRI examination'},
    {key: 'status', label: 'Status', placeholder: 'Procedure created'},
]

function ProceduresList() {

    const procedureClient = new ProcedureApiService();
    const { ref } = useOutletContext<{ ref: any }>();

    const params = useParams();

    const [activeProcedureId, setActiveProcedureId] = React.useState<number | null>(null);
    const [dialogOpen, setDialogOpen] = React.useState<boolean>(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const [contextOpen, setContextOpen] = React.useState<number | null>(null);
    const [procedure, setProcedure] = React.useState<Procedure>( // store intermediate state in record creation
        { id: 0, exam_id: Number(params.examId), name: "", status: "", jobs: [], datetime_created: new Date(), datetime_updated: new Date()}
    );

    const handleContextClose = () => {
        setAnchorEl(null);
        setContextOpen(null);
    }

    const handleContextOpen = (e, procedureId) => {
        e.preventDefault();
        setAnchorEl(e.currentTarget);
        setContextOpen(procedureId);
    }

    // Set active procedure if component is rendered
    // function updateActive() {
    //     if (params.procedureId === undefined) {
    //         setActiveProcedureId(null)
    //     }
    //     else if (Number(params.procedureId) !== activeProcedureId) {
    //         setActiveProcedureId(Number(params.procedureId))
    //     } 
    // }

    // Query all procedures
    const { data: procedures, refetch, isLoading: proceduresLoading, isError: proceduresError } = useQuery<Procedure[], Error>(
        ['procedures', params.examId], 
        () => procedureClient.getAll(Number(params.examId))
    );

    // Move this part to Record
    // const { data: devices, isLoading: devicesLoading, isError: devicesError } = useQuery<Device[], Error>(
    //     ['devices'], 
    //     () => client.devices.getAll()
    // );


    // Post a new record and refetch records table
    const createProcedure = useMutation(async() => {
        await procedureClient.create(procedure).then( (response) => { procedures?.push(response) } )
        .catch((err) => { console.log(err) }) 
    })

    const deleteProcedureById = useMutation(async (id: number) => {
        await procedureClient.delete(id)
        .then(() => { refetch(); })
    })

    // Use imperative handle to define a delete record function, which can be called from parent by ref
    React.useImperativeHandle(ref, () => { deleteProcedureById.mutate(Number(params.procedureId)) })


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
                            Create new procedure
                        </Typography>
                        
                        <form
                            onSubmit={(event) => {
                                event.preventDefault();
                                createProcedure.mutate();
                                setDialogOpen(false);
                            }}
                        >
                            <Stack spacing={5}>
                                <Grid container rowSpacing={1.5} columnSpacing={5}>
                                    {
                                        createProcedureForm.map((item, index) => (
                                            <Grid key={ index } md={12}
                                            >
                                                <FormLabel>{ item.label }</FormLabel>
                                                <Input 
                                                    name={ item.key }
                                                    onChange={(e) => setProcedure({...procedure, [e.target.name]: e.target.value})} 
                                                    placeholder={ item.placeholder }
                                                    required 
                                                />
                                            </Grid>
                                        ))
                                    }
                                </Grid>
                                <Button size='sm' type="submit" sx={{ maxWidth: 100 }}>Submit</Button>
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
                                    <Typography>{ procedure.name }</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ `Created: ${new Date(procedure.datetime_created).toDateString()}` }</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ `Updated: ${procedure.datetime_updated ? new Date(procedure.datetime_updated).toDateString() : '-'}` }</Typography>
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
                                            Edit procedure
                                    </MenuItem>
                                    <ListDivider />
                                    <MenuItem key="delete-record" color='danger' onClick={() => { deleteProcedureById.mutate(procedure.id) }}>
                                        <ListItemDecorator>
                                            <ClearSharpIcon />
                                        </ListItemDecorator>{' '}
                                            Delete procedure
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