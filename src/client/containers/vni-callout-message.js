// @flow

import moment from 'moment';
import { connect } from 'react-redux';

import CalloutMessage from '../components/callout-message';

const mapStateToProps = (state) => {
  const result = {};

  if (state &&
    state.newDatasetReducer &&
    state.newDatasetReducer.vni &&
    state.newDatasetReducer.vni.killTime
  ) {
    const dataSetState = state.newDatasetReducer;
    const now = moment();
    const then = moment.utc(dataSetState.vni.killTime, 'YYYY-MM-DD HH:mm:ss');

    const ms = now.diff(then);
    const duration = moment.duration(ms);

    const hours = Math.floor(duration.asHours());
    const minutes = parseInt(moment.utc(ms).format('m'), 10);
    const seconds = parseInt(moment.utc(ms).format('s'), 10);

    result.prefix = 'It has been  ';
    if (hours > 0) {
      result.emphasis = `${hours} hours, ${minutes} minutes, and ${seconds} seconds`;
    } else if (minutes > 0) {
      result.emphasis = `${minutes} minutes and ${seconds} seconds`;
    } else {
      result.emphasis = `${seconds} seconds`;
    }
    result.suffix = ' since a TEST ratting VNI died.';
  } else {
    result.prefix = '';
    result.emphasis = '';
    result.suffix = '';
  }

  return result;
};

export default connect(mapStateToProps)(CalloutMessage);
