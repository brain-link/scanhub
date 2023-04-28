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
import Grid from '@mui/joy/Grid';
import { useQuery } from "react-query";
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';

import { Exam } from '../../client/interfaces';
// import client from '../../client/queries';
import { ExamApiService } from '../../client/queries';


// Patient form items, order is row wise
const createExamFormContent = [
    {key: 'name', label: 'Exam Name', placeholder: 'Knee complaints'},
    {key: 'site', label: 'Site', placeholder: 'Berlin'},
    {key: 'address', label: 'Site Address', placeholder: ''},
    {key: 'creator', label: 'Name of Exam Creater', placeholder: 'Last name, first name'},
    {key: 'status', label: 'Status', placeholder: 'Exam created'},
]


function ExamList() {

    const examClient = new ExamApiService();

    const params = useParams();
    const [activeExamId, setActiveExamId] = React.useState<number | undefined>(undefined);
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
    const [contextOpen, setContextOpen] = React.useState<number | null>(null);

    const [exam, setExam] = React.useState<Exam>({
        id: 0, 
        patient_id: Number(params.patientId),
        name: '',
        procedures: [],
        country: 'D',
        site: '',
        address: '',
        creator: '', 
        status: '', 
        datetime_created: new Date(), 
        datetime_updated: new Date(),
    })

    const { data: exams, refetch, isLoading: examsLoading, isError: examsError } = useQuery<Exam[], Error>({
        queryKey: ['exam', params.patientId],
        queryFn: () => examClient.getAll(Number(params.patientId))
    });

    const handleContextClose = () => {
        setAnchorEl(null);
        setContextOpen(null);
    }

    const handleContextOpen = (e, examId) => {
        e.preventDefault();
        setAnchorEl(e.currentTarget);
        setContextOpen(examId);
    }

    // React.useEffect(() => {
    //     if (params.examId && Number(params.examId) !== activeExamId){
    //         setActiveExamId(Number(params.examId));
    //     }
    // }, [params.examId]);


    // async function deleteExam(examId) {
    //     // await axios.delete(`${config.baseURL}/patients/${params.patientId}/${procedureId}`)
    //     // .then(() => { fetchProcedures(); })
    //     console.log("Exam selected for deletion: ", examId)
    //     await client.exams.delete(examId)
    // }

    const deleteExamById = useMutation( async (id: number) => {
        await examClient.delete(id)
        .then(() => { refetch(); })
    })

    const createExam = useMutation(async() => {
        await examClient.create(exam).then( (response) => { exams?.push(response) } )
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
                        sx={{ width: '50vw', borderRadius: 'md', p: 5 }}
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
                                createExam.mutate();
                                setDialogOpen(false);
                            }}
                        >
                            <Stack spacing={5}>
                                <Grid container rowSpacing={1.5} columnSpacing={5}>
                                    {
                                        createExamFormContent.map((item, index) => (
                                            <Grid key={ index } md={6}
                                            >
                                                <FormLabel>{ item.label }</FormLabel>
                                                <Input 
                                                    name={ item.key }
                                                    onChange={(e) => setExam({...exam, [e.target.name]: e.target.value})} 
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
                                    <Typography>{exam.name}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ `Issuer: ${exam.creator}, ${exam.site}`}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{exam.status}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ `Created: ${new Date(exam.datetime_created).toDateString()}` }</Typography>
                                    <Typography level="body2" textColor="text.tertiary">{ `Updated: ${exam.datetime_updated ? new Date(exam.datetime_updated).toDateString() : '-'}` }</Typography>
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
                                    <MenuItem key="delete-exam" color='danger' onClick={() => { deleteExamById.mutate(exam.id); }}>
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