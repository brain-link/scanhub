import * as React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import { useMutation } from 'react-query';

import Skeleton from '@mui/material/Skeleton';

import Card from '@mui/joy/Card';
import CardContent from '@mui/joy/CardContent';
import CardOverflow from '@mui/joy/CardOverflow';
import Typography from '@mui/joy/Typography';
import Divider from '@mui/joy/Divider';
import AspectRatio from '@mui/joy/AspectRatio';

import { Job } from '../../interfaces/data.interface'; 
import { ItemComponentProps } from '../../interfaces/components.interface';
import { JobApiService } from '../../client/queries';


function JobItem ({data: job, onDelete, isSelected}: ItemComponentProps<Job>) {


    const params = useParams();

    return (
        <Card
            orientation="horizontal"
            variant="outlined"
            sx={{ width: 260, bgcolor: 'background.body' }}
        >
            <CardOverflow>
                <AspectRatio ratio="1" sx={{ width: 90 }}>
                    <Skeleton variant="rectangular" width='100%' height='100%' />
                </AspectRatio>
            </CardOverflow>

            <CardContent sx={{ px: 2 }}>

                <Typography fontWeight="md" textColor="success.plainColor" mb={0.5}>
                    { job.type }
                </Typography>
                <Typography level="body2">
                    { job.comment }
                </Typography>

            </CardContent>
        </Card>
    );
}

export default JobItem;