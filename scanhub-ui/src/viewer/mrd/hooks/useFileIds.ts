// useFileIds.ts
import { useQuery } from '@tanstack/react-query';
import { taskApi } from '../../../api'; // your pre-configured OpenAPI client instance
import { TaskType } from '../../../openapi/generated-client/exam';

function normalizeToArray<T>(v: T | T[] | undefined | null): T[] {
  return Array.isArray(v) ? v : v != null ? [v] : [];
}

export type FileIds = {
  workflowId: string;
  taskId: string;
  resultId: string;
};

/**
 * Resolves workflowId, taskId, and resultId for a given taskId.
 * - Accepts any task that HAS results (doesn't force a specific TaskType).
 * - If multiple results exist, returns the newest by datetime_created (falls back to created_at / created).
 * - Throws a typed error when IDs are unavailable, so consumers can show a proper fallback.
 */
export function useFileIds(taskId?: string) {
  const {
    data,
    isLoading,
    isError,
    error,
  } = useQuery<FileIds>({
    queryKey: ['file-ids', taskId],
    enabled: !!taskId,
    staleTime: 5 * 60_000,
    queryFn: async () => {
      const { data } = await taskApi.getTaskApiV1ExamTaskTaskIdGet(taskId!);

      // Only DAG tasks with results
      const isAcquisition = data?.task_type === TaskType.Acquisition;
      const results = normalizeToArray<any>(data?.results);
      if (!isAcquisition || results.length === 0) {
        throw new Error('Task has no results.');
      }

      // Pick newest by datetime_created
      const latest = results.reduce((a, b) =>
        new Date(a?.datetime_created ?? 0) > new Date(b?.datetime_created ?? 0) ? a : b
      );

      const resultId = latest?.id ?? '';
      if (!resultId) throw new Error('Result is missing id.');
      const workflowId = data?.workflow_id ?? '';
      if (!workflowId) throw new Error('No workflow ID.');

      return {workflowId: String(workflowId), taskId: String(data.id), resultId: String(resultId)}
    },
  });

  return { fileIds: data, isLoading, isError, error };
}
