import * as React from 'react';
import { Alerts, AlertProps } from '../interfaces/components.interface';

import Typography from '@mui/joy/Typography';
import Alert from '@mui/joy/Alert';

import InfoIcon from '@mui/icons-material/Info';
import WarningIcon from '@mui/icons-material/Warning';
import ReportIcon from '@mui/icons-material/Report';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';



function AlertItem({title, type, info}: AlertProps) {

    function getIcon(alertType) {
        switch (alertType) {
            case Alerts.Danger:
                return <ReportIcon/>
            case Alerts.Success:
                return <CheckCircleIcon/>
            case Alerts.Warning:
                return <WarningIcon/>
            case Alerts.Neutral:
                return <InfoIcon/>
            default:
                return <InfoIcon/>
        }
    }
    
    return (
        <Alert
            key={ title }
            sx={{ alignItems: 'flex-start' }}
            startDecorator={ getIcon(type) }
            variant="soft"
            color={ type }
        >
            <div>
                <Typography level="title-md">{ title }</Typography>
                {
                    // info ? <Typography level="body-sm" color={ type }> { info }</Typography> : null
                    info ? <Typography level="body-sm" color={ type }> { info }</Typography> : null
                }
                
            </div>
        </Alert>
    )
}

export default AlertItem;
