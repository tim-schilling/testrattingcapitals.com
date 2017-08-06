/*
  Copyright (c) 2016-2017 Tony Lechner and contributors

  testrattingcapitals.com is free software: you can redistribute it and/or
  modify it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, either version 3 of the
  License, or (at your option) any later version.

  testrattingcapitals.com is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with testrattingcapitals.com.  If not, see
  <http://www.gnu.org/licenses/>.
*/
import React, { Component } from 'react';
import { getLatestTrackedKills } from '../repository/LatestTrackedKillRepository';

import LatestTrackedKillComponent from './LatestTrackedKillComponent';

const PROCESS_ALL = process.env.REACT_APP_PROCESS_ALL ? true : false;
const TICK_RATE = parseInt(process.env.REACT_APP_TICK_RATE || 5000, 10);

const TRACKING_KEY_DETAIL_MAP = {
  'BAD_DRAGON_DEPLOYMENT': {
    trackingLabel: 'Bad Dragon Deployment Deserter',
    trackingLabelDescription: 'since a TEST member has died in shame alone in the South, not helping his alliance deployed in the North.',
  },
  'RATTING_CAPITAL': {
    trackingLabel: 'Ratting Capital',
    trackingLabelDescription: 'since a TEST ratting capital has died.',
  },
  'VNI': {
      trackingLabel: 'Vexor Navy Issue',
      trackingLabelDescription: 'since a TEST Vexor Navy Issue has died.',
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
    this.updateInterval = setInterval(() => {
      return self.tick();
    }, TICK_RATE);

    this.tick();
  }

  componentWillUnmount() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
  }

  tick() {
    const self = this;
    return getLatestTrackedKills()
    .then(response => self.digestLatestPayload(response), (ex) => {
      console.warn(':frogsiren:', ex);
      throw ex;
      // TODO show something meaningful to the user
    })
    .then((newState) => self.setState(newState));
  };

  digestLatestPayload(response) {
    return new Promise((resolve) => {
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
      return resolve(newState);
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
