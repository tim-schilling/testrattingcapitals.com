// @flow

import React, { PropTypes } from 'react';

const CalloutMessage = ({ prefix, emphasis, suffix }: Object) =>
  <div>
    <p>{prefix}<span className="capitalEmphasis">{emphasis}</span>{suffix}</p>
  </div>;

CalloutMessage.propTypes = {
  prefix: PropTypes.string.isRequired,
  emphasis: PropTypes.string.isRequired,
  suffix: PropTypes.string.isRequired,
};

export default CalloutMessage;
