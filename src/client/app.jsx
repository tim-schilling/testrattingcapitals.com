// @flow

import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, combineReducers } from 'redux';
import { Provider } from 'react-redux';

import { newDataset, vniTick } from './actions/newDatasetAction';
import newDatasetReducer from './reducers/newDatasetReducer';
import SimpleJsonRepository from './repositories/simpleJsonRepository';
import CapitalCalloutMessage from './containers/capital-callout-message';
import CapitalKillLink from './containers/capital-kill-link';
import VniCalloutMessage from './containers/vni-callout-message';
import VniKillLink from './containers/vni-kill-link';


const store = createStore(combineReducers({
  newDatasetReducer,
}));

SimpleJsonRepository.get('/data.json')
.then((data) => {
  store.dispatch(newDataset(data));
  setInterval(() => {
    store.dispatch(vniTick());
  }, 30);
}, (err) => {
  throw err;
});

ReactDOM.render(
  <Provider store={store}>
    <div className="container">
      <div className="row">
        <div className="col-xs-12 capitalCalloutMessage">
          <CapitalCalloutMessage />
        </div>
        <div className="col-xs-12 capitalCalloutMessage">
          <CapitalKillLink />
        </div>
      </div>
      <div className="row">
        <div className="col-xs-12 vniCalloutMessage">
          <VniCalloutMessage />
        </div>
        <div className="col-xs-12 capitalCalloutMessage">
          <VniKillLink />
        </div>
      </div>
    </div>
  </Provider>
   , document.querySelector('.app'),
);
