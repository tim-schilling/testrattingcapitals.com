// @flow

import moment from 'moment';
import { NEW_DATASET, VNI_TICK } from '../actions/newDatasetAction';

const parseNewDataset = (state, action) => {
  if (!action || !action.payload) {
    return state;
  }

  const { payload } = action;

  const newState = {};
  Object.keys(state).forEach((key) => {
    if ({}.hasOwnProperty.call(state, key) === true) {
      newState[key] = state[key];
    }
  });

  newState.capital = payload.capital;
  newState.vni = payload.vni;
  newState.lastUpdatedServer = moment(payload.lastUpdated);
  newState.lastUpdatedClient = moment();

  return newState;
};

const parseVniTick = (state, action) => {
  if (!action) {
    return state;
  }

  const newState = {};
  Object.keys(state).forEach((key) => {
    if ({}.hasOwnProperty.call(state, key) === true) {
      newState[key] = state[key];
    }
  });

  return newState;
};

const initialState = {};

const newDatasetReducer = (state: Object = initialState, action: Object) => {
  let result = state;

  switch (action.type) {
    case NEW_DATASET:
      result = parseNewDataset(state, action);
      break;
    case VNI_TICK:
      result = parseVniTick(state, action);
      break;
    default:
      break;
  }

  return result;
};

export default newDatasetReducer;
