import { useState, useEffect } from 'react';

function useHealthCheck(url: string, interval: number = 5000) {

    const [isReady, setIsReady] = useState(false);

    useEffect(() => {

    const intervalId = setInterval(() => {
        fetch(`${url}/health/readiness`).then(response => {
            response.status === 200 ? setIsReady(true) : setIsReady(false);
        })
        .catch(() => setIsReady(false));
    }, interval);

    return () => clearInterval(intervalId);

    }, [url, interval]);

    return isReady;
}

export default useHealthCheck;