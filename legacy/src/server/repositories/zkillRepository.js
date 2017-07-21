// @flow

import Rest from 'restler';

const ZKILL_BASE_URL = 'https://zkillboard.com';
const ZKILL_CAPITAL_RESOURCE = '/api/losses/alliance/498125261/group/30,513,547,659,883,902/no-items/no-attackers/limit/1/';
const ZKILL_VNI_RESOURCE = '/api/losses/alliance/498125261/ship/17843/no-items/no-attackers/limit/1/';

const zkillGet = (resource: string) =>
  new Promise((resolve, reject) => {
    Rest.get(`${ZKILL_BASE_URL}${resource}`)
    .on('complete', (result) => {
      if (!result) {
        return reject(new Error('No response'));
      }

      if (result instanceof Error) {
        return reject(result);
      }

      if (Array.isArray(result) === false) {
        return reject(new Error('Response not an array'));
      }

      if (result.length === 0 || !result[0]) {
        return reject(new Error('No data in response'));
      }

      return resolve(result[0]);
    });
  },
);

class ZKillRepository {
  static getLatestCapital(): object {
    return zkillGet(ZKILL_CAPITAL_RESOURCE);
  }

  static getLatestVni(): object {
    return zkillGet(ZKILL_VNI_RESOURCE);
  }
}

export default ZKillRepository;
