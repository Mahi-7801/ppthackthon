const http = require('https');

const BASE_URL = 'https://app1f3f-production.up.railway.app';

// Minimal valid 1-page PDF binary in Base64
const SAMPLE_PDF_BASE64 = `JVBERi0xLjQKMSAwIG9iagocL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDIgMCBSCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovS2lkcyBbMyAwIFJdCi9Db3VudCAxCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgMiAwIFIKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KL1Jlc291cmNlcyA8PAogIC9Gb250IDw8CiAgICAvRjEgNCAwIFIKICA+Pgo+PgovQ29udGVudHMgNSAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhCj4+CmVuZG9iago1IDAgb2JqCjw8IC9MZW5ndGg1NiA+PgpzdHJlYW0KQlQKL0YxIDI0IFRmCjEwMCA3MDAgVGQKKEhlbGxvLCBTZWN1cmVTaWduISkgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgNgowMDAwMDAwMDAwDYTY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAwMTE1IDAwMDAwIG4gCjAwMDAwMDAyNjYgMDAwMDAgbiAKMDAwMDAwMDM0MCAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDYKL1Jvb3QgMSAwIFIKPj4Kc3RhcnR4cmVmCjQ0NgolJUVPRg==`;

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
        try { parsed = JSON.parse(data); } catch {}
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

async function verifyPdfUpload() {
  console.log('==== Verifying PDF Upload on', BASE_URL, '====\n');

  // Step 1: Login to get token
  const loginRes = await request('POST', '/api/login', {}, {
    email: 'pdf_test_user@example.com',
    password: 'Password123!',
  });
  console.log('1. Login Status:', loginRes.status);
  const token = loginRes.body.token;
  const userId = loginRes.body.user.id;

  // Step 2: Upload PDF document with Base64 data
  const documentName = `Agreement_${Date.now()}.pdf`;
  const documentHash = 'SHA256:a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3';

  const uploadRes = await request('POST', '/api/documents', {
    Authorization: `Bearer ${token}`
  }, {
    user_id: userId,
    document_name: documentName,
    document_hash: documentHash,
    storage_path: `${userId}/${Date.now()}_${documentName}`,
    file_data: SAMPLE_PDF_BASE64,
  });

  console.log('2. PDF Upload Status:', uploadRes.status);
  console.log('   Response Body:', JSON.stringify(uploadRes.body, null, 2));

  if (uploadRes.status === 200 && uploadRes.body.id) {
    console.log('\n✅ PDF UPLOAD VERIFIED SUCCESSFUL!');
    console.log('   Document ID:', uploadRes.body.id);
    console.log('   Document Name:', uploadRes.body.document_name);
    console.log('   Document Hash:', uploadRes.body.document_hash);
    console.log('   Storage Path:', uploadRes.body.storage_path);
  } else {
    console.log('\n❌ PDF UPLOAD FAILED');
  }
}

verifyPdfUpload().catch(console.error);
