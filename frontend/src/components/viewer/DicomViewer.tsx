import React, { Component } from 'react';
import CornerstoneViewport from 'react-cornerstone-viewport';
// import get from 'lodash.get';

type MyProps = {
  studyUid: string;
  seriesUid: string;
};

class DicomViewer extends Component<MyProps> {
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
  };

  static getDerivedStateFromProps(props: any, state: any) {
    return (state.seriesUid = props.seriesUid);
  }

  find() {
    // const query = `${Config.hostname}:${Config.port}/${Config.qido}/studies/${this.props.studyUid}/series/${this.props.seriesUid}/instances`;
    // const imageQuery = `wadouri:${Config.hostname}:${Config.port}/${Config.wadouri}?studyUID=${this.props.studyUid}&seriesUID=${this.props.seriesUid}&objectUID=`;
    // fetch(query)
    //   .then((response) => response.json())
    //   .then((data) => {
    //     if (data) {
    //       const res = data.map((row: any, index: any) => imageQuery + get(row, '00080018.Value[0]', ''));
    //       this.setState({ imageIds: res, ready: true });
    //     }
    //   });
  }

  componentDidMount() {
    this.find();
  }
  componentDidUpdate(prevProps: any) {
    if (prevProps.seriesUid !== this.props.seriesUid) {
      this.find();
    }
  }

  render() {
    if (this.state.ready) {
      return <CornerstoneViewport tools={this.state.tools} imageIds={this.state.imageIds} style={{ minWidth: '100%', height: '512px', flex: '1' }} />;
    } else {
      return null;
    }
  }
}

export default DicomViewer;