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

