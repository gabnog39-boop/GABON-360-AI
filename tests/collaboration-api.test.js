const assert = require('node:assert/strict');
const handler = require('../api/collaboration.js');

function response() {
  return {
    code: 200,
    payload: null,
    status(code) { this.code = code; return this; },
    json(payload) { this.payload = payload; return this; }
  };
}

async function run() {
  global.fetch = async (url) => {
    if (String(url).includes('/auth/v1/user')) {
      return { ok: true, json: async () => ({ id: 'test-user' }) };
    }
    if (String(url).includes('/rest/v1/profiles')) {
      return { ok: true, json: async () => ([{ statut: 'actif' }]) };
    }
    throw new Error('Unexpected fetch URL: ' + url);
  };

  const ok = response();
  await handler({
    method: 'POST',
    headers: { authorization: 'Bearer test-session' },
    body: {
      agent: 'satellites',
      question: 'Vérifier les observations Sentinel dans les parcs',
      evidence: [{
        source: 'copernicus_sentinel_2_l2a',
        kind: 'satellite_catalog_observation',
        catalog_record: { product_id: 'fixture-only' },
        live: false
      }]
    }
  }, ok);

  assert.equal(ok.code, 200);
  assert.equal(ok.payload.ok, true);
  assert.equal(ok.payload.execution, 'deterministic_evidence_triage');
  assert.equal(ok.payload.agents.length <= 7, true);
  assert.equal(ok.payload.agents[0].id, 'satellites');
  assert.equal(ok.payload.agents[0].evidence_count, 1);
  assert.equal(ok.payload.agents[0].autonomous_model_connected, false);
  assert.equal(ok.payload.agents[0].requires_human_validation, true);

  // Exercise all 22 registered roles with one matching evidence field each.
  const fixtures = {
    accueil:'situation', carte:'geometry', satellites:'sentinel', drones:'drone',
    navigation:'route', geoloc:'coordinates', cyber:'security', memoire:'history',
    alertes:'severity', rapports:'report', stats:'count', meteo:'weather',
    parcs:'forest', eaux:'water', frontieres:'border', air:'airspace',
    centre:'source', admin:'role', users:'user', paiements:'payment',
    missions:'mission', garmin:'gpx'
  };
  for (const [agent, evidenceKey] of Object.entries(fixtures)) {
    const result = response();
    await handler({
      method: 'POST',
      headers: { authorization: 'Bearer test-session' },
      body: { agent, question: 'test', evidence: [{ [evidenceKey]: 'fixture' }] }
    }, result);
    assert.equal(result.code, 200, agent);
    assert.equal(result.payload.agents[0].id, agent, agent);
    assert.equal(result.payload.agents[0].evidence_count, 1, agent);
    assert.equal(result.payload.agents[0].requires_human_validation, true, agent);
  }

  const inactiveProfile = response();
  global.fetch = async (url) => {
    if (String(url).includes('/auth/v1/user')) return { ok: true, json: async () => ({ id: 'inactive-user' }) };
    if (String(url).includes('/rest/v1/profiles')) return { ok: true, json: async () => ([{ statut: 'suspendu' }]) };
    throw new Error('Unexpected fetch URL: ' + url);
  };
  await handler({ method: 'POST', headers: { authorization: 'Bearer test-session' }, body: {} }, inactiveProfile);
  assert.equal(inactiveProfile.code, 403);

  global.fetch = async (url) => {
    if (String(url).includes('/auth/v1/user')) return { ok: true, json: async () => ({ id: 'test-user' }) };
    if (String(url).includes('/rest/v1/profiles')) return { ok: true, json: async () => ([{ statut: 'actif' }]) };
    throw new Error('Unexpected fetch URL: ' + url);
  };
  const unknown = response();
  await handler({ method: 'POST', headers: { authorization: 'Bearer test-session' }, body: { agent: 'inconnu' } }, unknown);
  assert.equal(unknown.code, 400);

  const tooLarge = response();
  await handler({ method: 'POST', headers: { authorization: 'Bearer test-session' }, body: { agent: 'accueil', payload: 'x'.repeat(100001) } }, tooLarge);
  assert.equal(tooLarge.code, 413);

  const denied = response();
  await handler({ method: 'POST', headers: {}, body: {} }, denied);
  assert.equal(denied.code, 401);

  const wrongMethod = response();
  await handler({ method: 'GET', headers: {}, body: {} }, wrongMethod);
  assert.equal(wrongMethod.code, 405);

  console.log('OK — API collaboration: 22 rôles, preuves, authentification, suspension et limites');
}

run().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
