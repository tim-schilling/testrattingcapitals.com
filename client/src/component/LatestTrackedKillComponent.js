import * as moment from 'moment';
import React, { Component } from 'react';

const ZKILLBOARD_BASE_URL = process.env.REACT_APP_ZKILLBOARD_BASE_URL || '';
const TIMEDIFF_INTERVAL_TICKRATE = process.env.REACT_APP_TIMEDIFF_RERENDER_TICK_RATE || 250;

export const timeSinceTimestamp = (timestamp) => {
  if (!timestamp) {
    return '';
  }

  const now = moment.utc();
  const then = moment.utc(timestamp);

  const ms = now.diff(then);
  const duration = moment.duration(ms);

  const hours = Math.floor(duration.asHours());
  const minutes = parseInt(moment.utc(ms).format('m'), 10);
  const seconds = parseInt(moment.utc(ms).format('s'), 10);

  if (hours > 0) {
    return `${hours} hours, ${minutes} minutes, and ${seconds} seconds`;
  } else if (minutes > 0) {
    return `${minutes} minutes and ${seconds} seconds`;
  } else {
    return `${seconds} seconds`;
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
      <div>
        <p>{ this.state.trackingLabel }</p>
        <p>{ this.state.trackingLabelDescription }</p>
        <p>{ moment(this.state.killTimestamp).format('YYYY-MM-DD HH:mm:ss') }</p>
        <p>{ this.state.killUrl }</p>
        <p>{ this.state.killTimediff }</p>
      </div>
    );
  }
}

export default LatestTrackedKillComponent;
