// src/viewer/dicom/hooks/useImageIds.ts
import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { taskApi } from '../../../api';
import { TaskType } from '../../../openapi/generated-client/exam';


function normalizeToArray<T>(v: T | T[] | undefined | null): T[] {
  return Array.isArray(v) ? v : v != null ? [v] : [];
}


/**
 * Fetches the latest result's 'instances' from a task, and maps them to Cornerstone3D imageIds.
 * - Accepts a taskId
 * - Returns { imageIds, isVolumeCandidate, isLoading, isError }
 * - Uses 'wado-uri:' scheme per Cornerstone v3 docs
 */
export function useImageIds(taskId?: string) {
  
  const { 
    data: dicomUrls = [],
    isLoading,
    isError
  } = useQuery<string[]>({
    queryKey: ['tasks', taskId],
    enabled: !!taskId,
    queryFn: async () => {
      const { data } = await taskApi.getTaskApiV1ExamTaskTaskIdGet(taskId!);

      // Only DAG tasks with results
      const isDag = data?.task_type === TaskType.Dag;
      const results = normalizeToArray<any>(data?.results);
      if (!isDag || results.length === 0) return [];

      // Pick newest by datetime_created
      const latest = results.reduce((a, b) =>
        new Date(a?.datetime_created ?? 0) > new Date(b?.datetime_created ?? 0) ? a : b
      );

      const instances = (latest?.meta as any)?.instances;
      const urls = normalizeToArray<string>(instances).filter(Boolean);

      // Ensure correct order by sorting urls, i.e. numeric suffixes in filenames
      urls.sort();
      return urls;
    },
  });

  const imageIds = useMemo(
    () => dicomUrls.map((u) => (u.startsWith('wadouri:') ? u : `wadouri:${u}`)),
    [dicomUrls]
  );

  return { imageIds, isLoading, isError };
}
