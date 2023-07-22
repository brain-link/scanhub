// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// PatientIndex.tsx is responsible for rendering the patient view. It is the entry point for the patient view.

import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { useMutation } from 'react-query';

// Mui Material
import { styled } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';

// Mui Joy
import Box from '@mui/joy/Box';
import List from '@mui/joy/List';
import Badge from '@mui/material/Badge';
import Typography from '@mui/joy/Typography';
import IconButton from '@mui/joy/IconButton';
import ListDivider from '@mui/joy/ListDivider';
import KeyboardArrowRightSharpIcon from '@mui/icons-material/KeyboardArrowRightSharp';
import KeyboardArrowLeftSharpIcon from '@mui/icons-material/KeyboardArrowLeftSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';

// Import sub components
import PatientInfo from '../components/PatientInfo';
import ExamItem from '../components/ExamItem';
import ProcedureItem from '../components/ProcedureItem';
import JobView from '../components/jobs/JobView';
import ExamModal from '../components/ExamModal';
import ProcedureModal from '../components/ProcedureModal';

// Import interfaces, api services and global variables
import { Patient } from '../interfaces/data.interface';
import { Exam } from '../interfaces/data.interface';
import { Procedure } from '../interfaces/data.interface';
import { Job } from '../interfaces/data.interface';
import client from '../client/exam-tree-queries';
import { patientView, navigation } from '../utils/size_vars';
import { create } from '@mui/material/styles/createTransitions';


const Main = styled('div', { shouldForwardProp: (prop) => prop !== 'open' }) <{ open?: boolean }>
(
    ({ theme, open }) => (
        {
            // flexGrow: 1,
            display: 'flex',
            flexDirection: 'row',
            height: '100%',
            transition: theme.transitions.create('margin', {
                    easing: theme.transitions.easing.sharp,
                    duration: theme.transitions.duration.leavingScreen,
            }),
            marginLeft: 0,
            ...(open && {
                transition: theme.transitions.create('margin', {
                    easing: theme.transitions.easing.easeOut,
                    duration: theme.transitions.duration.enteringScreen,
                }),
                marginLeft: patientView.drawerWidth     //theme.patientView.drawerWidth
            })
        }
    )
);


