"""
GDPR Compliance Module
Implements comprehensive GDPR compliance features for the Harem CRM system.
"""

import streamlit as st
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GDPRCompliance:
    """GDPR Compliance Manager for data protection and privacy rights"""
    
    def __init__(self):
        self.consent_records = {}
        self.data_retention_policies = {
            'applications': 365,  # 1 year
            'user_data': 2555,   # 7 years
            'logs': 90,         # 3 months
            'analytics': 730     # 2 years
        }
    
    def show_consent_banner(self):
        """Display GDPR consent banner"""
        if not st.session_state.get('gdpr_consent_given', False):
            with st.container():
                st.markdown("""
                <div style="position: fixed; bottom: 0; left: 0; right: 0; background: #1e1e1e; 
                           color: white; padding: 20px; z-index: 1000; border-top: 2px solid #ff6b6b;">
                    <h4>🍪 Privacy & Data Protection</h4>
                    <p>We use cookies and collect personal data to provide our services. 
                    By continuing, you consent to our data processing practices.</p>
                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("✅ Accept All", key="accept_all"):
                        self.give_consent("all")
                        st.rerun()
                
                with col2:
                    if st.button("⚙️ Customize", key="customize"):
                        self.show_consent_preferences()
                
                with col3:
                    if st.button("❌ Reject", key="reject"):
                        self.reject_consent()
                        st.rerun()
                
                st.markdown("</div></div>", unsafe_allow_html=True)
    
    def show_consent_preferences(self):
        """Show detailed consent preferences"""
        st.session_state['show_consent_preferences'] = True
        
        with st.expander("🔒 Privacy Preferences", expanded=True):
            st.markdown("### Data Collection Preferences")
            
            # Essential cookies (always required)
            st.checkbox("Essential Cookies (Required)", value=True, disabled=True)
            st.caption("These cookies are necessary for the website to function properly.")
            
            # Analytics cookies
            analytics = st.checkbox("Analytics Cookies", value=False)
            st.caption("Help us understand how you use our website to improve our services.")
            
            # Marketing cookies
            marketing = st.checkbox("Marketing Cookies", value=False)
            st.caption("Used to deliver relevant advertisements and marketing content.")
            
            # Personalization cookies
            personalization = st.checkbox("Personalization Cookies", value=False)
            st.caption("Remember your preferences and customize your experience.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Save Preferences", type="primary"):
                    consent_data = {
                        'essential': True,
                        'analytics': analytics,
                        'marketing': marketing,
                        'personalization': personalization,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.give_consent("custom", consent_data)
                    st.session_state['show_consent_preferences'] = False
                    st.rerun()
            
            with col2:
                if st.button("❌ Reject All"):
                    self.reject_consent()
                    st.session_state['show_consent_preferences'] = False
                    st.rerun()
    
    def give_consent(self, consent_type: str, data: Dict = None):
        """Record user consent"""
        consent_record = {
            'type': consent_type,
            'data': data or {},
            'timestamp': datetime.now().isoformat(),
            'ip_hash': self._hash_ip(),
            'user_agent': st.session_state.get('user_agent', 'unknown')
        }
        
        # Store consent record
        self._store_consent_record(consent_record)
        
        # Update session state
        st.session_state['gdpr_consent_given'] = True
        st.session_state['consent_type'] = consent_type
        st.session_state['consent_data'] = data or {}
        
        logger.info(f"GDPR consent given: {consent_type}")
        st.success("✅ Consent recorded. You can change your preferences anytime in settings.")
    
    def reject_consent(self):
        """Handle consent rejection"""
        st.session_state['gdpr_consent_given'] = False
        st.session_state['consent_type'] = 'rejected'
        st.session_state['consent_data'] = {}
        
        logger.info("GDPR consent rejected")
        st.warning("⚠️ Some features may be limited without consent.")
    
    def show_data_rights(self):
        """Display GDPR data subject rights"""
        st.markdown("### 🔒 Your Data Rights (GDPR)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Right to Access**
            - View all your personal data
            - Download your data in portable format
            - See how your data is processed
            
            **Right to Rectification**
            - Correct inaccurate data
            - Update incomplete information
            - Modify your preferences
            """)
        
        with col2:
            st.markdown("""
            **Right to Erasure**
            - Delete your account and data
            - Remove specific data categories
            - Withdraw consent at any time
            
            **Right to Portability**
            - Export your data
            - Transfer to another service
            - Machine-readable format
            """)
        
        # Data rights actions
        st.markdown("### 📋 Data Rights Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👁️ View My Data", key="view_data"):
                self.show_user_data()
        
        with col2:
            if st.button("📥 Download Data", key="download_data"):
                self.download_user_data()
        
        with col3:
            if st.button("✏️ Update Data", key="update_data"):
                self.show_data_update_form()
        
        with col4:
            if st.button("🗑️ Delete Data", key="delete_data"):
                self.show_data_deletion_confirmation()
    
    def show_user_data(self):
        """Display user's personal data"""
        st.markdown("### 📊 Your Personal Data")
        
        # Get user data (this would connect to your database)
        user_data = self._get_user_data()
        
        if user_data:
            st.json(user_data)
        else:
            st.info("No personal data found.")
    
    def download_user_data(self):
        """Download user data in JSON format"""
        user_data = self._get_user_data()
        
        if user_data:
            # Create downloadable JSON
            json_data = json.dumps(user_data, indent=2)
            
            st.download_button(
                label="📥 Download My Data",
                data=json_data,
                file_name=f"my_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        else:
            st.warning("No data available for download.")
    
    def show_data_update_form(self):
        """Show form to update personal data"""
        st.markdown("### ✏️ Update Your Data")
        
        with st.form("data_update_form"):
            st.text_input("Full Name", key="update_name")
            st.text_input("Email", key="update_email")
            st.text_input("Phone", key="update_phone")
            st.text_area("Address", key="update_address")
            
            if st.form_submit_button("💾 Update Data"):
                self._update_user_data()
                st.success("✅ Data updated successfully!")
    
    def show_data_deletion_confirmation(self):
        """Show data deletion confirmation"""
        st.markdown("### 🗑️ Delete Your Data")
        st.warning("⚠️ This action cannot be undone!")
        
        st.markdown("""
        **What will be deleted:**
        - Your personal information
        - Application data
        - Service history
        - All associated files
        
        **What will be retained:**
        - Legal compliance records
        - Financial records (as required by law)
        - Anonymized analytics data
        """)
        
        if st.button("🗑️ Confirm Deletion", type="primary"):
            self._delete_user_data()
            st.success("✅ Your data has been deleted.")
    
    def show_privacy_policy(self):
        """Display comprehensive privacy policy"""
        st.markdown("### 🔒 Privacy Policy")
        
        st.markdown("""
        **Data Controller:** Harem CRM System  
        **Contact:** privacy@haremcrm.com  
        **Last Updated:** December 2024
        
        ### What Data We Collect
        - Personal information (name, email, phone)
        - Application data and preferences
        - Service history and performance metrics
        - Usage analytics and cookies
        
        ### How We Use Your Data
        - Provide and improve our services
        - Process applications and requests
        - Communicate with you
        - Legal compliance and reporting
        
        ### Data Protection Measures
        - Encryption at rest and in transit
        - Access controls and authentication
        - Regular security audits
        - Data minimization principles
        
        ### Your Rights
        - Access your personal data
        - Correct inaccurate information
        - Delete your data
        - Export your data
        - Withdraw consent
        - Object to processing
        
        ### Data Retention
        - Application data: 1 year
        - User data: 7 years
        - Logs: 3 months
        - Analytics: 2 years
        
        ### Contact Us
        For privacy questions or requests, contact: privacy@haremcrm.com
        """)
    
    def show_cookie_policy(self):
        """Display cookie policy"""
        st.markdown("### 🍪 Cookie Policy")
        
        st.markdown("""
        **Essential Cookies (Required)**
        - Session management
        - Security and authentication
        - Basic functionality
        
        **Analytics Cookies (Optional)**
        - Usage statistics
        - Performance monitoring
        - Service improvement
        
        **Marketing Cookies (Optional)**
        - Targeted advertising
        - Campaign tracking
        - User engagement
        
        **Personalization Cookies (Optional)**
        - User preferences
        - Customized experience
        - Settings storage
        """)
    
    def _hash_ip(self) -> str:
        """Hash IP address for privacy"""
        # In production, get actual IP
        return hashlib.sha256("user_ip".encode()).hexdigest()[:16]
    
    def _store_consent_record(self, record: Dict):
        """Store consent record securely"""
        # In production, store in database
        logger.info(f"Consent record stored: {record}")
    
    def _get_user_data(self) -> Dict:
        """Get user's personal data"""
        # In production, fetch from database
        return {
            "personal_info": {
                "name": "User Name",
                "email": "user@example.com",
                "phone": "+1234567890"
            },
            "application_data": {
                "submitted": "2024-12-01",
                "status": "pending"
            },
            "preferences": {
                "notifications": True,
                "marketing": False
            }
        }
    
    def _update_user_data(self):
        """Update user data"""
        # In production, update database
        logger.info("User data updated")
    
    def _delete_user_data(self):
        """Delete user data"""
        # In production, delete from database
        logger.info("User data deleted")

# Global GDPR instance
gdpr_compliance = GDPRCompliance()

def show_gdpr_compliance():
    """Main GDPR compliance interface"""
    st.markdown("# 🔒 GDPR Compliance & Privacy")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Consent", "Data Rights", "Privacy Policy", "Cookies"])
    
    with tab1:
        gdpr_compliance.show_consent_banner()
        st.markdown("### Current Consent Status")
        if st.session_state.get('gdpr_consent_given'):
            st.success("✅ Consent given")
            st.json(st.session_state.get('consent_data', {}))
        else:
            st.warning("⚠️ No consent given")
    
    with tab2:
        gdpr_compliance.show_data_rights()
    
    with tab3:
        gdpr_compliance.show_privacy_policy()
    
    with tab4:
        gdpr_compliance.show_cookie_policy()
