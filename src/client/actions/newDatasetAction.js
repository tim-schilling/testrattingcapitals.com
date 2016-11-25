// @flow

import { createAction } from 'redux-actions';

export const NEW_DATASET = 'NEW_DATASET';
export const newDataset = createAction(NEW_DATASET, data => data);

export const VNI_TICK = 'VNI_TICK';
export const vniTick = createAction(VNI_TICK);
