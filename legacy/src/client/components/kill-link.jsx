// @flow

import React, { PropTypes } from 'react';

const KillLink = ({ prefix, urlHref, urlDisplay, suffix }: Object) =>
  <div className="killLink">
    <p>{prefix}<a href={urlHref}>{urlDisplay}</a>{suffix}</p>
  </div>;

KillLink.propTypes = {
  prefix: PropTypes.string.isRequired,
  urlHref: PropTypes.string.isRequired,
  urlDisplay: PropTypes.string.isRequired,
  suffix: PropTypes.string.isRequired,
};

export default KillLink;
