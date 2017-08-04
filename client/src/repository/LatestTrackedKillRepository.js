import axios from 'axios'

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '';

export const getLatestTrackedKills = (restGetter = axios) => {
  return restGetter.get(`${API_BASE_URL}/api/v2/latest`)
  .then((response) => {
    if (!response || !response.data) {
      return null;
    }

    return response.data;
  });
};

