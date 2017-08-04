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
