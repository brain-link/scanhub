import React from "react";

import {
    Card,
    CardContent,
    IconButton
} from "@mui/material"

export function Dashboard() {
    return (
        <>
            <Card className='m-4'>
                <CardContent className='m-2 text-center'>
                    <img src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg" width="400" height="200" alt="ScanHub"/>
                    <div className="mt-5">
                        <span><small>ScanHub &copy; 2022, Powered by BRAIN-LINK</small></span>
                        <IconButton href="https://www.brain-link.de/">
                            <img
                                src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
                                alt=""
                                height="30"
                                className="d-inline-block"
                            />
                        </IconButton>
                    </div>
                </CardContent>
            </Card>
        </>
    );
}