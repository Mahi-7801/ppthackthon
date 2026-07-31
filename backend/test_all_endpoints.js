const http = require('https');

const BASE_URL = 'https://app1f3f-production.up.railway.app';

function request(method, path, headers = {}, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const reqOptions = {
      method,
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname + url.search,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };

    const req = http.request(reqOptions, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        let parsed = data;
        try {
          parsed = JSON.parse(data);
        } catch {}
        resolve({ status: res.statusCode, headers: res.headers, body: parsed });
      });
    });

    req.on('error', (err) => reject(err));
    if (body) {
      req.write(typeof body === 'string' ? body : JSON.stringify(body));
    }
    req.end();
  });
}

async function runTests() {
  console.log('==== Testing All Endpoints on', BASE_URL, '====\n');
  let passed = 0;
  let failed = 0;

  // 1. Health check
  try {
    const res = await request('GET', '/');
    console.log('1. GET / -> Status:', res.status, res.body);
    if (res.status === 200) passed++; else failed++;
  } catch (e) { console.error('1. GET / FAILED:', e.message); failed++; }

  // 2. Signup
  const testEmail = `test_${Date.now()}@example.com`;
  let token = null;
  let userId = null;
  try {
    const res = await request('POST', '/api/signup', {}, {
      email: testEmail,
      password: 'Password123!',
      full_name: 'Test Endpoint User',
    });
    console.log('\n2. POST /api/signup -> Status:', res.status, res.body);
    if (res.status === 200 && res.body.token) {
      token = res.body.token;
      userId = res.body.user?.id;
      passed++;
    } else failed++;
  } catch (e) { console.error('2. Signup FAILED:', e.message); failed++; }

  // 3. Login
  try {
    const res = await request('POST', '/api/login', {}, {
      email: testEmail,
      password: 'Password123!',
    });
    console.log('\n3. POST /api/login -> Status:', res.status, res.body);
    if (res.status === 200 && res.body.token) {
      token = res.body.token;
      userId = res.body.user?.id;
      passed++;
    } else failed++;
  } catch (e) { console.error('3. Login FAILED:', e.message); failed++; }

  const authHeaders = { Authorization: `Bearer ${token}` };
  const mockDocId = 'doc-mock-' + Date.now();
  const docHash = 'SHA256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';

  // 4. Upload document
  try {
    const res = await request('POST', '/api/documents', authHeaders, {
      user_id: userId,
      document_name: 'Test_Contract.pdf',
      document_hash: docHash,
      storage_path: `test/${Date.now()}.pdf`,
    });
    console.log('\n4. POST /api/documents -> Status:', res.status, res.body);
    if (res.status === 200 || res.status === 201) passed++; else failed++;
  } catch (e) { console.error('4. Upload FAILED:', e.message); failed++; }

  // 5. Hash document
  try {
    const res = await request('POST', `/api/documents/${mockDocId}/hash`, authHeaders);
    console.log('\n5. POST /api/documents/:id/hash -> Status:', res.status, res.body);
    if (res.status === 200) passed++; else failed++;
  } catch (e) { console.error('5. Hash FAILED:', e.message); failed++; }

  // 6. List user documents
  try {
    const res = await request('GET', `/api/documents/${userId}`, authHeaders);
    console.log('\n6. GET /api/documents/:userId -> Status:', res.status, res.body);
    if (res.status === 200 && Array.isArray(res.body)) passed++; else failed++;
  } catch (e) { console.error('6. List docs FAILED:', e.message); failed++; }

  // 7. Submit Timestamp (RFC 3161)
  try {
    const res = await request('POST', '/api/submit-timestamp', authHeaders, {
      signature: 'mock_signature_blob_12345',
      documentHash: docHash,
    });
    console.log('\n7. POST /api/submit-timestamp -> Status:', res.status, res.body);
    if (res.status === 200 && res.body.timestamp) passed++; else failed++;
  } catch (e) { console.error('7. Timestamp FAILED:', e.message); failed++; }

  // 8. Record signing session
  try {
    const res = await request('POST', '/api/signing-sessions', authHeaders, {
      user_id: userId,
      document_id: mockDocId,
      certificate_serial_number: '1234567890ABCDEF',
      signed_hash: docHash,
      signature_blob: 'mock_sig_data_blob',
      timestamp_token: new Date().toISOString(),
    });
    console.log('\n8. POST /api/signing-sessions -> Status:', res.status, res.body);
    if (res.status === 200) passed++; else failed++;
  } catch (e) { console.error('8. Record session FAILED:', e.message); failed++; }

  // 9. Assemble PAdES signature
  try {
    const res = await request('POST', '/api/assemble-signature', authHeaders, {
      documentId: mockDocId,
      signature: 'mock_sig_data_blob',
      timestamp: new Date().toISOString(),
      certificateSerial: '1234567890ABCDEF',
    });
    console.log('\n9. POST /api/assemble-signature -> Status:', res.status, res.body);
    if (res.status === 200 && res.body.signedDocumentUrl) passed++; else failed++;
  } catch (e) { console.error('9. Assemble FAILED:', e.message); failed++; }

  // 10. Verify signature
  try {
    const res = await request('POST', '/api/verify-signature', authHeaders, {
      documentId: mockDocId,
      signature: 'mock_sig_data_blob',
    });
    console.log('\n10. POST /api/verify-signature -> Status:', res.status, res.body);
    if (res.status === 200) passed++; else failed++;
  } catch (e) { console.error('10. Verify FAILED:', e.message); failed++; }

  // 11. Log audit
  try {
    const res = await request('POST', '/api/audit-logs', authHeaders, {
      user_id: userId,
      event_type: 'document_signed',
      event_details: { document_id: mockDocId },
    });
    console.log('\n11. POST /api/audit-logs -> Status:', res.status, res.body);
    if (res.status === 200) passed++; else failed++;
  } catch (e) { console.error('11. Log audit FAILED:', e.message); failed++; }

  // 12. List audit logs
  try {
    const res = await request('GET', `/api/audit-logs/${userId}`, authHeaders);
    console.log('\n12. GET /api/audit-logs/:userId -> Status:', res.status, res.body);
    if (res.status === 200) passed++; else failed++;
  } catch (e) { console.error('12. List audit FAILED:', e.message); failed++; }

  // 13. Download signed document PDF
  try {
    const res = await request('GET', `/signed-documents/${mockDocId}-signed.pdf`, authHeaders);
    console.log('\n13. GET /signed-documents/:filename -> Status:', res.status, 'Content-Type:', res.headers['content-type']);
    if (res.status === 200 && res.headers['content-type'] === 'application/pdf') passed++; else failed++;
  } catch (e) { console.error('13. Download PDF FAILED:', e.message); failed++; }

  console.log(`\n========================================`);
  console.log(`RESULTS: ${passed} PASSED, ${failed} FAILED out of ${passed + failed} endpoints.`);
  console.log(`========================================`);
}

runTests();
