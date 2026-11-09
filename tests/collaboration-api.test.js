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

  const denied = response();
  await handler({ method: 'POST', headers: {}, body: {} }, denied);
  assert.equal(denied.code, 401);

  const wrongMethod = response();
  await handler({ method: 'GET', headers: {}, body: {} }, wrongMethod);
  assert.equal(wrongMethod.code, 405);

  console.log('OK — API collaboration: routage, preuves, authentification et limites');
}

run().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
