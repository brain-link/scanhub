import * as React from 'react';
import { useMutation } from 'react-query';
import axios from 'axios';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import DocumentScannerOutlinedIcon from '@mui/icons-material/DocumentScannerOutlined';
import ContentPasteSharpIcon from '@mui/icons-material/ContentPasteSharp';
import AddSharpIcon from '@mui/icons-material/AddSharp';
import IconButton from '@mui/joy/IconButton';
import Divider from '@mui/material/Divider';
import Badge from '@mui/material/Badge';

import { Procedure } from './Interfaces';


export default function Procedures(context: any ) {

    const [activeElement, setActiveElement] = React.useState(0)

    // TODO: Procedures and records fetch, fetch in sub component!
    // Is this single procedure variable necessary?
    const [procedure, setProcedure] = React.useState<Procedure>({ id: 0, patient_id: 0, reason: "", date: "" });
    const [procedures, setProcedures] = React.useState<Procedure[] | undefined>(undefined);

    // Define fetch function for procedures table
    async function fetchProcedures () {
        await axios.get(context.procedureURL).then((response) => {
            setProcedures(response.data)
            if (response.data && response.data.length > 0) {
                setActiveElement(response.data.at(0).id)
            }
        })
    };

    // fetch procedures
    React.useEffect(() => {
        fetchProcedures();
    }, []);

    const mutation = useMutation(async() => {
        await axios.post(`${context.procedureURL}/new/`, procedure)
        .then((response) => {
            setProcedure(response.data) // required?
            fetchProcedures()
        })
        .catch((err) => {
            console.log(err)
        })
    })

    // procedures && procedures.length > 0 ? setActiveElement(procedures[0]?.id) : () => {}

    return (
        <Box>
            <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            
                <Box sx={{display: 'flex', alignItems: 'center', gap: 3}}>
                    <Typography level="h5">Records</Typography>
                    <Badge badgeContent={procedures?.length} color="primary"/>
                </Box>

                <IconButton size='sm' variant='outlined'>
                    <AddSharpIcon />
                </IconButton>

            </Box>
                
            <Divider />

            <List sx={{ pt: 0 }}>
                {procedures?.map((procedure, index) => (
                    <React.Fragment key={index}>

                        <ListItem>
                            <ListItemButton 
                                selected={activeElement === procedure.id}
                                onClick={() => setActiveElement(procedure.id)}
                                variant={activeElement === procedure.id ? "soft" : "plain"}
                            >

                                <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                                    <ContentPasteSharpIcon />
                                </ListItemDecorator>
                                <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                                    <Typography level="body2" textColor="text.tertiary">{procedure.id}</Typography>
                                    <Typography>{procedure.reason}</Typography>
                                    <Typography level="body2" textColor="text.tertiary">Records: {procedure.date}</Typography>
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
