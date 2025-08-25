import { ResultOut } from '../openapi/generated-client/exam'

/**
 * Extract run id from untyped dictionary
 * @param meta untyped dictionary which may contain run_id
 * @returns run_id as string if available, else null
 */
export function extractRunId(meta: unknown): string | null {
  if (meta && typeof meta === "object" && "run_id" in (meta as Record<string, unknown>)) {
    const v = (meta as Record<string, unknown>)["run_id"];
    return typeof v === "string" ? v : v != null ? String(v) : null;
  }
  return null;
}

/**
 * Get latest result from a list of ResultOut
 * @param results 
 * @returns latest result
 */
export function getLatestResult(results: ResultOut[]) {
  if (!results || results.length === 0) return null;

  if (!Array.isArray(results) || results.length === 0) return null;

  const latest = results.reduce((a: ResultOut, b: ResultOut) =>
    Date.parse(a.datetime_created) < Date.parse(b.datetime_created) ? b : a
  );

  return latest
}
