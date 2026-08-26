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
  const otp = Math.floor(100000 + Math.random() * 900000).toString();

  console.log(`[SMTP] Sending test 2FA Access OTP (${otp}) to ${targetEmail}...`);

  const html = `
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><style>
      body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #0B132B; color: #FFFFFF; margin: 0; padding: 20px; }
      .card { max-width: 500px; margin: 0 auto; background-color: #111C3D; border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 28px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; }
      .badge { display: inline-block; background-color: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 11px; font-weight: bold; padding: 4px 12px; border-radius: 6px; border: 1px solid #38BDF8; margin-bottom: 12px; }
      .title { font-size: 20px; font-weight: 800; color: #FFFFFF; margin-bottom: 8px; }
      .text { font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 20px; }
      .otp-box { background-color: #172554; border: 2px dashed #38BDF8; border-radius: 12px; padding: 18px; font-size: 32px; font-weight: 900; color: #38BDF8; letter-spacing: 8px; margin: 16px 0; }
      .footer { font-size: 11px; color: #64748B; margin-top: 20px; }
    </style></head>
    <body>
      <div class="card">
        <div class="badge">🔐 TWO-FACTOR OUT-OF-BAND AUTHENTICATION</div>
        <div class="title">SecureSign Document Access Code</div>
        <p class="text">You requested to access the digitally signed document <strong>AP_Govt_Order_MS_104.pdf</strong>. Enter this 6-digit verification code:</p>
        <div class="otp-box">${otp}</div>
        <p class="text" style="font-size: 11px; color: #94A3B8;">This code is valid for <strong>5 minutes</strong>. Signed under CCA India & IT Act 2000 Section 3A guidelines.</p>
        <div class="footer">SecureSign Innovation Challenge 2026 • Government of Andhra Pradesh & APIS</div>
      </div>
    </body>
    </html>
  `;

  try {
    const info = await mailTransporter.sendMail({
      from: '"SecureSign AP Government" <pmahi7801@gmail.com>',
      to: targetEmail,
      subject: `🔑 [${otp}] Your SecureSign Document Access Code`,
      html,
    });
    console.log(`✔ SUCCESS: OTP Email delivered to ${targetEmail}! Message ID: ${info.messageId}`);
    console.log(`✔ Sent OTP: ${otp}`);
  } catch (err) {
    console.error('❌ SMTP Error:', err);
  }
}

run();
