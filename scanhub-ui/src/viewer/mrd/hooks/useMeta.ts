import { useQuery } from '@tanstack/react-query';
import { resultApi } from '../../../api';
import { MRDMetaResponse } from '../../../openapi/generated-client/exam';

export function useMeta(enabled: boolean, workflowId: string, taskId: string, resultId: string) {
  return useQuery<MRDMetaResponse>({
    queryKey: ['raw-meta', workflowId, taskId, resultId],
    enabled: enabled,
    queryFn: async () => {
      const res = await resultApi.getMrdMeta(workflowId, taskId, resultId);
      return res.data
    },
    staleTime: Infinity,
  });
}
