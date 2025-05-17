<template>
  <div class="mfa-setup">
    <h2>Set Up Two-Factor Authentication</h2>
    
    <div class="setup-steps">
      <div class="step" :class="{ 'active': currentStep === 1, 'completed': currentStep > 1 }">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>Install Authenticator App</h3>
          <p>Download and install an authenticator app on your mobile device:</p>
          <div class="app-options">
            <div class="app-option">
              <img src="@/assets/google-authenticator.png" alt="Google Authenticator" />
              <span>Google Authenticator</span>
            </div>
            <div class="app-option">
              <img src="@/assets/authy.png" alt="Authy" />
              <span>Authy</span>
            </div>
            <div class="app-option">
              <img src="@/assets/microsoft-authenticator.png" alt="Microsoft Authenticator" />
              <span>Microsoft Authenticator</span>
            </div>
          </div>
          <button @click="goToStep(2)" class="btn-next">Continue</button>
        </div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 2, 'completed': currentStep > 2 }">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>Scan QR Code</h3>
          <p>Open your authenticator app and scan this QR code:</p>
          <div class="qr-container">
            <div v-if="isLoadingQR" class="loading-qr">Loading QR code...</div>
            <img v-else :src="qrCodeUrl" alt="QR Code" class="qr-code" />
          </div>
          <div class="manual-entry">
            <p>Can't scan the code? Use this key instead:</p>
            <div class="secret-key">
              <code>{{ secretKey }}</code>
              <button @click="copySecretKey" class="btn-copy">
                <span v-if="copied">Copied!</span>
                <span v-else>Copy</span>
              </button>
            </div>
          </div>
          <button @click="goToStep(3)" class="btn-next">Continue</button>
        </div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 3 }">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>Verify Code</h3>
          <p>Enter the 6-digit code from your authenticator app:</p>
          <div class="verification-code">
            <input 
              type="text" 
              v-model="verificationCode" 
              maxlength="6" 
              placeholder="000000"
              @input="onCodeInput"
            />
          </div>
          <div v-if="verificationError" class="error-message">
            {{ verificationError }}
          </div>
          <button 
            @click="verifyCode" 
            class="btn-verify" 
            :disabled="verificationCode.length !== 6 || isVerifying"
          >
            {{ isVerifying ? 'Verifying...' : 'Verify and Enable 2FA' }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="setupComplete" class="setup-complete">
      <div class="success-icon">✓</div>
      <h3>Two-Factor Authentication Enabled</h3>
      <p>Your account is now more secure. You'll be asked for a verification code when you sign in.</p>
      <div class="recovery-codes">
        <h4>Recovery Codes</h4>
        <p>Save these recovery codes in a secure place. You can use them to access your account if you lose your authenticator device.</p>
        <div class="codes-container">
          <ul>
            <li v-for="(code, index) in recoveryCodes" :key="index">{{ code }}</li>
          </ul>
        </div>
        <button @click="downloadRecoveryCodes" class="btn-download">
          Download Recovery Codes
        </button>
      </div>
      <button @click="finishSetup" class="btn-finish">Finish Setup</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const currentStep = ref(1);
const isLoadingQR = ref(true);
const qrCodeUrl = ref('');
const secretKey = ref('');
const verificationCode = ref('');
const verificationError = ref('');
const isVerifying = ref(false);
const copied = ref(false);
const setupComplete = ref(false);
const recoveryCodes = ref([]);

// Mock data for QR code and secret key
const mockQrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=otpauth://totp/WealthMap:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=WealthMap';
const mockSecretKey = 'JBSWY3DPEHPK3PXP';
const mockRecoveryCodes = [
  'a1b2c3d4e5f6',
  'g7h8i9j0k1l2',
  'm3n4o5p6q7r8',
  's9t0u1v2w3x4',
  'y5z6a7b8c9d0'
];

onMounted(async () => {
  // In a real app, you would fetch the QR code and secret key from your API
  // Simulating API call
  setTimeout(() => {
    qrCodeUrl.value = mockQrUrl;
    secretKey.value = mockSecretKey;
    isLoadingQR.value = false;
  }, 1500);
});

const goToStep = (step) => {
  currentStep.value = step;
};

const copySecretKey = () => {
  navigator.clipboard.writeText(secretKey.value);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};

const onCodeInput = (event) => {
  // Only allow digits
  verificationCode.value = event.target.value.replace(/\D/g, '');
  verificationError.value = '';
};

const verifyCode = async () => {
  if (verificationCode.value.length !== 6) {
    verificationError.value = 'Please enter a 6-digit code';
    return;
  }
  
  try {
    isVerifying.value = true;
    verificationError.value = '';
    
    // Simulate API call to verify the code
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // In a real app, you would call your API here
    // const response = await verifyMfaCode(verificationCode.value);
    
    // For demo purposes, we'll accept any code
    setupComplete.value = true;
    recoveryCodes.value = mockRecoveryCodes;
    
  } catch (err) {
    verificationError.value = 'Invalid verification code. Please try again.';
  } finally {
    isVerifying.value = false;
  }
};

const downloadRecoveryCodes = () => {
  const codesText = recoveryCodes.value.join('\n');
  const blob = new Blob([codesText], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = 'wealthmap-recovery-codes.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};

const finishSetup = () => {
  // In a real app, you might redirect to the dashboard or settings page
  router.push('/settings/security');
};
</script>

<style scoped>
.mfa-setup {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  margin-bottom: 2rem;
  text-align: center;
  color: #333;
}

.setup-steps {
  position: relative;
}

.step {
  display: flex;
  margin-bottom: 2rem;
  opacity: 0.5;
}

.step.active {
  opacity: 1;
}

.step.completed {
  opacity: 0.8;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e2e8f0;
  color: #4a5568;
  font-weight: bold;
  margin-right: 1rem;
  flex-shrink: 0;
}

.step.active .step-number {
  background-color: #4a6cf7;
  color: white;
}

.step.completed .step-number {
  background-color: #48bb78;
  color: white;
}

.step-content {
  flex: 1;
}

h3 {
  margin-bottom: 0.75rem;
  color: #2d3748;
}

p {
  margin-bottom: 1rem;
  color: #4a5568;
}

.app-options {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.app-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  width: 120px;
}

.app-option img {
  width: 48px;
  height: 48px;
  margin-bottom: 0.5rem;
}

.qr-container {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0;
  min-height: 200px;
  align-items: center;
}

.loading-qr {
  color: #718096;
}

.qr-code {
  width: 200px;
  height: 200px;
  border: 1px solid #e2e8f0;
  padding: 0.5rem;
  background-color: white;
}

.manual-entry {
  margin: 1.5rem 0;
  padding: 1rem;
  background-color: #f7fafc;
  border-radius: 8px;
}

.secret-key {
  display: flex;
  align-items: center;
  background-color: white;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

code {
  font-family: monospace;
  font-size: 1.1rem;
  letter-spacing: 1px;
  flex: 1;
}

.btn-copy {
  background-color: #edf2f7;
  color: #4a5568;
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.verification-code {
  margin: 1.5rem 0;
}

.verification-code input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1.5rem;
  text-align: center;
  letter-spacing: 4px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.btn-next, .btn-verify, .btn-finish {
  padding: 0.75rem 1.5rem;
  background-color: #4a6cf7;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-next:hover, .btn-verify:hover, .btn-finish:hover {
  background-color: #3a5ce5;
}

.btn-verify:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.error-message {
  color: #e53e3e;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.setup-complete {
  text-align: center;
  padding: 2rem;
  background-color: #f7fafc;
  border-radius: 8px;
}

.success-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background-color: #48bb78;
  color: white;
  font-size: 2rem;
  border-radius: 50%;
  margin: 0 auto 1.5rem;
}

.recovery-codes {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  text-align: left;
}

.codes-container {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f7fafc;
  border-radius: 4px;
}

.codes-container ul {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
}

.codes-container li {
  font-family: monospace;
  padding: 0.5rem;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  text-align: center;
}

.btn-download {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #4a5568;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.btn-download:hover {
  background-color: #2d3748;
}
</style>