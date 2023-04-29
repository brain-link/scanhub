import * as React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { useMutation } from 'react-query';

// Mui joy components
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import Menu from '@mui/joy/Menu';
import MenuItem from '@mui/joy/MenuItem';
import IconButton from '@mui/joy/IconButton';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
// import FilterCenterFocusSharpIcon from '@mui/icons-material/FilterCenterFocusSharp';
import DescriptionSharpIcon from '@mui/icons-material/DescriptionSharp';

// Interfaces and api service
import { Procedure } from '../interfaces/data.interface'; 
import { ItemComponentProps } from '../interfaces/components.interface';
import { ProcedureApiService } from '../client/queries';


function ProcedureItem({data: procedure, onDelete, isSelected}: ItemComponentProps<Procedure>) {

    const params = useParams();
    const navigate = useNavigate();

    const procedureClient = new ProcedureApiService();

    // Context: Delete and edit options, anchor for context location
    const [contextOpen, setContextOpen] = React.useState<number | null>(null);
    const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);


    const handleContextClose = () => {
        setAnchorEl(null);
        setContextOpen(null);
    }

    const handleContextOpen = (e, procedureId) => {
        e.preventDefault();
        setAnchorEl(e.currentTarget);
        setContextOpen(procedureId);
    }

    const deleteProcedureById = useMutation(async (id: number) => {
        await procedureClient.delete(id)
        .then(() => {
            if (Number(params.examId) === id) {
                // Reset router path if this exam id is in the path
                navigate(`/patients/${params.patientId}/${params.examId}`)
            }
            onDelete(); 
        })
    })


    return (
        <ListItem>
            <ListItemButton 
                id="procedure-item"
                component={ RouterLink }
                // If procedureId exists, we redirect to this procedure id, otherwise procedure id is appended
                to={ `/patients/${params.patientId}/${params.examId}/${procedure.id}` }
                selected={ isSelected }
                variant={( isSelected || procedure.id === contextOpen) ? "soft" : "plain" }
            >
                <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                    <DescriptionSharpIcon />
                </ListItemDecorator>

                <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%'}}>

                    <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                        <Typography>{procedure.name}</Typography>
                        <IconButton 
                            variant='plain' 
                            sx={{ "--IconButton-size": "25px" }}
                            onClick={ (e) => handleContextOpen(e, procedure.id) }
                        >
                            <MoreHorizIcon />
                        </IconButton>
                    </Box>

                    <Typography level="body2" textColor="text.tertiary">{ `Created: ${new Date(procedure.datetime_created).toDateString()}` }</Typography>
                    <Typography level="body2" textColor="text.tertiary">{ `Updated: ${procedure.datetime_updated ? new Date(procedure.datetime_updated).toDateString() : '-'}` }</Typography>
                </Box>

                <Menu   
                    id='context-menu'
                    variant='plain'
                    anchorEl={anchorEl}
                    open={procedure.id === contextOpen}
                    onClose={() => handleContextClose()}
                    sx={{ zIndex: 'snackbar' }}
                >
                    <MenuItem key='edit' onClick={() => { console.log('To be implemented...') }}>
                        Edit
                    </MenuItem>
                    <MenuItem key='delete' onClick={() => { deleteProcedureById.mutate(procedure.id) }}>
                        Delete
                    </MenuItem>
                </Menu>
                
            </ListItemButton>  
        </ListItem>
    );  
}

export default ProcedureItem;