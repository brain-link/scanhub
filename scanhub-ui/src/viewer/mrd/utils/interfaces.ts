export interface WorkerTrace {
  label: string;
  x: Float32Array;
  y: Float32Array;
}

export interface WorkerMessage {
  time: WorkerTrace[];
  freq: WorkerTrace[];
}
