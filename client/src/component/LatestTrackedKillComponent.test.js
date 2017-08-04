import Unit from './LatestTrackedKillComponent';

it('has no state with no props', () => {
  const result = new Unit(undefined);
  expect(result.state).toMatchObject({});
})

it('has no state with missing props', () => {
  let result = new Unit({ trackingLabelDescription: '', kill: {} });
  expect(result.state).toMatchObject({});

  result = new Unit({ trackingLabel: '', kill: {} });
  expect(result.state).toMatchObject({});

  result = new Unit({ trackingLabel: '', trackingLabelDescription: '' });
  expect(result.state).toMatchObject({});
});
