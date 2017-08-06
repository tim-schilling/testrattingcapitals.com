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
import { getLatestTrackedKills } from './LatestTrackedKillRepository';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '';

it('queries the API_BASE_URL\'s latest endpoint', (done) => {
  let urlQueried = undefined;
  const mockGetter = {
    get: (url) => {
      urlQueried = url;
      return Promise.resolve(undefined);
    } 
  }

  getLatestTrackedKills(mockGetter)
  .then(() => {
    expect(urlQueried.indexOf('/api/v2/latest'))
      .toBeGreaterThan(-1);
  })
  .then(() => done(), (ex) => done(ex))
});

it('returns the response data', (done) => {
  const input = {
    data: 'success!'
  };
  const mockGetter = {
    get: () => {
      return Promise.resolve(input);
    } 
  }

  getLatestTrackedKills(mockGetter)
  .then((result) => {
    expect(result).toEqual(input.data);
  })
  .then(() => done(), (ex) => done(ex))
})

it('returns null when there is no response', (done) => {
  const mockGetter = {
    get: () => {
      return Promise.resolve(undefined);
    } 
  }

  getLatestTrackedKills(mockGetter)
  .then((result) => {
    expect(result).toBeNull()
  })
  .then(() => done(), (ex) => done(ex))
})

it('returns null when there is no response data', (done) => {
  const input = {
    notdata: 'hello'
  };

  const mockGetter = {
    get: () => {
      return Promise.resolve(input);
    } 
  }

  getLatestTrackedKills(mockGetter)
  .then((result) => {
    expect(result).toBeNull()
  })
  .then(() => done(), (ex) => done(ex))
})
