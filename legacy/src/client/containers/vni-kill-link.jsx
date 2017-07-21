// @flow

import { connect } from 'react-redux';

import KillLink from '../components/kill-link';

const mapStateToProps = (state) => {
  const result = {};

  if (state &&
    state.newDatasetReducer &&
    state.newDatasetReducer.vni &&
    state.newDatasetReducer.vni.killID
  ) {
    const dataSetState = state.newDatasetReducer;
    result.prefix = '';
    result.urlDisplay = `https://zkillboard.com/kill/${dataSetState.vni.killID}`;
    result.urlHref = result.urlDisplay;
    result.suffix = '';
  } else {
    result.prefix = '';
    result.urlDisplay = '';
    result.urlHref = '';
    result.suffix = '';
  }

  return result;
};

export default connect(mapStateToProps)(KillLink);
