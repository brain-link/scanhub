// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// DicomViewer.tsx is responsible for rendering the dicom viewer.

import React, { Component } from 'react';
import CornerstoneViewport from 'react-cornerstone-viewport';
import './ConerstoneInit';
// import get from 'lodash.get';

import axios from 'axios';
import config from '../../../utils/config';

type ViewerProps = {
  procedureId: string;
};

class DicomViewer extends Component<ViewerProps> {
  state = {
    tools: [
      // Mouse
      {
        name: 'Wwwc',
        mode: 'active',
        modeOptions: { mouseButtonMask: 1 },
      },
      {
        name: 'Zoom',
        mode: 'active',
        modeOptions: { mouseButtonMask: 2 },
      },
      {
        name: 'Pan',
        mode: 'active',
        modeOptions: { mouseButtonMask: 4 },
      },
      // Scroll
      { name: 'StackScrollMouseWheel', mode: 'active' },
      // Touch
      { name: 'PanMultiTouch', mode: 'active' },
      { name: 'ZoomTouchPinch', mode: 'active' },
      { name: 'StackScrollMultiTouch', mode: 'active' },
    ],
    imageIds: [],
    ready: false,
    procedureId: "",
  };

  static getDerivedStateFromProps(props: any, state: any) {
    return (state.procedureId = props.procedureId)
  }

  async find() {

    if (this.state.procedureId !== undefined){
      await axios.get(`${config.baseURL}/records/${this.state.procedureId}`)
      .then((response) => {
        if (response.data.data) {
          const res = "dicomweb:" + response.data.data

          // Set state with console log in callback
          // this.setState({ imageIds: [res], ready: true }, () => {console.log(this.state)});
          this.setState({ imageIds: [res], ready: true });  
        }
      })
    }
  }

  componentDidMount() {
    
    this.find();
  }

  componentDidUpdate(prevProps: any) {
    if (prevProps.procedureId !== this.props.procedureId) {
      this.find();
    }
  }

  render() {
    if (this.state.ready) {

      console.log(this.state)

      return (
        <CornerstoneViewport 
          tools={this.state.tools} 
          imageIds={this.state.imageIds} 
          style={{ minWidth: '100%', height: '100%', flex: '1' }} 
        />
      )
    } else {
      // TODO: Return circular loader here...
      return (
        <div>
          Loading...
        </div>
      );
    }
  }
}

export default DicomViewer;