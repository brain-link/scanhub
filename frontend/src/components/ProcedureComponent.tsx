import * as React from 'react';
import Box from '@mui/joy/Box';
import Typography from '@mui/joy/Typography';
import List from '@mui/joy/List';
import ListDivider from '@mui/joy/ListDivider';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import DocumentScannerOutlinedIcon from '@mui/icons-material/DocumentScannerOutlined';
import ContentPasteSharpIcon from '@mui/icons-material/ContentPasteSharp';

const data = [
  {
    id: 0,
    date: '21 Oct 2021',
    reason: 'Details for Yosemite Park',
    records: 5,
  },
  {
    id: 1,
    date: '3 Feb 2022',
    reason: 'Tickets for upcoming trip',
    records: 1,
  },
  {
    id: 2,
    date: '16 May 2022',
    reason: 'Brunch this Saturday?',
    records: 0,
  },
];

// const MyListItem = withStyles({
//     root: {
//       "&$selected": {
//         backgroundColor: "red",
//         color: "white",
//         "& .MuiListItemIcon-root": {
//           color: "white"
//         }
//       },
//       "&$selected:hover": {
//         backgroundColor: "purple",
//         color: "white",
//         "& .MuiListItemIcon-root": {
//           color: "white"
//         }
//       },
//       "&:hover": {
//         backgroundColor: "blue",
//         color: "white",
//         "& .MuiListItemIcon-root": {
//           color: "white"
//         }
//       }
//     },
//     selected: {}
// })(ListItem);

export default function Procedures() {

    const [activeElement, setActiveElement] = React.useState(0)

    const updateActiveElement = (id) => {
        setActiveElement(activeElement !== id ? id : -1)
    }

    return (
        <List sx={{ pt: 0 }}>
            {data.map((item, index) => (
                <React.Fragment key={index}>

                    <ListItem>
                        <ListItemButton 
                            selected={activeElement === item.id}
                            onClick={() => setActiveElement(item.id)}
                            variant={activeElement === item.id ? "soft" : "plain"}
                        >

                            <ListItemDecorator sx={{ align: 'center', justify: 'center'}}>
                                <ContentPasteSharpIcon />
                            </ListItemDecorator>
                            <Box sx={{ display: 'flex', flexDirection: 'column'}}>
                                <Typography level="body2" textColor="text.tertiary">{item.date}</Typography>
                                <Typography>{item.reason}</Typography>
                                <Typography level="body2" textColor="text.tertiary">Records: {item.records}</Typography>
                            </Box>
                            
                        </ListItemButton>   
                    </ListItem>

                    <ListDivider sx={{ m: 0 }} />
                </React.Fragment>
            ))}
        </List>
    );  
}
