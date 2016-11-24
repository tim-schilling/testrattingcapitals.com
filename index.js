var rest = require('restler');
var moment = require('moment');

var ZKILL_BASE_URL = 'https://zkillboard.com';
var ZKILL_RESOURCE = '/api/losses/alliance/498125261/group/547,513,902,30,659,883/no-items/no-attackers/limit/1';

function resultObject(daysSince = 0, url) {
  this.daysSince = daysSince;
  this.url = url;
};

function parseZKill(zKill) {
  var result;

  if (!zKill || !zKill.killTime || !zKill.killID) {
    result = new resultObject(-1);
    return result;
  }

  var now = moment(new Date().getTime());
  var killDate = moment(zKill.killTime);
  var daysSince = now.diff(killDate, 'days');

  var url = ZKILL_BASE_URL + '/kill/' + zKill.killID;

  return new resultObject(daysSince, url);
};

rest.get(ZKILL_BASE_URL + ZKILL_RESOURCE).on('complete', function (result) {
  if (result instanceof Error) return;
  if (Array.isArray(result) === false) return;
  if (result.length === 0 || !result[0]) return;

  console.log(
    JSON.stringify(
      parseZKill(result[0])
    )
  );
});
