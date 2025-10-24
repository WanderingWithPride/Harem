"""
Digital Signature and Execution System
Comprehensive digital signature management for legal service agreements.
Handles secure signature capture, verification, and legal execution.
"""

import streamlit as st
import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DigitalSignatureSystem:
    """Comprehensive digital signature management system"""
    
    def __init__(self):
        self.signatures = {}
        self.signature_verification = {}
        self.execution_records = {}
        self.legal_requirements = self._load_legal_requirements()
    
    def _load_legal_requirements(self) -> Dict[str, Any]:
        """Load legal requirements for digital signatures"""
        return {
            "esign_act_compliance": {
                "title": "Electronic Signatures in Global and National Commerce Act (ESIGN)",
                "requirements": [
                    "Consent to electronic transactions",
                    "Clear identification of signer",
                    "Intent to sign the document",
            "Association of signature with the record",
                    "Retention of signature record"
                ]
            },
            "ueta_compliance": {
                "title": "Uniform Electronic Transactions Act (UETA)",
                "requirements": [
                    "Electronic signature must be attributable to the person",
                    "Signature must be made with intent to sign",
                    "Signature must be associated with the record",
                    "Record must be retained in its original form"
                ]
            },
            "maryland_law": {
                "title": "Maryland State Law Requirements",
                "requirements": [
                    "All parties must be 18 years of age or older",
                    "Consent must be explicit and informed",
                    "Signature must be legally binding",
                    "Record must be maintained for legal compliance"
                ]
            }
        }
    
    def show_signature_capture(self, agreement_id: str, signer_type: str):
        """Show digital signature capture interface"""
        st.markdown(f"# ✍️ Digital Signature Capture - {signer_type.title()}")
        
        # Legal compliance notice
        st.warning("""
        **⚖️ Legal Notice:** By providing your digital signature, you acknowledge that:
        - You are 18 years of age or older
        - You have the legal capacity to enter into this agreement
        - You consent to electronic transactions
        - Your signature is legally binding and enforceable
        """)
        
        # Signature capture methods
        st.subheader("📝 Signature Methods")
        
        method = st.radio(
            "Choose Signature Method:",
            ["Draw Signature", "Type Signature", "Upload Signature Image"],
            help="Select your preferred method for capturing your signature"
        )
        
        if method == "Draw Signature":
            self._show_draw_signature(agreement_id, signer_type)
        elif method == "Type Signature":
            self._show_type_signature(agreement_id, signer_type)
        elif method == "Upload Signature Image":
            self._show_upload_signature(agreement_id, signer_type)
    
    def _show_draw_signature(self, agreement_id: str, signer_type: str):
        """Show drawing signature interface"""
        st.subheader("🖊️ Draw Your Signature")
        
        # Signature canvas (simplified version for Streamlit)
        st.info("💡 **Signature Drawing:** Use the canvas below to draw your signature")
        
        # Create signature input
        signature_text = st.text_area(
            "Signature (Draw your signature in the text area):",
            height=100,
            help="Draw your signature using text characters or describe your signature"
        )
        
        # Signature verification
        st.subheader("🔍 Signature Verification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Legal Name *", help="Must match government ID")
            date_of_birth = st.date_input("Date of Birth *", help="Must be 18+ years old")
            email = st.text_input("Email Address *", help="For signature verification")
            phone = st.text_input("Phone Number *", help="For identity verification")
        
        with col2:
            id_type = st.selectbox("ID Type", ["Driver's License", "Passport", "State ID", "Other"])
            id_number = st.text_input("ID Number *", help="Government ID number")
            id_state = st.text_input("ID State/Country", help="Issuing state or country")
            ip_address = st.text_input("IP Address", value="Auto-detected", disabled=True)
        
        # Legal consent
        st.subheader("⚖️ Legal Consent")
        
        consent_esign = st.checkbox(
            "I consent to electronic signatures and transactions *",
            help="Required for ESIGN Act compliance"
        )
        
        consent_legal = st.checkbox(
            "I understand this signature is legally binding *",
            help="Required for legal validity"
        )
        
        consent_identity = st.checkbox(
            "I verify my identity and legal capacity *",
            help="Required for signature validity"
        )
        
        consent_retention = st.checkbox(
            "I consent to the retention of this signature record *",
            help="Required for legal compliance"
        )
        
        # Capture signature
        if st.button("✍️ Capture Digital Signature", type="primary"):
            if all([signature_text, full_name, date_of_birth, email, phone, id_number]):
                if all([consent_esign, consent_legal, consent_identity, consent_retention]):
                    try:
                        # Create signature record
                        signature_data = {
                            "signature_id": f"SIG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}",
                            "agreement_id": agreement_id,
                            "signer_type": signer_type,
                            "signature_method": "draw",
                            "signature_data": signature_text,
                            "signer_info": {
                                "full_name": full_name,
                                "date_of_birth": date_of_birth.isoformat(),
                                "email": email,
                                "phone": phone,
                                "id_type": id_type,
                                "id_number": id_number,
                                "id_state": id_state,
                                "ip_address": ip_address
                            },
                            "legal_consent": {
                                "esign_consent": consent_esign,
                                "legal_binding": consent_legal,
                                "identity_verification": consent_identity,
                                "record_retention": consent_retention
                            },
                            "timestamp": datetime.now().isoformat(),
                            "status": "captured",
                            "verification_hash": self._generate_verification_hash(signature_text, full_name, email)
                        }
                        
                        # Store signature
                        self.signatures[signature_data["signature_id"]] = signature_data
                        
                        st.success("✅ Digital signature captured successfully!")
                        st.info(f"**Signature ID:** {signature_data['signature_id']}")
                        st.info(f"**Verification Hash:** {signature_data['verification_hash']}")
                        
                        # Show signature summary
                        with st.expander("📋 Signature Summary", expanded=True):
                            st.json(signature_data)
                        
                    except Exception as e:
                        st.error(f"❌ Error capturing signature: {e}")
                else:
                    st.error("❌ All consent checkboxes must be checked")
            else:
                st.error("❌ All required fields must be completed")
    
    def _show_type_signature(self, agreement_id: str, signer_type: str):
        """Show typed signature interface"""
        st.subheader("⌨️ Type Your Signature")
        
        # Typed signature input
        typed_signature = st.text_input(
            "Type Your Full Legal Name:",
            help="Type your full legal name as it appears on your government ID"
        )
        
        # Signature style options
        col1, col2 = st.columns(2)
        
        with col1:
            signature_style = st.selectbox(
                "Signature Style",
                ["Standard", "Cursive", "Formal", "Informal"],
                help="Choose the style for your typed signature"
            )
        
        with col2:
            signature_font = st.selectbox(
                "Font Style",
                ["Arial", "Times New Roman", "Calibri", "Georgia"],
                help="Choose the font for your signature"
            )
        
        # Signature verification (same as draw signature)
        st.subheader("🔍 Signature Verification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Legal Name *", value=typed_signature, help="Must match government ID")
            date_of_birth = st.date_input("Date of Birth *", help="Must be 18+ years old")
            email = st.text_input("Email Address *", help="For signature verification")
        
        with col2:
            phone = st.text_input("Phone Number *", help="For identity verification")
            id_type = st.selectbox("ID Type", ["Driver's License", "Passport", "State ID", "Other"])
            id_number = st.text_input("ID Number *", help="Government ID number")
        
        # Legal consent (same as draw signature)
        st.subheader("⚖️ Legal Consent")
        
        consent_esign = st.checkbox("I consent to electronic signatures and transactions *")
        consent_legal = st.checkbox("I understand this signature is legally binding *")
        consent_identity = st.checkbox("I verify my identity and legal capacity *")
        consent_retention = st.checkbox("I consent to the retention of this signature record *")
        
        # Capture signature
        if st.button("✍️ Capture Typed Signature", type="primary"):
            if all([typed_signature, full_name, date_of_birth, email, phone, id_number]):
                if all([consent_esign, consent_legal, consent_identity, consent_retention]):
                    try:
                        # Create signature record
                        signature_data = {
                            "signature_id": f"SIG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}",
                            "agreement_id": agreement_id,
                            "signer_type": signer_type,
                            "signature_method": "type",
                            "signature_data": typed_signature,
                            "signature_style": signature_style,
                            "signature_font": signature_font,
                            "signer_info": {
                                "full_name": full_name,
                                "date_of_birth": date_of_birth.isoformat(),
                                "email": email,
                                "phone": phone,
                                "id_type": id_type,
                                "id_number": id_number
                            },
                            "legal_consent": {
                                "esign_consent": consent_esign,
                                "legal_binding": consent_legal,
                                "identity_verification": consent_identity,
                                "record_retention": consent_retention
                            },
                            "timestamp": datetime.now().isoformat(),
                            "status": "captured",
                            "verification_hash": self._generate_verification_hash(typed_signature, full_name, email)
                        }
                        
                        # Store signature
                        self.signatures[signature_data["signature_id"]] = signature_data
                        
                        st.success("✅ Typed signature captured successfully!")
                        st.info(f"**Signature ID:** {signature_data['signature_id']}")
                        
                    except Exception as e:
                        st.error(f"❌ Error capturing signature: {e}")
                else:
                    st.error("❌ All consent checkboxes must be checked")
            else:
                st.error("❌ All required fields must be completed")
    
    def _show_upload_signature(self, agreement_id: str, signer_type: str):
        """Show upload signature interface"""
        st.subheader("📤 Upload Signature Image")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Signature Image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image of your signature (PNG, JPG, JPEG)"
        )
        
        if uploaded_file:
            # Display uploaded image
            st.image(uploaded_file, caption="Uploaded Signature", use_column_width=True)
            
            # Signature verification
            st.subheader("🔍 Signature Verification")
            
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Legal Name *", help="Must match government ID")
                date_of_birth = st.date_input("Date of Birth *", help="Must be 18+ years old")
                email = st.text_input("Email Address *", help="For signature verification")
            
            with col2:
                phone = st.text_input("Phone Number *", help="For identity verification")
                id_type = st.selectbox("ID Type", ["Driver's License", "Passport", "State ID", "Other"])
                id_number = st.text_input("ID Number *", help="Government ID number")
            
            # Legal consent
            st.subheader("⚖️ Legal Consent")
            
            consent_esign = st.checkbox("I consent to electronic signatures and transactions *")
            consent_legal = st.checkbox("I understand this signature is legally binding *")
            consent_identity = st.checkbox("I verify my identity and legal capacity *")
            consent_retention = st.checkbox("I consent to the retention of this signature record *")
            
            # Capture signature
            if st.button("✍️ Capture Uploaded Signature", type="primary"):
                if all([full_name, date_of_birth, email, phone, id_number]):
                    if all([consent_esign, consent_legal, consent_identity, consent_retention]):
                        try:
                            # Convert image to base64
                            image_data = base64.b64encode(uploaded_file.getvalue()).decode()
                            
                            # Create signature record
                            signature_data = {
                                "signature_id": f"SIG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}",
                                "agreement_id": agreement_id,
                                "signer_type": signer_type,
                                "signature_method": "upload",
                                "signature_data": image_data,
                                "signer_info": {
                                    "full_name": full_name,
                                    "date_of_birth": date_of_birth.isoformat(),
                                    "email": email,
                                    "phone": phone,
                                    "id_type": id_type,
                                    "id_number": id_number
                                },
                                "legal_consent": {
                                    "esign_consent": consent_esign,
                                    "legal_binding": consent_legal,
                                    "identity_verification": consent_identity,
                                    "record_retention": consent_retention
                                },
                                "timestamp": datetime.now().isoformat(),
                                "status": "captured",
                                "verification_hash": self._generate_verification_hash(image_data, full_name, email)
                            }
                            
                            # Store signature
                            self.signatures[signature_data["signature_id"]] = signature_data
                            
                            st.success("✅ Uploaded signature captured successfully!")
                            st.info(f"**Signature ID:** {signature_data['signature_id']}")
                            
                        except Exception as e:
                            st.error(f"❌ Error capturing signature: {e}")
                    else:
                        st.error("❌ All consent checkboxes must be checked")
                else:
                    st.error("❌ All required fields must be completed")
    
    def _generate_verification_hash(self, signature_data: str, full_name: str, email: str) -> str:
        """Generate verification hash for signature"""
        combined_data = f"{signature_data}{full_name}{email}{datetime.now().isoformat()}"
        return hashlib.sha256(combined_data.encode()).hexdigest()
    
    def show_signature_verification(self, signature_id: str):
        """Show signature verification interface"""
        if signature_id not in self.signatures:
            st.error("❌ Signature not found")
            return
        
        signature = self.signatures[signature_id]
        
        st.markdown(f"# 🔍 Signature Verification: {signature_id}")
        
        # Signature details
        st.subheader("📋 Signature Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Signature ID:** {signature['signature_id']}")
            st.write(f"**Agreement ID:** {signature['agreement_id']}")
            st.write(f"**Signer Type:** {signature['signer_type']}")
            st.write(f"**Method:** {signature['signature_method']}")
            st.write(f"**Status:** {signature['status']}")
        
        with col2:
            st.write(f"**Timestamp:** {signature['timestamp']}")
            st.write(f"**Verification Hash:** {signature['verification_hash']}")
            st.write(f"**Full Name:** {signature['signer_info']['full_name']}")
            st.write(f"**Email:** {signature['signer_info']['email']}")
            st.write(f"**Phone:** {signature['signer_info']['phone']}")
        
        # Legal compliance check
        st.subheader("⚖️ Legal Compliance Check")
        
        compliance_status = self._check_legal_compliance(signature)
        
        for requirement, status in compliance_status.items():
            icon = "✅" if status else "❌"
            st.write(f"{icon} {requirement}")
        
        # Signature verification actions
        st.subheader("🔧 Verification Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Verify Signature", key="verify_signature"):
                self._verify_signature(signature_id)
                st.success("✅ Signature verified!")
                st.rerun()
        
        with col2:
            if st.button("❌ Reject Signature", key="reject_signature"):
                self._reject_signature(signature_id)
                st.warning("❌ Signature rejected!")
                st.rerun()
        
        with col3:
            if st.button("📄 Generate Certificate", key="generate_certificate"):
                self._generate_verification_certificate(signature_id)
    
    def _check_legal_compliance(self, signature: Dict) -> Dict[str, bool]:
        """Check legal compliance requirements"""
        compliance = {}
        
        # ESIGN Act compliance
        compliance["ESIGN Act Consent"] = signature['legal_consent']['esign_consent']
        compliance["Legal Binding Consent"] = signature['legal_consent']['legal_binding']
        compliance["Identity Verification"] = signature['legal_consent']['identity_verification']
        compliance["Record Retention Consent"] = signature['legal_consent']['record_retention']
        
        # Age verification
        dob = datetime.fromisoformat(signature['signer_info']['date_of_birth'])
        age = (datetime.now() - dob).days // 365
        compliance["Age 18+ Verification"] = age >= 18
        
        # Identity verification
        compliance["Full Name Provided"] = bool(signature['signer_info']['full_name'])
        compliance["Email Provided"] = bool(signature['signer_info']['email'])
        compliance["Phone Provided"] = bool(signature['signer_info']['phone'])
        compliance["ID Number Provided"] = bool(signature['signer_info']['id_number'])
        
        return compliance
    
    def _verify_signature(self, signature_id: str):
        """Verify signature"""
        try:
            signature = self.signatures[signature_id]
            signature['status'] = 'verified'
            signature['verification_timestamp'] = datetime.now().isoformat()
            self._log_verification(signature_id, "verified")
            logger.info(f"Signature verified: {signature_id}")
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            raise
    
    def _reject_signature(self, signature_id: str):
        """Reject signature"""
        try:
            signature = self.signatures[signature_id]
            signature['status'] = 'rejected'
            signature['rejection_timestamp'] = datetime.now().isoformat()
            self._log_verification(signature_id, "rejected")
            logger.info(f"Signature rejected: {signature_id}")
        except Exception as e:
            logger.error(f"Error rejecting signature: {e}")
            raise
    
    def _generate_verification_certificate(self, signature_id: str):
        """Generate verification certificate"""
        try:
            signature = self.signatures[signature_id]
            
            certificate = {
                "certificate_id": f"CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}",
                "signature_id": signature_id,
                "agreement_id": signature['agreement_id'],
                "signer_name": signature['signer_info']['full_name'],
                "verification_hash": signature['verification_hash'],
                "verification_timestamp": datetime.now().isoformat(),
                "legal_compliance": "Verified",
                "certificate_authority": "Harem CRM Legal System"
            }
            
            st.success("✅ Verification certificate generated!")
            st.json(certificate)
            
        except Exception as e:
            st.error(f"❌ Error generating certificate: {e}")
    
    def _log_verification(self, signature_id: str, action: str):
        """Log verification action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "signature_id": signature_id,
            "action": action,
            "user": "system"
        }
        self.signature_verification[signature_id] = log_entry
        logger.info(f"Verification log: {action} for {signature_id}")
    
    def show_signature_management(self):
        """Show signature management interface"""
        st.markdown("# ✍️ Digital Signature Management")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Capture Signature", "Verify Signatures", "Signature Records", "Legal Compliance"])
        
        with tab1:
            st.subheader("📝 Capture New Signature")
            
            agreement_id = st.text_input("Agreement ID", help="Enter the agreement ID for this signature")
            signer_type = st.selectbox("Signer Type", ["Submissive", "Dominant", "Witness", "Legal Representative"])
            
            if agreement_id and signer_type:
                self.show_signature_capture(agreement_id, signer_type)
        
        with tab2:
            st.subheader("🔍 Signature Verification")
            
            if self.signatures:
                signature_id = st.selectbox(
                    "Select Signature to Verify",
                    list(self.signatures.keys())
                )
                
                if signature_id:
                    self.show_signature_verification(signature_id)
            else:
                st.info("No signatures available for verification")
        
        with tab3:
            st.subheader("📋 Signature Records")
            
            if self.signatures:
                for sig_id, signature in self.signatures.items():
                    with st.expander(f"Signature {sig_id}"):
                        st.json(signature)
            else:
                st.info("No signature records available")
        
        with tab4:
            st.subheader("⚖️ Legal Compliance")
            
            st.markdown("### Legal Requirements")
            
            for law, requirements in self.legal_requirements.items():
                st.markdown(f"**{requirements['title']}**")
                for requirement in requirements['requirements']:
                    st.write(f"• {requirement}")
                st.write("")

# Global digital signature instance
digital_signature = DigitalSignatureSystem()

def show_digital_signature_system():
    """Main digital signature system interface"""
    digital_signature.show_signature_management()
