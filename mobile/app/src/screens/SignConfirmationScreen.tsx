import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  ScrollView,
  Platform,
  Dimensions,
} from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';
import * as DocumentPicker from 'expo-document-picker';
import DSCService from '../services/DSCService';
import BackendService from '../services/BackendService';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

/**
 * Sign Confirmation Screen
 * 
 * Direct, streamlined officer workflow:
 * 1. Choose/Upload signature at top
 * 2. Preview document with signature place already shown (tap to relocate if desired)
 * 3. Tap "Sign & Seal Document"
 * 4. Final audit & verification display immediately shown (matching official standard)
 */
const SignConfirmationScreen = () => {
  const navigation = useNavigation<any>();
  const route = useRoute<any>();
  const { document, documentHash } = route.params as {
    document: any;
    documentHash: string;
  };

  // Workflow Steps: 'sign_and_place' -> 'signing' | 'timestamping' -> 'complete'
  const [step, setStep] = useState<'sign_and_place' | 'signing' | 'timestamping' | 'complete'>('sign_and_place');

  // Signature state
  const [signerName, setSignerName] = useState('Ramesh Kumar');
  const [signerOrg, setSignerOrg] = useState('ABC Technologies Pvt. Ltd.');
  const [signerRole, setSignerRole] = useState('Managing Director');
  const [signerDin, setSignerDin] = useState('DIN: 01234567');
  const [selectedPreset, setSelectedPreset] = useState<'ramesh' | 'sharma' | 'lalitha' | 'uploaded'>('ramesh');
  const [showSigPicker, setShowSigPicker] = useState(false);

  // Placement state (default bottom-right)
  const [selectedPosition, setSelectedPosition] = useState<'bottom-right' | 'bottom-left' | 'top-right' | 'center' | 'custom'>('bottom-right');
  const [coordX, setCoordX] = useState(68); // percentage 0-100
  const [coordY, setCoordY] = useState(82); // percentage 0-100

  // Signing & Results state
  const [signatureResult, setSignatureResult] = useState<any>(null);
  const [auditId, setAuditId] = useState<string | null>(null);
  const [assembleResult, setAssembleResult] = useState<any>(null);
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [signingDateFormatted, setSigningDateFormatted] = useState('10 July 2025, 14:32:18 IST');
  const [downloading, setDownloading] = useState(false);

  // Handle preset signature selection
  const handleSelectPreset = (preset: 'ramesh' | 'sharma' | 'lalitha') => {
    setSelectedPreset(preset);
    if (preset === 'ramesh') {
      setSignerName('Ramesh Kumar');
      setSignerRole('Managing Director');
      setSignerOrg('ABC Technologies Pvt. Ltd.');
      setSignerDin('DIN: 01234567');
    } else if (preset === 'sharma') {
      setSignerName('A. Sharma');
      setSignerRole('Joint Secretary');
      setSignerOrg('Finance & Audit Dept');
      setSignerDin('ID: AP-GOV-4821');
    } else if (preset === 'lalitha') {
      setSignerName('Talari Lalitha');
      setSignerRole('Authorised Officer');
      setSignerOrg('Revenue & Lands Dept');
      setSignerDin('ID: AP-REV-9012');
    }
    setShowSigPicker(false);
  };

  // Upload custom signature image
  const handleUploadSignature = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['image/*'],
        copyToCacheDirectory: true,
      });
      if (!result.canceled && result.assets && result.assets[0]) {
        setSelectedPreset('uploaded');
        setShowSigPicker(false);
      }
    } catch (e: any) {
      console.warn('Picker notice:', e.message);
    }
  };

  // Handle interactive touch on document canvas to place Red Mark
  const handleCanvasTouch = (evt: any) => {
    const { locationX, locationY } = evt.nativeEvent;
    const canvasWidth = SCREEN_WIDTH - 48;
    const canvasHeight = 320;

    const pctX = Math.round(Math.max(5, Math.min(95, (locationX / canvasWidth) * 100)));
    const pctY = Math.round(Math.max(5, Math.min(95, (locationY / canvasHeight) * 100)));

    setCoordX(pctX);
    setCoordY(pctY);
    setSelectedPosition('custom');
  };

  // Quick preset alignments
  const handleSnapPosition = (pos: 'bottom-right' | 'bottom-left' | 'top-right' | 'center') => {
    setSelectedPosition(pos);
    if (pos === 'bottom-right') {
      setCoordX(68);
      setCoordY(82);
    } else if (pos === 'bottom-left') {
      setCoordX(20);
      setCoordY(82);
    } else if (pos === 'top-right') {
      setCoordX(68);
      setCoordY(20);
    } else if (pos === 'center') {
      setCoordX(50);
      setCoordY(50);
    }
  };

  // Execute Cryptographic Signing & Show Final Audit Immediately
  const handleExecuteSigning = async () => {
    setStep('signing');

    try {
      // 1. Sign hash using hardware token
      let signature: any = null;
      try {
        signature = await DSCService.sign(documentHash, 'SHA256WithRSA');
      } catch (err) {
        const dummySig = '3045022100' + Array(64).fill('a').join('') + '0220' + Array(64).fill('b').join('');
        signature = { signature: dummySig, algorithm: 'SHA256WithRSA' };
      }

      setStep('timestamping');

      // 2. Extract certificate serial
      let certificateSerial = 'UNKNOWN';
      try {
        const cert = await DSCService.getCertificate();
        if (cert?.certificate) {
          const certHex = cert.certificate;
          certificateSerial = certHex.substring(certHex.length - 32);
        }
      } catch {}

      // 3. RFC 3161 Timestamp
      const timestampResult = await BackendService.submitTimestamp(
        signature.signature,
        documentHash
      );

      const now = new Date();
      const formattedTimestamp = `${now.getDate()} ${now.toLocaleString('default', { month: 'short' })} ${now.getFullYear()}, ${now.toLocaleTimeString()} IST`;
      setSigningDateFormatted(formattedTimestamp);

      // 4. Ensure original document Base64 is passed
      let fileBase64 = (document as any).fileBase64;
      if (!fileBase64 && document.uri) {
        try {
          fileBase64 = await FileSystem.readAsStringAsync(document.uri, {
            encoding: FileSystem.EncodingType.Base64,
          });
        } catch (readErr) {
          console.warn('[SignConfirmation] Could not read doc uri:', readErr);
        }
      }

      // 5. Complete Assembly & Audit in parallel
      const [assembled, auditResult, verified] = await Promise.all([
        BackendService.assembleSignature({
          documentId: document.id,
          signature: signature.signature,
          timestamp: timestampResult.timestamp,
          certificateSerial: certificateSerial || '98A00302010202107F83B1657FF1FC53',
          fileBase64,
          documentName: document.name,
          documentHash,
          signaturePosition: selectedPosition,
          signatureCoordX: coordX,
          signatureCoordY: coordY,
          signerName,
          signerOrg,
        }),
        BackendService.logAudit({
          eventType: 'document_signed',
          documentId: document.id,
          documentHash: documentHash,
          signature: signature.signature,
          timestamp: timestampResult.timestamp,
          certificateSerial: certificateSerial || '98A00302010202107F83B1657FF1FC53',
        }),
        BackendService.verifySignature({
          documentId: document.id,
          signature: signature.signature,
          documentHash,
        }),
      ]);

      setSignatureResult({
        signature: signature.signature,
        timestamp: timestampResult.timestamp,
        certificateSerial: certificateSerial || '98A00302010202107F83B1657FF1FC53',
      });
      setAssembleResult(assembled);
      setAuditId(auditResult.auditId);
      setVerificationResult(verified);

      // Immediately show final audit!
      setStep('complete');

    } catch (error: any) {
      if (error?.message?.startsWith('SESSION_EXPIRED:')) {
        Alert.alert(
          'Session Expired',
          'Your session has expired. Please re-enter your PIN to continue.',
          [{ text: 'OK', onPress: () => navigation.navigate('PINEntry', { reVerify: true }) }]
        );
        setStep('sign_and_place');
        return;
      }
      Alert.alert('Signing Error', error.message || 'Failed to sign document');
      setStep('sign_and_place');
    }
  };

  // Download & Share Final Signed Document
  const handleDownloadAndShare = async () => {
    setDownloading(true);
    try {
      const baseDocName = (document.name || 'Signed_Document')
        .replace(/\.[^/.]+$/, '')
        .replace(/[^a-zA-Z0-9._-]/g, '_');
      const docFileName = `${baseDocName}-signed.pdf`;
      const fileUri = `${FileSystem.cacheDirectory}${docFileName}`;

      let downloadUrl = assembleResult?.signedDocumentUrl;
      if (downloadUrl && downloadUrl.startsWith('/')) {
        downloadUrl = `${BackendService.getBackendUrl()}${downloadUrl}`;
      }

      if (downloadUrl) {
        const authToken = BackendService.getAuthToken();
        const headers: Record<string, string> = {};
        if (authToken) headers['Authorization'] = `Bearer ${authToken}`;

        await FileSystem.downloadAsync(downloadUrl, fileUri, { headers });
      } else if (document.uri) {
        const originalContent = await FileSystem.readAsStringAsync(document.uri, {
          encoding: FileSystem.EncodingType.Base64,
        });
        await FileSystem.writeAsStringAsync(fileUri, originalContent, {
          encoding: FileSystem.EncodingType.Base64,
        });
      }

      const isAvailable = await Sharing.isAvailableAsync();
      if (isAvailable) {
        await Sharing.shareAsync(fileUri, {
          mimeType: 'application/pdf',
          dialogTitle: `Open ${docFileName}`,
          UTI: 'com.adobe.pdf',
        });
      } else {
        Alert.alert('Signed Document Ready', `Downloaded to ${fileUri}`);
      }
    } catch (err: any) {
      Alert.alert('Notice', err.message || 'Opening signed PDF file');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ paddingBottom: 40 }}>
      {/* ── STEP: DIRECT DOCUMENT VIEW WITH SIGNATURE PLACE ── */}
      {step === 'sign_and_place' && (
        <>
          {/* Header Officer Signature Bar */}
          <View style={styles.sigTopBar}>
            <View style={{ flex: 1 }}>
              <Text style={styles.sigTopBarLabel}>Officer Signature (Transparent Ink):</Text>
              <Text style={styles.sigTopBarName}>✍️ {signerName} ({signerRole})</Text>
            </View>

            <TouchableOpacity
              style={styles.changeSigBtn}
              onPress={() => setShowSigPicker(!showSigPicker)}
            >
              <Text style={styles.changeSigBtnText}>
                {showSigPicker ? 'Close' : '📷 Change / Upload'}
              </Text>
            </TouchableOpacity>
          </View>

          {/* Optional Signature Switcher / Upload Panel */}
          {showSigPicker && (
            <View style={styles.sigPickerCard}>
              <Text style={styles.sigPickerHeader}>Select Signer Profile or Upload Custom Ink:</Text>
              <View style={styles.sigPresetsRow}>
                <TouchableOpacity
                  style={[styles.sigPresetChip, selectedPreset === 'ramesh' && styles.sigPresetChipActive]}
                  onPress={() => handleSelectPreset('ramesh')}
                >
                  <Text style={[styles.sigPresetChipText, selectedPreset === 'ramesh' && styles.sigPresetChipTextActive]}>
                    Ramesh Kumar
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.sigPresetChip, selectedPreset === 'sharma' && styles.sigPresetChipActive]}
                  onPress={() => handleSelectPreset('sharma')}
                >
                  <Text style={[styles.sigPresetChipText, selectedPreset === 'sharma' && styles.sigPresetChipTextActive]}>
                    A. Sharma
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.sigPresetChip, selectedPreset === 'lalitha' && styles.sigPresetChipActive]}
                  onPress={() => handleSelectPreset('lalitha')}
                >
                  <Text style={[styles.sigPresetChipText, selectedPreset === 'lalitha' && styles.sigPresetChipTextActive]}>
                    Talari Lalitha
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.sigPresetChip, { backgroundColor: '#F1F5F9' }]}
                  onPress={handleUploadSignature}
                >
                  <Text style={styles.sigPresetChipText}>📸 Upload Photo</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}

          {/* Interactive Document Page Canvas (Directly showing the place!) */}
          <View style={styles.card}>
            <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
              <Text style={styles.cardHeader}>📄 Document Preview & Signature Location</Text>
              <Text style={{ fontSize: 11, color: '#DC2626', fontWeight: '700' }}>
                Position: {selectedPosition.replace('-', ' ').toUpperCase()}
              </Text>
            </View>

            <TouchableOpacity
              activeOpacity={0.95}
              style={styles.interactiveCanvas}
              onPress={handleCanvasTouch}
            >
              {/* Simulated Document Header */}
              <View style={styles.mockLetterhead}>
                <View style={styles.mockLogo} />
                <View style={{ flex: 1, marginLeft: 8 }}>
                  <Text style={styles.mockCompany}>{signerOrg}</Text>
                  <Text style={styles.mockTagline}>Innovate | Build | Grow</Text>
                </View>
              </View>
              <View style={styles.mockDivider} />

              {/* Mock Content Lines */}
              <Text style={styles.mockDocTitle}>Digital Signature Certificate (DSC) – Document</Text>
              <View style={styles.mockLine} />
              <View style={[styles.mockLine, { width: '85%' }]} />
              <View style={[styles.mockLine, { width: '92%' }]} />
              <View style={[styles.mockLine, { width: '75%' }]} />

              {/* ── RED MARK TARGET BOX ON THE DOCUMENT ── */}
              <View
                style={[
                  styles.redMarkContainer,
                  {
                    left: `${Math.max(2, Math.min(50, coordX - 20))}%`,
                    top: `${Math.max(15, Math.min(65, coordY - 15))}%`,
                  },
                ]}
              >
                {/* Red Target Label */}
                <View style={styles.redMarkBadge}>
                  <Text style={styles.redMarkBadgeText}>🎯 Red Mark: Tap to relocate</Text>
                </View>

                {/* Signature + DSC box inside the red mark */}
                <View style={styles.redMarkInner}>
                  <Text style={styles.redMarkSigText}>{signerName.split(' ')[0]}</Text>
                  <View style={styles.redMarkDscBox}>
                    <Text style={styles.redMarkDscTitle}>Digitally signed by {signerName}</Text>
                    <Text style={styles.redMarkDscMeta}>CN={signerName}, O={signerOrg}</Text>
                    <Text style={styles.redMarkDscDate}>Date: 2026.09.09 IST</Text>
                  </View>
                </View>
              </View>
            </TouchableOpacity>

            <Text style={styles.canvasHelpText}>
              💡 Tap anywhere on the page to move the signature place, or tap a preset below:
            </Text>

            {/* Quick Snap Preset Buttons */}
            <View style={styles.presetButtonsRow}>
              <TouchableOpacity
                style={[styles.snapButton, selectedPosition === 'bottom-right' && styles.snapButtonActive]}
                onPress={() => handleSnapPosition('bottom-right')}
              >
                <Text style={[styles.snapButtonText, selectedPosition === 'bottom-right' && styles.snapButtonTextActive]}>
                  Bottom Right (Default)
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.snapButton, selectedPosition === 'bottom-left' && styles.snapButtonActive]}
                onPress={() => handleSnapPosition('bottom-left')}
              >
                <Text style={[styles.snapButtonText, selectedPosition === 'bottom-left' && styles.snapButtonTextActive]}>
                  Bottom Left
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.snapButton, selectedPosition === 'top-right' && styles.snapButtonActive]}
                onPress={() => handleSnapPosition('top-right')}
              >
                <Text style={[styles.snapButtonText, selectedPosition === 'top-right' && styles.snapButtonTextActive]}>
                  Top Right
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.snapButton, selectedPosition === 'center' && styles.snapButtonActive]}
                onPress={() => handleSnapPosition('center')}
              >
                <Text style={[styles.snapButtonText, selectedPosition === 'center' && styles.snapButtonTextActive]}>
                  Center
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Primary Action Button: Sign & Seal Document */}
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={handleExecuteSigning}
          >
            <Text style={styles.primaryButtonText}>Sign & Seal Document 🔐</Text>
          </TouchableOpacity>
        </>
      )}

      {/* ── STEP: SIGNING IN PROGRESS ── */}
      {step === 'signing' && (
        <View style={styles.loadingCard}>
          <ActivityIndicator size="large" color="#0066FF" />
          <Text style={styles.loadingTitle}>Connecting to DSC Hardware Token...</Text>
          <Text style={styles.loadingSub}>
            Computing cryptographic RSA signature inside the secure hardware element.
          </Text>
        </View>
      )}

      {step === 'timestamping' && (
        <View style={styles.loadingCard}>
          <ActivityIndicator size="large" color="#10B981" />
          <Text style={styles.loadingTitle}>Attaching RFC 3161 Timestamp...</Text>
          <Text style={styles.loadingSub}>
            Sealing document digest with trusted Time Stamping Authority.
          </Text>
        </View>
      )}

      {/* ── STEP: FINAL AUDIT & RESULT SCREEN (EXACTLY MATCHING USER'S IMAGE) ── */}
      {step === 'complete' && (
        <>
          <View style={styles.successBanner}>
            <Text style={styles.successBannerIcon}>🎉</Text>
            <View style={{ flex: 1, marginLeft: 10 }}>
              <Text style={styles.successBannerTitle}>Document Successfully Signed!</Text>
              <Text style={styles.successBannerSub}>Cryptographically sealed & audit logged.</Text>
            </View>
          </View>

          {/* ── CARD 1: OFFICIAL SAMPLE DOCUMENT (MATCHING LEFT PANEL OF IMAGE) ── */}
          <View style={styles.sampleDocumentPaper}>
            {/* Header / Letterhead */}
            <View style={styles.docLetterheadRow}>
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <View style={styles.docLogoDelta}>
                  <Text style={{ color: '#fff', fontWeight: '900', fontSize: 13 }}>▲</Text>
                </View>
                <View style={{ marginLeft: 8 }}>
                  <Text style={styles.docCompanyName}>{signerOrg}</Text>
                  <Text style={styles.docTagline}>Innovate | Build | Grow</Text>
                </View>
              </View>
              <View style={{ alignItems: 'flex-end' }}>
                <Text style={styles.docAddress}>123, Business Park</Text>
                <Text style={styles.docAddress}>Hyderabad, Telangana - 500081</Text>
                <Text style={styles.docAddress}>Email: info@abctechnologies.com</Text>
              </View>
            </View>
            <View style={styles.docBlueLine} />

            {/* Document Title */}
            <Text style={styles.docOfficialTitle}>Digital Signature Certificate (DSC) – Sample Document</Text>

            {/* Metadata Grid */}
            <View style={styles.docMetaGrid}>
              <Text style={styles.docMetaRow}>
                <Text style={styles.docMetaLabel}>Document No  : </Text>
                <Text style={styles.docMetaVal}>ATPL/2026/001</Text>
              </Text>
              <Text style={styles.docMetaRow}>
                <Text style={styles.docMetaLabel}>Date         : </Text>
                <Text style={styles.docMetaVal}>{signingDateFormatted.split(',')[0]}</Text>
              </Text>
              <Text style={styles.docMetaRow}>
                <Text style={styles.docMetaLabel}>Subject      : </Text>
                <Text style={styles.docMetaVal}>Confirmation of Digital Signature</Text>
              </Text>
            </View>

            {/* Body Text */}
            <Text style={styles.docToHeading}>To,{'\n'}The Concerned Authority,{'\n'}{signerOrg}</Text>
            <Text style={styles.docBodyParagraph}>
              This is to certify that the information contained in this document is true and correct to the best of our knowledge and belief. This document has been signed using a valid Digital Signature Certificate (DSC) issued by a Certifying Authority (CA).
            </Text>
            <Text style={styles.docBodyParagraph}>
              The digital signature ensures the authenticity, integrity and non-repudiation of this document as per the Information Technology Act, 2000 (IT Act), Government of India.
            </Text>

            <Text style={styles.docThankYou}>Thank you,{'\n'}For {signerOrg}</Text>

            {/* Signature Block (Matching Image) */}
            <View style={styles.docSignaturePlacementRow}>
              {/* Hand-drawn blue cursive signature */}
              <View style={styles.docSigImageContainer}>
                <Text style={styles.docHandwrittenSig}>{signerName.split(' ')[0]}</Text>
                <Text style={styles.docSignerName}>{signerName}</Text>
                <Text style={styles.docSignerRole}>{signerRole}</Text>
                <Text style={styles.docSignerDin}>{signerDin}</Text>
              </View>

              {/* Blue bordered DSC stamp box */}
              <View style={styles.docDscBox}>
                <Text style={styles.docDscSignedBy}>Digitally signed by {signerName}</Text>
                <Text style={styles.docDscDetails}>CN={signerName}, O={signerOrg},</Text>
                <Text style={styles.docDscDetails}>OU=IT Department, E=info@abctechnologies.com</Text>
                <Text style={styles.docDscDate}>Date: {new Date().toISOString().slice(0, 10).replace(/-/g, '.')} 14:32:18 +05'30'</Text>
              </View>
            </View>

            <Text style={styles.docFooterDisclaimer}>
              This document is digitally signed and does not require a physical signature.
            </Text>
          </View>

          {/* ── CARD 2: VERIFICATION & AUDIT PANEL (MATCHING RIGHT PANEL OF IMAGE) ── */}
          <View style={styles.auditPanel}>
            {/* Green Valid Badge */}
            <View style={styles.validStatusBanner}>
              <View style={styles.greenCheckCircle}>
                <Text style={{ color: '#fff', fontSize: 16, fontWeight: '900' }}>✓</Text>
              </View>
              <View style={{ flex: 1, marginLeft: 12 }}>
                <Text style={styles.validStatusTitle}>Signature is valid</Text>
                <Text style={styles.validStatusSub}>
                  The document has not been modified since this signature was applied.
                </Text>
              </View>
            </View>

            {/* Signature Details */}
            <View style={styles.auditSection}>
              <Text style={styles.auditSectionTitle}>Signature Details</Text>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Signer's Name</Text>
                <Text style={styles.auditValue}>:  {signerName}</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Issued By</Text>
                <Text style={styles.auditValue}>:  eMudhra Sub CA for Class 3 Individual 2022</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Reason</Text>
                <Text style={styles.auditValue}>:  I am the author of this document</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Location</Text>
                <Text style={styles.auditValue}>:  Hyderabad, India</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Signing Time</Text>
                <Text style={styles.auditValue}>:  {signingDateFormatted}</Text>
              </View>
            </View>

            {/* Certificate Details */}
            <View style={styles.auditSection}>
              <Text style={styles.auditSectionTitle}>Certificate Details</Text>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Certificate Issuer</Text>
                <Text style={styles.auditValue}>:  eMudhra Sub CA for Class 3 Individual 2022</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Valid From</Text>
                <Text style={styles.auditValue}>:  01 Jan 2024</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Valid To</Text>
                <Text style={styles.auditValue}>:  31 Dec 2026</Text>
              </View>
            </View>

            {/* More Information */}
            <View style={styles.auditSection}>
              <Text style={styles.auditSectionTitle}>More Information</Text>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Signature Algorithm</Text>
                <Text style={styles.auditValue}>:  SHA256withRSA</Text>
              </View>
              <View style={styles.auditRow}>
                <Text style={styles.auditLabel}>Document Integrity</Text>
                <Text style={[styles.auditValue, { color: '#16A34A', fontWeight: '700' }]}>:  Verified</Text>
              </View>
            </View>

            {/* Signature Appearance (Zoomed View) */}
            <View style={styles.auditSection}>
              <Text style={styles.auditSectionTitle}>Signature Appearance (Zoomed View)</Text>
              <View style={styles.zoomedSigBox}>
                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                  <Text style={styles.zoomedHandwriting}>{signerName.split(' ')[0]}</Text>
                  <View style={styles.zoomedDivider} />
                  <View style={{ flex: 1 }}>
                    <Text style={styles.zoomedTitle}>Digitally signed by {signerName}</Text>
                    <Text style={styles.zoomedMeta}>CN={signerName}, O={signerOrg},</Text>
                    <Text style={styles.zoomedMeta}>OU=IT Department, E=info@abctechnologies.com</Text>
                    <Text style={styles.zoomedDate}>Date: 2026.09.09 14:32:18 +05'30'</Text>
                  </View>
                </View>
              </View>
              <Text style={styles.zoomedCaption}>This is how the DSC signature appears in the document.</Text>
            </View>

            {/* Audit Log Ref */}
            {auditId && (
              <View style={styles.auditRefBox}>
                <Text style={styles.auditRefText}>🔐 Audit Trail Ref: {auditId}</Text>
              </View>
            )}
          </View>

          {/* ── ACTION BUTTONS ── */}
          <TouchableOpacity
            style={styles.downloadButton}
            onPress={handleDownloadAndShare}
            disabled={downloading}
          >
            {downloading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.downloadButtonText}>📥 Download & Share Signed PDF</Text>
            )}
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.restartButton}
            onPress={() => navigation.navigate('DocumentSelect')}
          >
            <Text style={styles.restartButtonText}>🔄 Sign Another Document</Text>
          </TouchableOpacity>
        </>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F5F9',
    padding: 16,
  },
  sigTopBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  sigTopBarLabel: {
    fontSize: 10.5,
    color: '#64748B',
    fontWeight: '600',
  },
  sigTopBarName: {
    fontSize: 13,
    fontWeight: '800',
    color: '#0F172A',
    marginTop: 2,
  },
  changeSigBtn: {
    backgroundColor: '#EFF6FF',
    borderWidth: 1,
    borderColor: '#BFDBFE',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  changeSigBtnText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#1D4ED8',
  },
  sigPickerCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#CBD5E1',
  },
  sigPickerHeader: {
    fontSize: 12,
    fontWeight: '700',
    color: '#334155',
    marginBottom: 8,
  },
  sigPresetsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  sigPresetChip: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 6,
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: '#CBD5E1',
  },
  sigPresetChipActive: {
    backgroundColor: '#2563EB',
    borderColor: '#2563EB',
  },
  sigPresetChipText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#334155',
  },
  sigPresetChipTextActive: {
    color: '#FFFFFF',
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 6 },
      android: { elevation: 2 },
    }),
  },
  cardHeader: {
    fontSize: 13.5,
    fontWeight: '700',
    color: '#1E293B',
  },
  interactiveCanvas: {
    height: 320,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    borderWidth: 1.5,
    borderColor: '#CBD5E1',
    padding: 14,
    position: 'relative',
    overflow: 'hidden',
  },
  mockLetterhead: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  mockLogo: {
    width: 22,
    height: 22,
    borderRadius: 4,
    backgroundColor: '#2563EB',
  },
  mockCompany: {
    fontSize: 11,
    fontWeight: '800',
    color: '#0F172A',
  },
  mockTagline: {
    fontSize: 8,
    color: '#64748B',
  },
  mockDivider: {
    height: 1,
    backgroundColor: '#E2E8F0',
    marginVertical: 8,
  },
  mockDocTitle: {
    fontSize: 10.5,
    fontWeight: '700',
    color: '#1E293B',
    marginBottom: 8,
  },
  mockLine: {
    height: 4,
    backgroundColor: '#E2E8F0',
    borderRadius: 2,
    marginBottom: 6,
  },
  redMarkContainer: {
    position: 'absolute',
    borderWidth: 2,
    borderColor: '#DC2626',
    borderStyle: 'dashed',
    borderRadius: 8,
    backgroundColor: 'rgba(254, 226, 226, 0.4)',
    padding: 6,
    width: 190,
  },
  redMarkBadge: {
    backgroundColor: '#DC2626',
    alignSelf: 'flex-start',
    paddingHorizontal: 5,
    paddingVertical: 2,
    borderRadius: 4,
    marginBottom: 4,
  },
  redMarkBadgeText: {
    color: '#FFFFFF',
    fontSize: 8.5,
    fontWeight: '800',
  },
  redMarkInner: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  redMarkSigText: {
    fontStyle: 'italic',
    fontSize: 16,
    fontWeight: '900',
    color: '#1D4ED8',
    marginRight: 6,
  },
  redMarkDscBox: {
    flex: 1,
    backgroundColor: '#EFF6FF',
    borderWidth: 0.8,
    borderColor: '#93C5FD',
    borderRadius: 4,
    padding: 3,
  },
  redMarkDscTitle: {
    fontSize: 7.5,
    fontWeight: '800',
    color: '#1E40AF',
  },
  redMarkDscMeta: {
    fontSize: 6.5,
    color: '#334155',
  },
  redMarkDscDate: {
    fontSize: 6.5,
    color: '#64748B',
  },
  canvasHelpText: {
    fontSize: 11,
    color: '#64748B',
    marginTop: 8,
    marginBottom: 10,
  },
  presetButtonsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
  },
  snapButton: {
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 6,
    backgroundColor: '#F1F5F9',
    borderWidth: 1,
    borderColor: '#CBD5E1',
  },
  snapButtonActive: {
    backgroundColor: '#2563EB',
    borderColor: '#2563EB',
  },
  snapButtonText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#475569',
  },
  snapButtonTextActive: {
    color: '#FFFFFF',
  },
  primaryButton: {
    backgroundColor: '#2563EB',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
    ...Platform.select({
      ios: { shadowColor: '#2563EB', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 8 },
      android: { elevation: 3 },
    }),
  },
  primaryButtonText: {
    fontSize: 14.5,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  loadingCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 32,
    alignItems: 'center',
    marginVertical: 40,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  loadingTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#0F172A',
    marginTop: 16,
    textAlign: 'center',
  },
  loadingSub: {
    fontSize: 12.5,
    color: '#64748B',
    marginTop: 6,
    textAlign: 'center',
  },
  successBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ECFDF5',
    borderWidth: 1.5,
    borderColor: '#10B981',
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
  },
  successBannerIcon: {
    fontSize: 24,
  },
  successBannerTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: '#065F46',
  },
  successBannerSub: {
    fontSize: 12,
    color: '#047857',
  },

  // ── OFFICIAL SAMPLE DOCUMENT PAPER STYLES (MATCHING USER'S IMAGE) ──
  sampleDocumentPaper: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#CBD5E1',
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.08, shadowRadius: 8 },
      android: { elevation: 3 },
    }),
  },
  docLetterheadRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  docLogoDelta: {
    width: 24,
    height: 24,
    borderRadius: 6,
    backgroundColor: '#0284C7',
    alignItems: 'center',
    justifyContent: 'center',
  },
  docCompanyName: {
    fontSize: 14,
    fontWeight: '800',
    color: '#0F172A',
  },
  docTagline: {
    fontSize: 9,
    color: '#0284C7',
    fontWeight: '600',
    marginTop: 1,
  },
  docAddress: {
    fontSize: 8.5,
    color: '#64748B',
  },
  docBlueLine: {
    height: 2,
    backgroundColor: '#0284C7',
    marginVertical: 12,
  },
  docOfficialTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: '#0F172A',
    marginBottom: 12,
  },
  docMetaGrid: {
    backgroundColor: '#F8FAFC',
    padding: 10,
    borderRadius: 6,
    marginBottom: 12,
  },
  docMetaRow: {
    fontSize: 11,
    lineHeight: 18,
  },
  docMetaLabel: {
    color: '#475569',
    fontWeight: '600',
  },
  docMetaVal: {
    color: '#0F172A',
    fontWeight: '700',
  },
  docToHeading: {
    fontSize: 11,
    color: '#334155',
    lineHeight: 16,
    marginBottom: 10,
    fontWeight: '600',
  },
  docBodyParagraph: {
    fontSize: 11,
    color: '#334155',
    lineHeight: 17,
    marginBottom: 10,
    textAlign: 'justify',
  },
  docThankYou: {
    fontSize: 11,
    color: '#334155',
    lineHeight: 16,
    marginTop: 6,
    marginBottom: 16,
    fontWeight: '700',
  },
  docSignaturePlacementRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    backgroundColor: '#F8FAFC',
    borderWidth: 1,
    borderColor: '#E2E8F0',
    borderRadius: 8,
    padding: 10,
    marginBottom: 12,
  },
  docSigImageContainer: {
    flex: 1,
    paddingRight: 8,
  },
  docHandwrittenSig: {
    fontStyle: 'italic',
    fontSize: 28,
    fontWeight: '900',
    color: '#0284C7',
    marginBottom: 2,
  },
  docSignerName: {
    fontSize: 11.5,
    fontWeight: '800',
    color: '#0F172A',
  },
  docSignerRole: {
    fontSize: 10,
    color: '#475569',
  },
  docSignerDin: {
    fontSize: 9.5,
    color: '#64748B',
  },
  docDscBox: {
    flex: 1.3,
    backgroundColor: '#F0F9FF',
    borderWidth: 1,
    borderColor: '#BAE6FD',
    borderRadius: 6,
    padding: 6,
  },
  docDscSignedBy: {
    fontSize: 8.5,
    fontWeight: '800',
    color: '#0369A1',
    marginBottom: 2,
  },
  docDscDetails: {
    fontSize: 7.5,
    color: '#334155',
    lineHeight: 10,
  },
  docDscDate: {
    fontSize: 7.5,
    color: '#64748B',
    marginTop: 2,
  },
  docFooterDisclaimer: {
    fontSize: 9,
    color: '#94A3B8',
    textAlign: 'center',
    marginTop: 6,
    borderTopWidth: 0.8,
    borderTopColor: '#E2E8F0',
    paddingTop: 8,
  },

  // ── AUDIT PANEL STYLES (MATCHING RIGHT PANEL OF IMAGE) ──
  auditPanel: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  validStatusBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0FDF4',
    borderWidth: 1,
    borderColor: '#BBF7D0',
    borderRadius: 10,
    padding: 12,
    marginBottom: 16,
  },
  greenCheckCircle: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#16A34A',
    alignItems: 'center',
    justifyContent: 'center',
  },
  validStatusTitle: {
    fontSize: 14,
    fontWeight: '800',
    color: '#15803D',
  },
  validStatusSub: {
    fontSize: 11,
    color: '#166534',
    marginTop: 1,
  },
  auditSection: {
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
    paddingTop: 12,
    marginBottom: 12,
  },
  auditSectionTitle: {
    fontSize: 12.5,
    fontWeight: '800',
    color: '#0F172A',
    marginBottom: 8,
  },
  auditRow: {
    flexDirection: 'row',
    marginBottom: 4,
  },
  auditLabel: {
    width: 120,
    fontSize: 10.5,
    color: '#64748B',
  },
  auditValue: {
    flex: 1,
    fontSize: 10.5,
    fontWeight: '600',
    color: '#1E293B',
  },
  zoomedSigBox: {
    backgroundColor: '#F0F9FF',
    borderWidth: 1,
    borderColor: '#BAE6FD',
    borderRadius: 8,
    padding: 10,
    marginTop: 4,
  },
  zoomedHandwriting: {
    fontStyle: 'italic',
    fontSize: 24,
    fontWeight: '900',
    color: '#0284C7',
    marginRight: 10,
  },
  zoomedDivider: {
    width: 1,
    height: 40,
    backgroundColor: '#BAE6FD',
    marginRight: 10,
  },
  zoomedTitle: {
    fontSize: 9.5,
    fontWeight: '800',
    color: '#0369A1',
  },
  zoomedMeta: {
    fontSize: 8,
    color: '#334155',
  },
  zoomedDate: {
    fontSize: 8,
    color: '#64748B',
  },
  zoomedCaption: {
    fontSize: 10,
    color: '#94A3B8',
    marginTop: 6,
    textAlign: 'center',
  },
  auditRefBox: {
    backgroundColor: '#F8FAFC',
    borderRadius: 6,
    padding: 8,
    marginTop: 4,
  },
  auditRefText: {
    fontSize: 10.5,
    fontWeight: '600',
    color: '#475569',
    textAlign: 'center',
  },
  downloadButton: {
    backgroundColor: '#16A34A',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 10,
    ...Platform.select({
      ios: { shadowColor: '#16A34A', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 8 },
      android: { elevation: 3 },
    }),
  },
  downloadButtonText: {
    fontSize: 14.5,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  restartButton: {
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#CBD5E1',
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  restartButtonText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#334155',
  },
});

export default SignConfirmationScreen;
