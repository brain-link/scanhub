// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// PatientIndex.tsx is responsible for rendering the patient view. It is the entry point for the patient view.

import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { useMutation } from 'react-query';

// Mui Joy
import Box from '@mui/joy/Box';
import Stack from '@mui/joy/Stack';
import List from '@mui/joy/List';
import Badge from '@mui/joy/Badge';
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
import JobList from '../components/JobList';
import ExamModal from '../components/ExamModal';
import ProcedureModal from '../components/ProcedureModal';

// Import interfaces, api services and global variables
import { Patient } from '../interfaces/data.interface';
import { Exam } from '../interfaces/data.interface';
import { Procedure } from '../interfaces/data.interface';
import { Job } from '../interfaces/data.interface';
import { patientView, navigation } from '../utils/size_vars';

import client from '../client/exam-tree-queries';


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
        .catch((err) => { console.log('Error on exam creation: ', err) }) 
    })

    const createProcedure = useMutation( async(data: Procedure) => {
        await client.procedureService.create(data)
        .then( () => { refetchExams() })
        .catch((err) => { console.log('Error on procedure creation: ', err)})
    })

    return (    

        <Stack direction="row" sx={{ height: `calc(100vh - ${navigation.height})`, width: '100%' }}>

            <Box sx={{ 
                minWidth: sidePanelOpen ? patientView.drawerWidth : 0,
                width: sidePanelOpen ? patientView.drawerWidth : 0,
                overflow: 'auto', 
                bgcolor: 'background.componentBg', 
                borderRight: '1px solid',
                borderColor: 'divider'
            }}>

                {/* Conditional rendering: Only rendered if patient exists */}
                { patient && <PatientInfo patient={patient} isLoading={patientLoading} isError={patientError}/> }
                
                <ListDivider />
                
                {/* Exam list header */}
                <Box sx={{ p: 1.5, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                        
                    <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                        <Typography level="title-md"> Exams </Typography>
                        <Badge badgeContent={exams?.length} color="primary"/>
                    </Box>
        
                    <Box sx={{ display: 'flex', gap: 1 }}>
                        <IconButton 
                            variant='soft'
                            sx={{ '--IconButton-size': patientView.iconButtonSize }}
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

            <Stack direction="row" sx={{ width: '100%' }}>
                
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
                                    sx={{ '--IconButton-size': patientView.iconButtonSize }}
                                    onClick={() => { setSidePanelOpen(!sidePanelOpen) }}
                                >
                                    { sidePanelOpen ? <KeyboardArrowLeftSharpIcon /> : <KeyboardArrowRightSharpIcon/> }
                                </IconButton>

                                <Typography level="title-md"> Procedures </Typography>

                                <Badge badgeContent={procedures?.length} color="primary"/>
                            </Box>
            
                            <IconButton 
                                variant='soft' 
                                sx={{ '--IconButton-size': patientView.iconButtonSize }}
                                onClick={() => {setProcedureModalOpen(true)}}
                                disabled={ params.examId === undefined }
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

            </Stack>
        </Stack>
    );      
}

export default PatientIndex;
