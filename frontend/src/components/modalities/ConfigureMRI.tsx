// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// ConfigureMRI.tsx is responsible for configuring the MRI modality.

import type { ModalityProps } from './types'

export function ConfigureMRI({
  recordingId,
}: ModalityProps) {
  return (
    <>
      <h1>Configure MRI ({recordingId})</h1>
      <form>
        <div className="grid gap-2" style={{ ['--columns' as string]: 3 }}>
          <fieldset className="grid col-2 gap-2">
            <legend>Fieldset 1</legend>
            <label>
              <span>B1 Frequency <span role='unit'>MHz</span></span>
              <input name='b1FrequencyHz' type='number'></input>
            </label>
            <label>
              <span>Pulse Length <span role='unit'>µs</span></span>
              <input name='pulseLengthUs' type='number'></input>
            </label>
            <label>
              <span>90° Pulse Amplitude</span>
              <input name='pulseAmplitude90' type='number'></input>
            </label>
            <label>
              <span>180° Pulse Amplitude</span>
              <input name='pulseAmplitude180' type='number'></input>
            </label>
          </fieldset>
          <fieldset className="grid col-2 gap-2">
            <legend>Fieldset 2</legend>
            <label>
              <span>Read Phase 1</span>
              <input name='readPhase1' type='number'></input>
            </label>
            <label>
              <span>FoV Readout <span role='unit'>mm</span></span>
              <input name='fovReadout' type='number'></input>
            </label>
            <label>
              <span>FoV Phase 1 <span role='unit'>mm</span></span>
              <input name='fovPhase1' type='number'></input>
            </label>
            <label>
              <span>FoV Phase 2 <span role='unit'>mm</span></span>
              <input name='fovPhase2' type='number'></input>
            </label>
          </fieldset>
          <fieldset className="grid col-2 gap-2">
            <legend>Fieldset 3</legend>
            <label>
              <span>K-Space Trajectory</span>
              <input name='readPhase1' type='number'></input>
            </label>
            <label>
              <span>Phase 1 Step Count</span>
              <input name='phase1StepCount' type='number'></input>
            </label>
            <label>
              <span>Phase 2 Step Count</span>
              <input name='phase2StepCount' type='number'></input>
            </label>
            <label>
              <span>Oversampling</span>
              <input name='oversampling' type='number'></input>
            </label>
          </fieldset>
          <fieldset className="grid col-2 gap-2">
            <legend>Fieldset 4</legend>
            <label>
              <span>Repetition Time <span role='unit'>ms</span></span>
              <input name='repetitionTimeMs' type='number'></input>
            </label>
            <label>
              <span>Echo Time <span role='unit'>ms</span></span>
              <input name='echoTimeMs' type='number'></input>
            </label>
            <label>
              <span>Echo Train Length</span>
              <input name='echoTrainLength' type='number'></input>
            </label>
            <label>
              <span>Dummy Scan Count</span>
              <input name='dummyScanCount' type='number'></input>
            </label>
            <label>
              <span>Gradient Ramp Time <span role='unit'>ms</span></span>
              <input name='gradientRampTimeMs' type='number'></input>
            </label>
          </fieldset>
          <fieldset className="grid col-2 gap-2">
            <legend>Fieldset 5</legend>
            <label>
              <span>Rx Gain <span role='unit'>dB</span></span>
              <input name='rxGainDb' type='number'></input>
            </label>
            <label>
              <span>Rx Phase <span role='unit'>degrees</span></span>
              <input name='rxPhaseDeg' type='number'></input>
            </label>
            <label>
              <span>Complex Point Count</span>
              <input name='complexPointCount' type='number'></input>
            </label>
            <label>
              <span>Dwell Time <span role='unit'>µs</span></span>
              <input name='dwellTimeUs' type='number'></input>
            </label>
            <label>
              <span>Scan Count</span>
              <input name='scanCount' type='number'></input>
            </label>
          </fieldset>
        </div>
        <menu className="flex gap-2">
          <button>Save</button>
          <button>Duplicate</button>
          <button>Export</button>
        </menu>
      </form>
    </>
  )
}