function PatientIndex() {

    const params = useParams();

    const [activeTool, setActiveTool] = React.useState<string | undefined>(undefined);
    const [sidePanelOpen, setSidePanelOpen] = React.useState(true);

    // State of create modals for exam and procedure
    const [examModalOpen, setExamModalOpen] = React.useState(false);
    const [procedureModalOpen, setProcedureModalOpen] = React.useState(false);

    const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);
    const [jobs, setJobs] = React.useState<Job[] | undefined>(undefined);

    // Set active tool if component is rendered
    // if (params.examViewId && params.examViewId.toString() !== activeTool) {
    //     setActiveTool(params.examViewId.toString())
    // }

    // useQuery for caching the fetched data
    const { data: patient, refetch: refetchPatient, isLoading: patientLoading, isError: patientError } = useQuery<Patient, Error>({
        queryKey: ['patient', params.patientId], 
        queryFn: () => client.patientService.get(Number(params.patientId))
    });
    
    // Query all exams of the patient
    const { data: exams, refetch: refetchExams, isLoading: examsLoading, isError: examsError } = useQuery<Exam[], Error>({
        queryKey: ['exam', params.patientId],
        queryFn: () => client.examService.getAll(Number(params.patientId))
    });

    // This useEffect hook is executed when either exams or params.examId change
    React.useEffect( () => {
        if (params.examId && exams) {
            // Get the selected exam
            const exam = exams.filter( (exam) => exam.id === Number(params.examId))[0];
            // Set procedures if exam exists
            if (exam) {
                // console.log("Set procedures: ", exam.procedures)
                setProcedures(exam.procedures);
            }
        }
    }, [exams, params.examId])

    // This useEffect hook is executed when either exams or params.procedureId change
    React.useEffect( () => {
        if (params.procedureId && procedures) {
            // Get the selected exam
            const procedure = procedures.filter( (procedure) => procedure.id === Number(params.procedureId))[0];
            // Set procedures if exam exists
            if (procedure) {
                // console.log("Set jobs: ", procedure.jobs)
                setJobs(procedure.jobs);
            }
        }
    }, [procedures, params.procedureId])

    // Mutations to create exam and procedure
    const createExam = useMutation( async(newExam: Exam) => {
        await client.examService.create(newExam)
        .then( () => { refetchExams() })
        .catch((err) => { console.log("Error on exam creation: ", err) }) 
    })

    const createProcedure = useMutation( async(newProcedure: Procedure) => {
        await client.procedureService.create(newProcedure)
        .then( () => { refetchExams() })
        .catch((err) => { console.log("Error on procedure creation: ", err)})
    })

    return (    
        <div 
            id="page-container" 
            style={{ 
                width: '100%', 
                position: 'relative', 
                height: `calc(100vh - ${navigation.height})`
            }}
        >
            <Drawer
                sx={{
                    width: patientView.drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: patientView.drawerWidth,
                    }
                }}
                PaperProps={{ style: { position: 'absolute' } }}
                // BackdropProps={{ style: { position: 'absolute' } }}
                ModalProps={{
                    container: document.getElementById('page-container'),
                    style: { position: 'absolute' }
                }}
                variant="persistent"
                anchor="left"
                open={sidePanelOpen}
            >
                <Box sx={{ overflow: 'auto', bgcolor: 'background.componentBg' }}>

                    {/* Conditional rendering: Only rendered if patient exists */}
                    { patient && <PatientInfo patient={patient} isLoading={patientLoading} isError={patientError}/> }
                    
                    <ListDivider />
                    
                    {/* Exam list header */}
                    <Box sx={{ p: 1.5, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                        <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                            <Typography level="h5"> Exams </Typography>
                            <Badge badgeContent={exams?.length} color="primary"/>
                        </Box>
            
                        <Box sx={{ display: 'flex', gap: 1 }}>
                            <IconButton 
                                variant='soft'
                                sx={{ "--IconButton-size": patientView.iconButtonSize }}
                                onClick={() => setExamModalOpen(true)}
                            >
                                <AddSharpIcon/>
                            </IconButton>
                        </Box>

                        <ExamModal 
                            // When data is null, modal fills data in new empty procedure 
                            data={ null }
                            dialogOpen={ examModalOpen }
                            setDialogOpen={ setExamModalOpen }
                            handleModalSubmit={ (data: Exam) => { createExam.mutate(data)} }
                        />

                    </Box>

                    <ListDivider />  

                    {/* List of exams */}
                    <List sx={{ pt: 0 }}>
                        {
                            // Check if exams are loading
                            exams?.map( (exam, index) => (
                                <React.Fragment key={index}>
                                    <ExamItem 
                                        data={ exam } 
                                        refetchParentData={ refetchExams } 
                                        isSelected={ exam.id === Number(params.examId) }
                                    />
                                    <ListDivider sx={{ m: 0 }} />
                                </React.Fragment>
                            ))
                        }
                    </List>
                </Box>

            </Drawer>

            <Main open={sidePanelOpen}>
                
                {/* List of procedures */}
                <Box sx={{ 
                    overflow: 'auto', 
                    minWidth: patientView.procedureListWidth, 
                    bgcolor: 'background.componentBg',
                    borderRight: '1px solid',
                    borderColor: 'divider',
                }}>

                    {/* Procedure header */}
                    <Box sx={{ p: 1.5, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                            <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                                <IconButton
                                    variant='soft'
                                    sx={{ "--IconButton-size": patientView.iconButtonSize }}
                                    onClick={() => { setSidePanelOpen(!sidePanelOpen) }}
                                >
                                    { sidePanelOpen ? <KeyboardArrowLeftSharpIcon /> : <KeyboardArrowRightSharpIcon/> }
                                </IconButton>

                                <Typography level="h5"> Procedures </Typography>

                                <Badge badgeContent={procedures?.length} color="primary"/>
                            </Box>
            
                            <IconButton 
                                variant='soft' 
                                sx={{ "--IconButton-size": patientView.iconButtonSize }}
                                onClick={() => {setProcedureModalOpen(true)}}
                            >
                                <AddSharpIcon/>
                            </IconButton>

                            <ProcedureModal
                                // When data is null, modal fills data in new empty procedure 
                                data={ null }
                                dialogOpen={ procedureModalOpen }
                                setDialogOpen={ setProcedureModalOpen }
                                // Refetch exams, once a new procedure is created:
                                // Procedures are extracted from selected exam by useEffect hook
                                // onSave={ refetchExams }
                                // onSave={ createProcedure }
                                handleModalSubmit={ () => {console.log("test")} }
                            />
                    </Box>

                    <ListDivider />

                    {/* List of procedures */}
                    <List sx={{ pt: 0 }}>
                        {
                            procedures?.map( (procedure, index) => (
                                <React.Fragment key={index}>
                                    <ProcedureItem 
                                        data={ procedure } 
                                        refetchParentData={ refetchExams } 
                                        isSelected={ procedure.id === Number(params.procedureId) }
                                    />
                                    <ListDivider sx={{ m: 0 }} />
                                </React.Fragment>
                            ))
                        }
                    </List>

                </Box>

                {/* job view controller */}
                <Box sx={{ width: '100%', bgcolor: 'background.componentBg' }}>
                    <JobView
                        // Implementation of new interface may be required
                        data={ jobs ? jobs : [] }
                        refetchParentData={ refetchExams }
                        isSelected={ params.procedureId ? true : false }
                    />
                </Box>

            </Main>
        </div>
    );      
}

export default PatientIndex;
