import { useQuery } from '@tanstack/react-query';
import { resultApi } from '../../../api';
import { MRDMetaResponse } from '../../../openapi/generated-client/protocol';

export function useMeta(enabled: boolean, protocolId: string, taskId: string, resultId: string) {
  return useQuery<MRDMetaResponse>({
    queryKey: ['raw-meta', protocolId, taskId, resultId],
    enabled: enabled,
    queryFn: async () => {
      const res = await resultApi.getMrdMeta(protocolId, taskId, resultId);
      return res.data
    },
    staleTime: Infinity,
  });
}
