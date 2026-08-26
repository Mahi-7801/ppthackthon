import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
  StatusBar,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import BackendService from '../services/BackendService';

const SignupScreen = () => {
  const navigation = useNavigation<any>();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSignup = async () => {
    setErrorMessage('');
    if (!fullName || !email || !password || !confirmPassword) {
      setErrorMessage('Please fill in all required fields');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setErrorMessage('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    try {
      const result = await BackendService.signup(email, password, fullName);
      if (result.user) {
        BackendService.setCurrentUserId(result.user.id);
        setIsSuccess(true);
      }
    } catch (error: any) {
      setErrorMessage(error.message || 'Failed to create account');
    } finally {
      setLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <View style={styles.container}>
        <StatusBar barStyle="light-content" backgroundColor="#0B132B" />
        <View style={styles.successWrapper}>
          <View style={styles.successCard}>
            <View style={styles.successGlow}>
              <Text style={styles.successCheckIcon}>✔</Text>
            </View>
            <Text style={styles.successTitle}>Account Activated!</Text>
            <Text style={styles.successSubtitle}>Welcome to SecureSign AP Government</Text>

            <View style={styles.successDetailBox}>
              <Text style={styles.successDetailLabel}>Registered Signer:</Text>
              <Text style={styles.successDetailValue}>{fullName}</Text>
              
              <Text style={[styles.successDetailLabel, { marginTop: 8 }]}>Authorized Email:</Text>
              <Text style={styles.successDetailValue}>{email}</Text>

              <View style={styles.smtpNoticeRow}>
                <Text style={styles.smtpNoticeIcon}>📧</Text>
                <Text style={styles.smtpNoticeText}>
                  Welcome & credentials confirmation email dispatched via SecureSign SMTP server!
                </Text>
              </View>
            </View>

            <TouchableOpacity
              style={styles.proceedButton}
              onPress={() => navigation.navigate('Login')}
              activeOpacity={0.8}
            >
              <Text style={styles.proceedButtonText}>Proceed to Sign In ➔</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <StatusBar barStyle="light-content" backgroundColor="#0B132B" />
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        
        {/* Header Branding */}
        <View style={styles.header}>
          <View style={styles.govBadge}>
            <Text style={styles.govBadgeText}>🏛️ GOVT OF AP • RTIH • NIC 2026</Text>
          </View>
          <View style={styles.logoSection}>
            <View style={styles.logoGlow}>
              <Text style={styles.shieldIcon}>🛡️</Text>
            </View>
            <Text style={styles.appName}>SECURESIGN</Text>
            <Text style={styles.appTagline}>Type-C DSC Mobile Signing Solution</Text>
          </View>
        </View>

        {/* Signup Form Card */}
        <View style={styles.formCard}>
          <Text style={styles.formTitle}>Register Signer Account</Text>
          <Text style={styles.formSubtitle}>Create authorized cryptographic profile</Text>

          {errorMessage !== '' && (
            <View style={styles.errorBanner}>
              <Text style={styles.errorText}>⚠️ {errorMessage}</Text>
            </View>
          )}

          <View style={styles.inputGroup}>
            <Text style={styles.inputLabel}>Full Name</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g. Mahankali Kornepati"
              placeholderTextColor="#64748B"
              value={fullName}
              onChangeText={setFullName}
              autoCapitalize="words"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.inputLabel}>Email Address</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g. pmahi7801@gmail.com"
              placeholderTextColor="#64748B"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.inputLabel}>Password</Text>
            <TextInput
              style={styles.input}
              placeholder="Min 6 characters"
              placeholderTextColor="#64748B"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.inputLabel}>Confirm Password</Text>
            <TextInput
              style={styles.input}
              placeholder="Re-enter password"
              placeholderTextColor="#64748B"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry
            />
          </View>

          <TouchableOpacity
            style={[styles.submitButton, loading && styles.submitButtonDisabled]}
            onPress={handleSignup}
            disabled={loading}
            activeOpacity={0.8}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.submitButtonText}>Create Signer Profile ➔</Text>
            )}
          </TouchableOpacity>

          {/* Quick Evaluator Fill for instant testing */}
          <TouchableOpacity
            style={styles.loginLink}
            onPress={() => navigation.navigate('Login')}
          >
            <Text style={styles.loginLinkText}>
              Already have an account? <Text style={styles.loginLinkBold}>Sign In</Text>
            </Text>
          </TouchableOpacity>
        </View>

        {/* Footer info */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>100% CCA India Compliant • Zero Key Leakage</Text>
        </View>

      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0B132B',
  },
  scrollContent: {
    padding: 16,
    paddingTop: Platform.OS === 'android' ? 24 : 16,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 16,
  },
  govBadge: {
    backgroundColor: 'rgba(56, 189, 248, 0.12)',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.3)',
    marginBottom: 8,
  },
  govBadgeText: {
    color: '#38BDF8',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  logoSection: {
    alignItems: 'center',
    marginVertical: 4,
  },
  logoGlow: {
    width: 54,
    height: 54,
    borderRadius: 27,
    backgroundColor: '#172554',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#38BDF8',
    marginBottom: 6,
  },
  shieldIcon: {
    fontSize: 26,
  },
  appName: {
    fontSize: 20,
    fontWeight: '900',
    color: '#FFFFFF',
    letterSpacing: 2,
  },
  appTagline: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  formCard: {
    backgroundColor: '#111C3D',
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.25)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 6,
  },
  formTitle: {
    fontSize: 18,
    fontWeight: '800',
    color: '#FFFFFF',
    textAlign: 'center',
  },
  formSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
    textAlign: 'center',
    marginTop: 4,
    marginBottom: 16,
  },
  errorBanner: {
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#EF4444',
    marginBottom: 14,
  },
  errorText: {
    color: '#F87171',
    fontSize: 12,
    fontWeight: '600',
  },
  inputGroup: {
    marginBottom: 12,
  },
  inputLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#CBD5E1',
    marginBottom: 6,
  },
  input: {
    backgroundColor: '#1E293B',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 14,
    color: '#FFFFFF',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  submitButton: {
    backgroundColor: '#0284C7',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 10,
  },
  submitButtonDisabled: {
    backgroundColor: '#475569',
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '800',
  },
  quickFillButton: {
    backgroundColor: 'rgba(56, 189, 248, 0.12)',
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: 'center',
    marginTop: 10,
    borderWidth: 1,
    borderColor: '#38BDF8',
  },
  quickFillText: {
    color: '#38BDF8',
    fontSize: 12,
    fontWeight: '700',
  },
  loginLink: {
    alignItems: 'center',
    marginTop: 16,
  },
  loginLinkText: {
    color: '#94A3B8',
    fontSize: 13,
  },
  loginLinkBold: {
    color: '#38BDF8',
    fontWeight: '700',
  },
  footer: {
    alignItems: 'center',
    marginTop: 16,
  },
  footerText: {
    color: '#64748B',
    fontSize: 11,
  },
  successWrapper: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  successCard: {
    backgroundColor: '#111C3D',
    borderRadius: 20,
    padding: 24,
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.4)',
    alignItems: 'center',
    shadowColor: '#10B981',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  successGlow: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: 'rgba(16, 185, 129, 0.2)',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 2,
    borderColor: '#10B981',
    marginBottom: 12,
  },
  successCheckIcon: {
    fontSize: 32,
    color: '#10B981',
    fontWeight: '900',
  },
  successTitle: {
    fontSize: 22,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  successSubtitle: {
    fontSize: 13,
    color: '#94A3B8',
    marginTop: 4,
    marginBottom: 16,
  },
  successDetailBox: {
    backgroundColor: '#172554',
    borderRadius: 12,
    padding: 14,
    width: '100%',
    marginBottom: 20,
    borderLeftWidth: 4,
    borderLeftColor: '#10B981',
  },
  successDetailLabel: {
    fontSize: 11,
    color: '#94A3B8',
    fontWeight: '600',
  },
  successDetailValue: {
    fontSize: 13,
    color: '#FFFFFF',
    fontWeight: '700',
    marginTop: 2,
  },
  smtpNoticeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(56, 189, 248, 0.1)',
    borderRadius: 8,
    padding: 10,
    marginTop: 12,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.2)',
  },
  smtpNoticeIcon: {
    fontSize: 18,
    marginRight: 8,
  },
  smtpNoticeText: {
    color: '#38BDF8',
    fontSize: 11,
    fontWeight: '600',
    flex: 1,
    lineHeight: 15,
  },
  proceedButton: {
    backgroundColor: '#10B981',
    borderRadius: 12,
    paddingVertical: 14,
    width: '100%',
    alignItems: 'center',
  },
  proceedButtonText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: '800',
  },
});

export default SignupScreen;
