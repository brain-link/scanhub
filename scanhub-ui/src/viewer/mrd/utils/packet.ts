// Tiny parser for the custom binary packet returned by /raw/acq
export type ParsedAcq = {
  acqId: number;
  nCoils: number;
  nSamples: number;
  data: Float32Array; // interleaved [re,im] per coil, contiguous by coil
};
export type ParsedBatch = ParsedAcq[];

// safer parse with diagnostics
export function parsePacket(buf: ArrayBuffer): ParsedBatch {
  if (!buf || buf.byteLength < 8) {
    throw new Error(`Packet too small: ${buf?.byteLength ?? 0} bytes`);
  }

  const dv = new DataView(buf);
  let off = 0;

  const magic = dv.getUint32(off, true); off += 4;
  const ver   = dv.getUint16(off, true); off += 2;
  const nHdr  = dv.getUint16(off, true); off += 2;

  if (magic !== 0x49534d52) {
    throw new Error(`Bad magic: 0x${magic.toString(16)} (len=${buf.byteLength})`);
  }
  if (ver !== 1) {
    throw new Error(`Unsupported version: ${ver}`);
  }
  if (nHdr === 0) return []; // header-only packet → no acquisitions

  const out: ParsedBatch = [];
  for (let i = 0; i < nHdr; i++) {
    // ensure enough bytes for acq header
    if (off + 4 + 2 + 2 + 4 + 4 > dv.byteLength) {
      throw new Error(`Truncated at acq ${i}: need 16 header bytes, have ${dv.byteLength - off}`);
    }
    const acqId     = dv.getUint32(off, true); off += 4;
    const nCoils    = dv.getUint16(off, true); off += 2;
    const dtypeCode = dv.getUint16(off, true); off += 2;
    const nSamples  = dv.getUint32(off, true); off += 4;
    const byteLen   = dv.getUint32(off, true); off += 4;

    if (dtypeCode !== 1) throw new Error(`Unsupported dtype code: ${dtypeCode}`);
    if (off + byteLen > dv.byteLength) {
      throw new Error(`Truncated payload for acq ${acqId}: need ${byteLen}, have ${dv.byteLength - off}`);
    }

    const slice = buf.slice(off, off + byteLen);
    off += byteLen;
    out.push({ acqId, nCoils, nSamples, data: new Float32Array(slice) });
  }
  return out;
}

// optional: quick hex dump for debugging
export function debugHeader(buf: ArrayBuffer) {
  const dv = new DataView(buf);
  const magic = dv.byteLength >= 4 ? dv.getUint32(0, true) : 0;
  const ver   = dv.byteLength >= 6 ? dv.getUint16(4, true) : 0;
  const nHdr  = dv.byteLength >= 8 ? dv.getUint16(6, true) : 0;
  console.log(`[packet] len=${buf.byteLength} magic=0x${magic.toString(16)} ver=${ver} nHdr=${nHdr}`);
}
