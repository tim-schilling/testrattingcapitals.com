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
import * as moment from 'moment';
import React, { Component } from 'react';

import './LatestTrackedKillComponent.css';

const ZKILLBOARD_BASE_URL = process.env.REACT_APP_ZKILLBOARD_BASE_URL || '';
const TIMEDIFF_INTERVAL_TICKRATE = process.env.REACT_APP_TIMEDIFF_RERENDER_TICK_RATE || 250;

export const timeSinceTimestamp = (timestamp) => {
  if (!timestamp) {
    return '';
  }

  const pluralize = (label, value) => (value === 1) ? `${label}` : `${label}s`;

  const now = moment.utc();
  const then = moment.utc(timestamp);

  const ms = now.diff(then);
  const duration = moment.duration(ms);

  const hours = Math.floor(duration.asHours());
  const hoursLabel = pluralize('hour', hours);
  const minutes = parseInt(moment.utc(ms).format('m'), 10);
  const minutesLabel = pluralize('minute', minutes);
  const seconds = parseInt(moment.utc(ms).format('s'), 10);
  const secondsLabel = pluralize('second', seconds);

  if (hours > 1) {
    return `${hours} ${hoursLabel}, ${minutes} ${minutesLabel}, and ${seconds} ${secondsLabel}`;
  } else if (minutes > 0) {
    return `${minutes} ${minutesLabel} and ${seconds} ${secondsLabel}`;
  } else {
    return `${seconds} ${secondsLabel}`;
  }
}

class LatestTrackedKillComponent extends Component {
  constructor(props) {
    super(props);
    const newState = {};

    // short circuit if no input
    if (!props) {
      this.state = newState;
      return;
    }

    // short circuit if fields are missing
    let requiredProps = [ 
      'trackingLabel',
      'trackingLabelDescription',
      'kill',
    ];

    for (let requiredProp of requiredProps) {
      if (!props.hasOwnProperty(requiredProp)) {

        this.state = newState;
        return;
      }
    }

    // short circuit if fields from killmail are missing
    requiredProps = [ 
      'kill_timestamp',
      'kill_id',
    ];

    for (let requiredProp of requiredProps) {
      if (!props.kill.hasOwnProperty(requiredProp)) {
        this.state = newState;
        return;
      }
    }

    // calc new state
    newState.trackingLabel = props.trackingLabel;
    newState.trackingLabelDescription = props.trackingLabelDescription;
    newState.killTimestamp = moment.utc(props.kill.kill_timestamp);
    newState.killUrl = `${ZKILLBOARD_BASE_URL}/kill/${props.kill.kill_id}`;
    newState.killTimediff = timeSinceTimestamp(newState.killTimestamp);

    this.state = newState;

    this.timediffInterval = setInterval(() => this.timediffIntervalTick(), parseInt(TIMEDIFF_INTERVAL_TICKRATE, 10));
  }

  timediffIntervalTick() {
    const newState = {}
    if (this.state && this.state.killTimestamp) {
      newState.trackingLabel = this.state.trackingLabel;
      newState.trackingLabelDescription = this.state.trackingLabelDescription;
      newState.killTimestamp = this.state.killTimestamp;
      newState.killUrl = this.state.killUrl;
      newState.killTimediff = timeSinceTimestamp(newState.killTimestamp);
    }
    this.setState(newState);
  }

  componentWillUnmount() {
    if (this.timediffInterval) {
      clearInterval(this.timediffInterval);
    }
  }

  render() {
    return (
      <div className="latestTrackedKillComponent">
        <p className="calloutMessage">It has been <em>{ this.state.killTimediff }</em> { this.state.trackingLabelDescription }</p>
        <p className="killUrl"><a href={ this.state.killUrl }>{ this.state.killUrl }</a></p>
      </div>
    );
  }
}

export default LatestTrackedKillComponent;
