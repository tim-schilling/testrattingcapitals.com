import moment from 'moment';
import zkillRepository from './repositories/zkillRepository';

Promise.all([
  zkillRepository.getLatestCapital(),
  zkillRepository.getLatestVni(),
])
/* eslint-disable no-console */
.then((values) => {
  console.log(JSON.stringify({
    capital: values[0],
    vni: values[1],
    lastUpdated: moment().toISOString(),
  }));
},
(err => console.error(`ERROR: ${err}`)),
);
  /* eslint-enable no-console */
