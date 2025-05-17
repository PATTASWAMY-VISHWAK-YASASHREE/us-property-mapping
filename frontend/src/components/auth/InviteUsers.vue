<template>
  <div class="invite-users">
    <h2>Invite Team Members</h2>
    <div class="invite-form">
      <div class="form-group">
        <label for="emails">Email Addresses</label>
        <textarea
          id="emails"
          v-model="emailsInput"
          placeholder="Enter email addresses (one per line or comma-separated)"
          rows="4"
        ></textarea>
        <small>Enter multiple email addresses separated by commas or new lines</small>
      </div>
      
      <div class="form-group">
        <label for="role">Role</label>
        <select id="role" v-model="selectedRole">
          <option v-for="role in availableRoles" :key="role.value" :value="role.value">
            {{ role.label }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="message">Personal Message (Optional)</label>
        <textarea
          id="message"
          v-model="personalMessage"
          placeholder="Add a personal message to the invitation email"
          rows="3"
        ></textarea>
      </div>
      
      <div class="form-actions">
        <button @click="handleInvite" :disabled="isLoading || !hasValidEmails">
          {{ isLoading ? 'Sending Invitations...' : 'Send Invitations' }}
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </div>
    
    <div v-if="pendingInvitations.length > 0" class="pending-invitations">
      <h3>Pending Invitations</h3>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Date Sent</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="invitation in pendingInvitations" :key="invitation.id">
            <td>{{ invitation.email }}</td>
            <td>{{ getRoleName(invitation.role) }}</td>
            <td>{{ formatDate(invitation.createdAt) }}</td>
            <td>{{ invitation.status }}</td>
            <td>
              <button 
                class="btn-resend" 
                @click="resendInvitation(invitation.id)"
                :disabled="isResending === invitation.id"
              >
                {{ isResending === invitation.id ? 'Resending...' : 'Resend' }}
              </button>
              <button 
                class="btn-cancel" 
                @click="cancelInvitation(invitation.id)"
                :disabled="isCancelling === invitation.id"
              >
                {{ isCancelling === invitation.id ? 'Cancelling...' : 'Cancel' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Mock data for available roles
const availableRoles = [
  { value: 'admin', label: 'Administrator' },
  { value: 'manager', label: 'Manager' },
  { value: 'analyst', label: 'Analyst' },
  { value: 'viewer', label: 'Viewer' }
];

// Form state
const emailsInput = ref('');
const selectedRole = ref('viewer');
const personalMessage = ref('');
const error = ref('');
const successMessage = ref('');
const isLoading = ref(false);
const isResending = ref(null);
const isCancelling = ref(null);

// Mock data for pending invitations
const pendingInvitations = ref([
  {
    id: 1,
    email: 'john.doe@example.com',
    role: 'analyst',
    createdAt: new Date(Date.now() - 86400000), // 1 day ago
    status: 'Pending'
  },
  {
    id: 2,
    email: 'jane.smith@example.com',
    role: 'manager',
    createdAt: new Date(Date.now() - 172800000), // 2 days ago
    status: 'Pending'
  }
]);

// Computed property to check if there are valid emails
const hasValidEmails = computed(() => {
  const emails = parseEmails(emailsInput.value);
  return emails.length > 0;
});

// Parse emails from input (comma or newline separated)
const parseEmails = (input) => {
  if (!input) return [];
  
  // Split by commas or newlines
  const rawEmails = input.split(/[,\n]+/);
  
  // Trim whitespace and filter out empty strings
  return rawEmails
    .map(email => email.trim())
    .filter(email => email && validateEmail(email));
};

// Simple email validation
const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

// Format date for display
const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

// Get role name from role value
const getRoleName = (roleValue) => {
  const role = availableRoles.find(r => r.value === roleValue);
  return role ? role.label : roleValue;
};

// Handle invite submission
const handleInvite = async () => {
  const emails = parseEmails(emailsInput.value);
  
  if (emails.length === 0) {
    error.value = 'Please enter at least one valid email address';
    return;
  }
  
  try {
    isLoading.value = true;
    error.value = '';
    successMessage.value = '';
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // In a real app, you would call your API here
    // await inviteUsers({ emails, role: selectedRole.value, message: personalMessage.value });
    
    successMessage.value = `Successfully sent invitations to ${emails.length} email(s)`;
    emailsInput.value = '';
    personalMessage.value = '';
    
    // Add to pending invitations (mock)
    const now = new Date();
    emails.forEach((email, index) => {
      pendingInvitations.value.push({
        id: Date.now() + index,
        email,
        role: selectedRole.value,
        createdAt: now,
        status: 'Pending'
      });
    });
    
  } catch (err) {
    error.value = err.message || 'Failed to send invitations. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Resend invitation
const resendInvitation = async (id) => {
  try {
    isResending.value = id;
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // In a real app, you would call your API here
    // await resendInvite(id);
    
    successMessage.value = 'Invitation resent successfully';
    error.value = '';
    
  } catch (err) {
    error.value = err.message || 'Failed to resend invitation';
    successMessage.value = '';
  } finally {
    isResending.value = null;
  }
};

// Cancel invitation
const cancelInvitation = async (id) => {
  try {
    isCancelling.value = id;
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // In a real app, you would call your API here
    // await cancelInvite(id);
    
    // Remove from pending invitations
    pendingInvitations.value = pendingInvitations.value.filter(inv => inv.id !== id);
    
    successMessage.value = 'Invitation cancelled successfully';
    error.value = '';
    
  } catch (err) {
    error.value = err.message || 'Failed to cancel invitation';
    successMessage.value = '';
  } finally {
    isCancelling.value = null;
  }
};
</script>

<style scoped>
.invite-users {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

h3 {
  margin: 2rem 0 1rem;
  color: #333;
}

.invite-form {
  background-color: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

textarea, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.75rem;
}

.form-actions {
  margin-top: 1.5rem;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #4a6cf7;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3a5ce5;
}

button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.error-message {
  color: #e53e3e;
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fed7d7;
  border-radius: 4px;
}

.success-message {
  color: #2f855a;
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #c6f6d5;
  border-radius: 4px;
}

.pending-invitations {
  margin-top: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #edf2f7;
}

th {
  background-color: #f7fafc;
  font-weight: 600;
}

.btn-resend, .btn-cancel {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  margin-right: 0.5rem;
}

.btn-cancel {
  background-color: #e53e3e;
}

.btn-cancel:hover {
  background-color: #c53030;
}
</style>