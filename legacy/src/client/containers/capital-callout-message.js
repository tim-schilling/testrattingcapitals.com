// @flow

import moment from 'moment';
import { connect } from 'react-redux';

import CalloutMessage from '../components/callout-message';

const mapStateToProps = (state) => {
  const result = {};

  if (state &&
    state.newDatasetReducer &&
    state.newDatasetReducer.capital &&
    state.newDatasetReducer.capital.killTime
  ) {
    const dataSetState = state.newDatasetReducer;
    const now = moment();
    const then = moment.utc(dataSetState.capital.killTime, 'YYYY-MM-DD HH:mm:ss');
    const diff = now.diff(then, 'days');

    const days = (diff === 1) ? 'day' : 'days';

    result.prefix = 'It has been';
    result.emphasis = ` ${diff} `;
    result.suffix = `${days} since a TEST ratting capital died.`;
  } else {
    result.prefix = '';
    result.emphasis = '';
    result.suffix = '';
  }

  return result;
};

export default connect(mapStateToProps)(CalloutMessage);
