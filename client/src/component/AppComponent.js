import React, { Component } from 'react';
import { getLatestTrackedKills } from '../repository/LatestTrackedKillRepository';

import LatestTrackedKillComponent from './LatestTrackedKillComponent';

const TRACKING_KEY_DETAIL_MAP = {
  'ALL': {
      trackingLabel: 'All kills',
      trackingLabelDescription: 'Any kill that has happened anywhere to anyone.'
  },
  'BAD_DRAGON_DEPLOYMENT': {
    trackingLabel: 'Bad Dragon Deployment Deserter',
    trackingLabelDescription: 'Any loss in our home region while we are at war and deployed abroad. A most shameful display.',
  },
  'RATTING_CAPITAL': {
    trackingLabel: 'Ratting Capital',
    trackingLabelDescription: '$40 - $3500 ships that take years to train into.',
  },
  'VNI': {
      trackingLabel: 'Vexor Navy Issue',
      trackingLabelDescription: 'The most common ratting subcapital in the game. Low income alone, but easy to get into and scales well.',
  },
};

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
      <div>
        {Object.keys(this.state).map((key) => {
          const val = this.state[key];
          return <LatestTrackedKillComponent key={key} {...val} />;
        })}
      </div>
    );
  }
}

export default AppComponent;
