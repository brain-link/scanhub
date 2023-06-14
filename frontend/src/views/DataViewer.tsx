import * as React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';

import client from '../client/exam-tree-queries';
import { Job } from '../interfaces/data.interface';
import SequenceViewer from '../components/viewer/SequenceViewer';
import { SequenceViewerProps } from '../interfaces/components.interface';

function Viewer () {

    const params = useParams();

    // TODO: Pass job here, any (data) viewer needs access to either 
    // data, which is linked in the job itself or from the record (which can be fetched from job)

    // useQuery for caching the fetched data
    const { data: job, refetch: refetchJob, isLoading: jobLoading, isError: jobError } = useQuery<Job, Error>({
        queryKey: ['job', params.jobId], 
        queryFn: () => client.jobService.get(Number(params.jobId))
    });

    React.useEffect(() => {
        console.log(job)
    }, [job])
    

    switch (params.viewId) {
        default:
            return (
                <div>Invalid view ID</div>
            )

        case 'seq':
            if (!job?.sequence_id) {
                <div>Error: No sequence id</div>
            }
            else {
                return (
                    <SequenceViewer sequence_id={ job.sequence_id } />
                )
            }
    }

}

export default Viewer;