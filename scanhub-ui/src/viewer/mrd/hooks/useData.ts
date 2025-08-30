import { useQuery } from '@tanstack/react-query';
import { resultApi } from '../../../api';
import { parsePacket, ParsedBatch, debugHeader } from '../utils/packet';
import type { AxiosRequestConfig } from 'axios';

export function useData(
  enabled: boolean, workflowId: string, taskId: string, resultId: string, idsExpr: string, coilsIdx?: number, stride = 1
) {
  const opts: AxiosRequestConfig = { responseType: 'arraybuffer' };
  return useQuery<ParsedBatch>({
    queryKey: ['raw-acq', workflowId, taskId, resultId, idsExpr, coilsIdx, stride],
    enabled: enabled,
    queryFn: async () => {
      const resp = await resultApi.getMRD(workflowId, taskId, resultId, idsExpr, coilsIdx, stride, opts);

      const buf: ArrayBuffer = (resp as any).data;
      debugHeader(buf);  // ← adds clarity in the console
      const batch = parsePacket(buf);

      if (!(buf instanceof ArrayBuffer)) {
        throw new Error('Expected ArrayBuffer from getMRD; check axios responseType and API method signature.');
      }
      
      // Optional: sanity check
      if (!Array.isArray(batch) || batch === undefined) {
        throw new Error('Parsed batch is not an array.');
      }
      
      return batch;
      
    },
    staleTime: 5 * 60_000,
  });
}
