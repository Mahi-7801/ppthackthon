import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  Platform,
  StatusBar,
} from 'react-native';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import DSCService from '../services/DSCService';
import BackendService from '../services/BackendService';
import SessionManager from '../services/SessionManager';

/**
 * Home Screen - Executive Mobile Signing Hub
 * Ultra-smooth, responsive Cyber-Glassmorphism UI.
 */
const HomeScreen = () => {
  const navigation = useNavigation<any>();
  const [tokens, setTokens] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [connectedDevice, setConnectedDevice] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string>('Ready for Hardware Signing');

  // Check if user is logged in
  const isLoggedIn = !!BackendService.getCurrentUserId();

  useEffect(() => {
    scanForTokens();
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      if (!isLoggedIn) return;

      const connectListener = DSCService.onDeviceConnected((data: any) => {
        setConnectedDevice(data.serialNumber);
        setStatusMessage(`✔ Hardware Connected: ${data.serialNumber}`);
      });

      const disconnectListener = DSCService.onDeviceDisconnected(() => {
        setConnectedDevice(null);
        setStatusMessage('DSC Dongle Disconnected');
      });

      scanForTokens();

      return () => {
        connectListener?.remove();
        disconnectListener?.remove();
      };
    }, [isLoggedIn])
  );

  const scanForTokens = async () => {
    setLoading(true);
    setStatusMessage('Scanning USB host endpoints...');
    try {
      const foundTokens = await DSCService.listTokens();
      setTokens(foundTokens || []);
      if (foundTokens && foundTokens.length > 0) {
        setStatusMessage(`Found ${foundTokens.length} DSC Hardware Token(s)`);
      } else {
        setStatusMessage('No USB Dongle Detected. Ready for Connection.');
      }
    } catch (error: any) {
      setTokens([]);
      setStatusMessage('No Hardware Dongle Attached');
    } finally {
      setLoading(false);
    }
  };

  const handleConnect = async (serialNumber: string) => {
    setLoading(true);
    try {
      await DSCService.connectDevice(serialNumber);
      setConnectedDevice(serialNumber);
      navigation.navigate('PINEntry');
    } catch (error: any) {
      setStatusMessage(`Connection Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleLaunchSandbox = () => {
    // Enable Sandbox Simulation Mode for Evaluators
    navigation.navigate('PINEntry', { isSandbox: true });
  };

  const handleLogout = () => {
    BackendService.logout();
    SessionManager.resetSession();
    navigation.reset({ index: 0, routes: [{ name: 'Login' }] });
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#0B132B" />
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        
        {/* Header Branding */}
        <View style={styles.header}>
          <View style={styles.badgeRow}>
            <View style={styles.govBadge}>
              <Text style={styles.govBadgeText}>🏛️ GOVT OF AP • RTIH • NIC</Text>
            </View>
            <TouchableOpacity style={styles.logoutPill} onPress={handleLogout}>
              <Text style={styles.logoutText}>Logout ➔</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.logoSection}>
            <View style={styles.logoGlow}>
              <Text style={styles.shieldIcon}>🛡️</Text>
            </View>
            <Text style={styles.appName}>SECURESIGN</Text>
            <Text style={styles.appTagline}>Type-C DSC Mobile Signing Solution</Text>
          </View>
        </View>

        {/* Live Status Bar */}
        <View style={styles.statusCard}>
          <View style={styles.statusDotRow}>
            <View style={[styles.statusDot, { backgroundColor: tokens.length > 0 ? '#10B981' : '#38BDF8' }]} />
            <Text style={styles.statusText}>{statusMessage}</Text>
          </View>
        </View>

        {/* Main Hardware Section */}
        <View style={styles.mainCard}>
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>Hardware Token Interface</Text>
            <TouchableOpacity style={styles.scanBtn} onPress={scanForTokens} disabled={loading}>
              {loading ? (
                <ActivityIndicator size="small" color="#38BDF8" />
              ) : (
                <Text style={styles.scanBtnText}>🔄 Scan</Text>
              )}
            </TouchableOpacity>
          </View>

          {tokens.length > 0 ? (
            <View style={styles.tokenList}>
              {tokens.map((token, index) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.tokenItem,
                    connectedDevice === token.serialNumber && styles.tokenItemActive,
                  ]}
                  onPress={() => handleConnect(token.serialNumber)}
                  activeOpacity={0.7}
                >
                  <View style={styles.tokenIcon}>
                    <Text style={{ fontSize: 24 }}>🔌</Text>
                  </View>
                  <View style={styles.tokenInfo}>
                    <Text style={styles.tokenTitle}>{token.productName || 'Type-C DSC Dongle'}</Text>
                    <Text style={styles.tokenSub}>Vendor: {token.manufacturer || 'ePass / ProxKey'}</Text>
                    <Text style={styles.tokenSerial}>SN: {token.serialNumber || 'CCID-8892'}</Text>
                  </View>
                  <View style={styles.connectPill}>
                    <Text style={styles.connectPillText}>CONNECT ➔</Text>
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          ) : (
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyIcon}>⚡</Text>
              <Text style={styles.emptyTitle}>Insert Type-C DSC Token</Text>
              <Text style={styles.emptyDesc}>
                Plug your hardware cryptographic token directly into the USB Type-C port or via OTG adapter.
              </Text>
              
              <View style={styles.divider} />

              {/* 1-Tap Evaluator Sandbox Switch */}
              <TouchableOpacity
                style={styles.sandboxButton}
                onPress={handleLaunchSandbox}
                activeOpacity={0.8}
              >
                <Text style={styles.sandboxIcon}>🧪</Text>
                <View style={{ flex: 1 }}>
                  <Text style={styles.sandboxBtnTitle}>Launch Evaluator Sandbox</Text>
                  <Text style={styles.sandboxBtnSub}>Test complete 8-step signing flow without physical dongle</Text>
                </View>
                <Text style={styles.sandboxArrow}>➔</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>

        {/* Regulatory Compliance Cards */}
        <View style={styles.grid2}>
          <View style={styles.miniCard}>
            <Text style={styles.miniIcon}>🔒</Text>
            <Text style={styles.miniTitle}>Zero Key Leakage</Text>
            <Text style={styles.miniDesc}>Private key stays permanently inside hardware chip.</Text>
          </View>

          <View style={styles.miniCard}>
            <Text style={styles.miniIcon}>⏱️</Text>
            <Text style={styles.miniTitle}>RFC 3161 TSA</Text>
            <Text style={styles.miniDesc}>Time stamped PAdES-LTV legally valid signature.</Text>
          </View>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>SecureSign Innovation Challenge 2026 • 100% CCA Compliant</Text>
        </View>

      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B132B',
  },
  scrollContent: {
    padding: 16,
    paddingTop: Platform.OS === 'android' ? 30 : 16,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 16,
  },
  badgeRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  govBadge: {
    backgroundColor: 'rgba(56, 189, 248, 0.12)',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.3)',
  },
  govBadgeText: {
    color: '#38BDF8',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  logoutPill: {
    backgroundColor: 'rgba(239, 68, 68, 0.12)',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(239, 68, 68, 0.3)',
  },
  logoutText: {
    color: '#EF4444',
    fontSize: 11,
    fontWeight: '600',
  },
  logoSection: {
    alignItems: 'center',
    marginVertical: 8,
  },
  logoGlow: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#172554',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#38BDF8',
    shadowColor: '#38BDF8',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 8,
    marginBottom: 8,
  },
  shieldIcon: {
    fontSize: 30,
  },
  appName: {
    fontSize: 22,
    fontWeight: '900',
    color: '#FFFFFF',
    letterSpacing: 2,
  },
  appTagline: {
    fontSize: 12,
    color: '#94A3B8',
    marginTop: 2,
  },
  statusCard: {
    backgroundColor: '#172554',
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.2)',
  },
  statusDotRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 8,
  },
  statusText: {
    color: '#E2E8F0',
    fontSize: 12,
    fontWeight: '600',
    flex: 1,
  },
  mainCard: {
    backgroundColor: '#111C3D',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.25)',
    marginBottom: 16,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  cardTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  scanBtn: {
    backgroundColor: 'rgba(56, 189, 248, 0.15)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.4)',
  },
  scanBtnText: {
    color: '#38BDF8',
    fontSize: 12,
    fontWeight: '700',
  },
  tokenList: {
    gap: 10,
  },
  tokenItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E293B',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.3)',
  },
  tokenItemActive: {
    borderColor: '#10B981',
    backgroundColor: '#132E2E',
  },
  tokenIcon: {
    marginRight: 12,
  },
  tokenInfo: {
    flex: 1,
  },
  tokenTitle: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  tokenSub: {
    color: '#94A3B8',
    fontSize: 11,
    marginTop: 2,
  },
  tokenSerial: {
    color: '#38BDF8',
    fontSize: 10,
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
    marginTop: 2,
  },
  connectPill: {
    backgroundColor: '#10B981',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  connectPillText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: '800',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  emptyIcon: {
    fontSize: 32,
    color: '#38BDF8',
    marginBottom: 6,
  },
  emptyTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  emptyDesc: {
    fontSize: 12,
    color: '#94A3B8',
    textAlign: 'center',
    marginTop: 4,
    lineHeight: 18,
    paddingHorizontal: 10,
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.08)',
    width: '100%',
    marginVertical: 14,
  },
  sandboxButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(56, 189, 248, 0.12)',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#38BDF8',
    width: '100%',
  },
  sandboxIcon: {
    fontSize: 22,
    marginRight: 10,
  },
  sandboxBtnTitle: {
    color: '#38BDF8',
    fontSize: 13,
    fontWeight: '700',
  },
  sandboxBtnSub: {
    color: '#94A3B8',
    fontSize: 10,
    marginTop: 2,
  },
  sandboxArrow: {
    color: '#38BDF8',
    fontSize: 16,
    fontWeight: '700',
    marginLeft: 6,
  },
  grid2: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  miniCard: {
    flex: 1,
    backgroundColor: '#111C3D',
    borderRadius: 12,
    padding: 12,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.06)',
  },
  miniIcon: {
    fontSize: 20,
    marginBottom: 6,
  },
  miniTitle: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '700',
  },
  miniDesc: {
    color: '#94A3B8',
    fontSize: 10,
    marginTop: 2,
    lineHeight: 14,
  },
  footer: {
    alignItems: 'center',
    marginTop: 10,
  },
  footerText: {
    color: '#64748B',
    fontSize: 10,
  },
});

export default HomeScreen;

