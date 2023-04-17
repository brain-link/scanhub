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
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import ClearSharpIcon from '@mui/icons-material/ClearSharp';
import EditSharpIcon from '@mui/icons-material/EditSharp';
import ContentPasteSharpIcon from '@mui/icons-material/ContentPasteSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
import Divider from '@mui/material/Divider';
import Button from '@mui/joy/Button';
import Input from '@mui/joy/Input';
import FormLabel from '@mui/joy/FormLabel';
import Badge from '@mui/material/Badge';
import config from '../../utils/config';
import Stack from '@mui/joy/Stack';
import { useQuery } from "react-query";
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';

// import { Procedure } from './Interfaces';
// import { format_date } from '../utils/formatter';
import { Exam } from '../../client/interfaces';
import client from '../../client/queries';


function ExamList() {

    const params = useParams();
    const [activeExamId, setActiveExamId] = React.useState<number | undefined>(undefined);
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const [contextOpen, setContextOpen] = React.useState<number | null>(null);

    // const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);
    // const [procedure, setProcedure] = React.useState<Procedure>({ 
    //     id: 0, name: "", modality: "", status: "", datetime_created: new Date(), datetime_updated: new Date()
    // });

    const [exam, setExam] = React.useState<Exam>({
        id: 0, 
        patient_id: Number(params.patientId),
        name: '',
        procedures: [],
        country: '',
        site: '',
        address: '',
        creator: '', 
        status: '', 
        datetime_created: new Date(), 
        datetime_updated: new Date(),
    })

    const { data: exams, isLoading: examsLoading, isError: examsError } = useQuery<Exam[], Error>(
        ['exams', params.patientId], 
        () => client.exams.getAll(Number(params.patientId))
    );

    const handleContextClose = () => {
        setAnchorEl(null);
        setContextOpen(null);
    }

    const handleContextOpen = (e, examId) => {
        e.preventDefault();
        setAnchorEl(e.currentTarget);
        setContextOpen(examId);
    }

    React.useEffect(() => {
        if (params.examId && Number(params.examId) !== activeExamId){
            setActiveExamId(Number(params.examId));
        }
    }, [params.examId]);

    // Define fetch function for procedures table
    // async function fetchProcedures () {
    //     // await axios.get(`${config['baseURL']}/patients/${params.patientId}/procedures`)
    //     // .then((response) => { setProcedures(response.data) })
    //     await client.procedures.getAll().then((data) => {setProcedures(data)})
    // };

    async function deleteExam(examId) {
        // await axios.delete(`${config.baseURL}/patients/${params.patientId}/${procedureId}`)
        // .then(() => { fetchProcedures(); })
        console.log("Exam selected for deletion: ", examId)
        // await client.exams.delete(examId)
    }

    // fetch procedures
    // React.useEffect(() => {
    //     fetchProcedures();
    // }, [params.procedureId]);

    const mutation = useMutation(async() => {
        // await axios.post(`${config['baseURL']}/patients/${params.patientId}/procedures/new`, procedure)
        // .then((response) => {
        //     setProcedure(response.data)
        //     fetchProcedures()
        // })
        // .catch((err) => { console.log(err) })

        await client.exams.create(exam).then()
        .catch((err) => { console.log(err) }) 
    })

    return (
        <Box>
            <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <Typography level="h5"> Exams </Typography>
                    <Badge badgeContent={exams?.length} color="primary"/>
                </Box>

                <Box sx={{ display: 'flex', gap: 1 }}>
                    {/* <IconButton
                        id="delete-record"
                        variant="outlined"
                        size="sm"
                        color="danger"
                        disabled={!params.procedureId}
                        onClick={() => { deleteProcedure(); }}
                    >
                        <ClearSharpIcon />
                    </IconButton> */}
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
                            Create new exam
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
                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />
                                <FormLabel>Site</FormLabel>
                                <Input 
                                    name='site'
                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />
                                <FormLabel>Address</FormLabel>
                                <Input 
                                    name='address'
                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />
                                <FormLabel>Country</FormLabel>
                                <Input 
                                    name='country'
                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />
                                <FormLabel>Creator</FormLabel>
                                <Input 
                                    name='creator'
                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                    autoFocus 
                                    required 
                                />
                                <FormLabel>Status</FormLabel>
                                <Input 
                                    name='status'
                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
                                    autoFocus 
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
                {exams?.map((exam, index) => (
                    <React.Fragment key={index}>

                        <ListItem>
                            <ListItemButton 
                                id="exam-item"
                                component={RouterLink}
                                to={`${exam.id}`}
                                selected={exam.id === activeExamId}
                                onClick={() => setActiveExamId(exam.id)}
                                variant={(exam.id === activeExamId || exam.id === contextOpen)? "soft" : "plain"}
                                onContextMenu={(e) => handleContextOpen(e, exam.id)}
                            >
                                <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                                    <ContentPasteSharpIcon />
                                </ListItemDecorator>
                                <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                                    <Typography level="body2" textColor="text.tertiary">{exam.name}</Typography>
                                    <Typography>{exam.status}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ exam.datetime_created.toLocaleString() }</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ exam.datetime_updated ? exam.datetime_updated.toLocaleString() : "" }</Typography>
                                </Box>

                                <Menu   
                                    id="exam-context"
                                    anchorEl={anchorEl}
                                    open={exam.id === contextOpen}
                                    onClose={() => handleContextClose()}
                                    sx={{ zIndex: 'snackbar' }}
                                    placement='auto'
                                >
                                    <MenuItem key="edit-exam" variant='plain' disabled>
                                        <ListItemDecorator>
                                            <EditSharpIcon />
                                        </ListItemDecorator>{' '}
                                            Edit exam
                                    </MenuItem>
                                    <ListDivider />
                                    <MenuItem key="delete-exam" color='danger' onClick={() => { deleteExam(exam.id); }}>
                                        <ListItemDecorator>
                                            <ClearSharpIcon />
                                        </ListItemDecorator>{' '}
                                            Delete exam
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

export default ExamList;