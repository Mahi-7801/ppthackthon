const nodemailer = require('nodemailer');

const mailTransporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'pmahi7801@gmail.com',
    pass: 'temwiqpfsrxxehob',
  },
});

async function run() {
  const targetEmail = 'mahankalikornepati@gmail.com';

  console.log(`[SMTP] Sending Welcome & Signed Document Notifications to ${targetEmail}...`);

  // 1. Welcome Email
  const welcomeHtml = `
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><style>
      body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #0B132B; color: #FFFFFF; margin: 0; padding: 20px; }
      .card { max-width: 540px; margin: 0 auto; background-color: #111C3D; border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 28px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
      .header { text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 18px; margin-bottom: 20px; }
      .badge { display: inline-block; background-color: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 11px; font-weight: bold; padding: 4px 12px; border-radius: 6px; border: 1px solid #38BDF8; }
      .title { font-size: 22px; font-weight: 800; color: #FFFFFF; margin-top: 10px; letter-spacing: 1px; }
      .text { font-size: 14px; color: #CBD5E1; line-height: 1.6; }
      .detail-box { background-color: #172554; border-radius: 10px; padding: 14px 18px; margin: 18px 0; border-left: 4px solid #10B981; }
      .detail-line { font-size: 13px; color: #E2E8F0; margin: 5px 0; }
      .footer { text-align: center; font-size: 11px; color: #64748B; margin-top: 24px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; }
    </style></head>
    <body>
      <div class="card">
        <div class="header">
          <div class="badge">🏛️ GOVT OF AP • RTIH • NIC CHALLENGE 2026</div>
          <div class="title">🛡️ Welcome to SecureSign</div>
          <p style="color:#94A3B8; font-size:12px; margin:4px 0 0 0;">Enterprise Type-C DSC Mobile Signing Solution</p>
        </div>
        <p class="text">Hello <strong>Mahankali Kornepati</strong>,</p>
        <p class="text">Thank you for registering on <strong>SecureSign</strong>. Your account is active and ready for hardware cryptographic operations compliant with CCA India rules.</p>
        <div class="detail-box">
          <div class="detail-line"><strong>Registered Email:</strong> ${targetEmail}</div>
          <div class="detail-line"><strong>Status:</strong> <span style="color:#10B981; font-weight:bold;">✔ 100% Verified & Active</span></div>
          <div class="detail-line"><strong>Hardware Security:</strong> ISO 7816-4 CCID Pure Hardware Mode</div>
          <div class="detail-line"><strong>Compliance:</strong> Class-3 DSC • RFC 3161 TSA • PAdES-LTV</div>
        </div>
        <p class="text">You can now plug your Type-C DSC token into your mobile device and perform tamper-evident digital signatures.</p>
        <div class="footer">
          SecureSign Innovation Challenge 2026 • Government of Andhra Pradesh & APIS
        </div>
      </div>
    </body>
    </html>
  `;

  await mailTransporter.sendMail({
    from: '"SecureSign AP Government" <pmahi7801@gmail.com>',
    to: targetEmail,
    subject: '🛡️ Welcome to SecureSign — Account Active & Ready for Hardware Signing',
    html: welcomeHtml,
  });

  console.log(`✔ SUCCESS: Welcome Email delivered to ${targetEmail}!`);
}

run();
