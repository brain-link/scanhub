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
import JobList from '../components/jobs/JobList';
import ExamModal from '../components/ExamModal';
import ProcedureModal from '../components/ProcedureModal';

// Import interfaces, api services and global variables
import { Patient } from '../interfaces/data.interface';
import { Exam } from '../interfaces/data.interface';
import { Procedure } from '../interfaces/data.interface';
import { Job } from '../interfaces/data.interface';
import { patientView, navigation } from '../utils/size_vars';

import client from '../client/exam-tree-queries';


const Main = styled('div', { shouldForwardProp: (prop) => prop !== 'open' }) <{ open?: boolean }>
(
    ({ theme, open }) => (
        {
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

    // Modal states for exam and procedure
    const [examModalOpen, setExamModalOpen] = React.useState(false);
    const [procedureModalOpen, setProcedureModalOpen] = React.useState(false);

    const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);
    const [jobs, setJobs] = React.useState<Job[] | undefined>(undefined);

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
                setJobs(procedure.jobs);
            }
        }
    }, [procedures, params.procedureId])

    // Mutations to create exam and procedure
    const createExam = useMutation( async(data: Exam) => {
        await client.examService.create(data)
        .then( () => { refetchExams() })
        .catch((err) => { console.log("Error on exam creation: ", err) }) 
    })

    const createProcedure = useMutation( async(data: Procedure) => {
        await client.procedureService.create(data)
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
                                handleModalSubmit={ (data: Procedure) => { createProcedure.mutate(data)} }
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
                    <JobList
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
