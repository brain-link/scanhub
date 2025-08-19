declare module 'ndarray-fft' {
  import ndarray from 'ndarray';
  function fft(dir: 1 | -1, real: ndarray, imag: ndarray): void;
  export = fft;
}