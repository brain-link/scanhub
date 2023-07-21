import * as React from 'react';

import { ModalProps } from '../interfaces/components.interface';
import { Exam } from '../interfaces/data.interface';

function ExamModal2(props: ModalProps<Exam>) {
    React.useEffect( () => {
        console.log(props)
    })
    return (
        <></>
    )
}

export default ExamModal2;