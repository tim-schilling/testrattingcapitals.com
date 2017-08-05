import React, { Component } from 'react';
import { getLatestTrackedKills } from '../repository/LatestTrackedKillRepository';

import LatestTrackedKillComponent from './LatestTrackedKillComponent';

const PROCESS_ALL = process.env.REACT_APP_PROCESS_ALL ? true : false;

const TRACKING_KEY_DETAIL_MAP = {
  'ALL': {
      trackingLabel: 'All kills',
      trackingLabelDescription: 'since a kill has happened somewhere in EVE.'
  },
  'BAD_DRAGON_DEPLOYMENT': {
    trackingLabel: 'Bad Dragon Deployment Deserter',
    trackingLabelDescription: 'since a TEST member has died in shame alone in the South, not helping his alliance deployed in the North.',
  },
  'RATTING_CAPITAL': {
    trackingLabel: 'Ratting Capital',
    trackingLabelDescription: 'since a ratting capital has died.',
  },
  'VNI': {
      trackingLabel: 'Vexor Navy Issue',
      trackingLabelDescription: 'since a Vexor Navy Issue has died.',
  },
};

if (PROCESS_ALL) {
  TRACKING_KEY_DETAIL_MAP.ALL = {
      trackingLabel: 'All kills',
      trackingLabelDescription: 'since a kill has happened somewhere in EVE.'
  }
}

class AppComponent extends Component {
  constructor(props) {
    super(props)
    this.state = {};

    const self = this;
    getLatestTrackedKills()
    .then((response) => {
      const newState = {};
      for (let trackingKey in TRACKING_KEY_DETAIL_MAP) {
        if (TRACKING_KEY_DETAIL_MAP.hasOwnProperty(trackingKey) && 
            response.hasOwnProperty(trackingKey) && response[trackingKey]['kill']) {
          newState[trackingKey] = {
            trackingLabel: TRACKING_KEY_DETAIL_MAP[trackingKey].trackingLabel,
            trackingLabelDescription: TRACKING_KEY_DETAIL_MAP[trackingKey].trackingLabelDescription,
            kill: response[trackingKey].kill,
          }
        }
      }
      self.setState(newState);
    }, (ex) => {
      console.warn(':frogsiren:', ex);
      // TODO show something meaningful to the user
    })
  }


  render() {
    return (
      <div className="container">
        {Object.keys(this.state).map((key) => {
          const val = this.state[key];
          return (
            <div className="row" key={key}>
              <div className="col-xs-12">
                <LatestTrackedKillComponent  {...val} />
              </div>
            </div>
          );
        })}
      </div>
    );
  }
}

export default AppComponent;
