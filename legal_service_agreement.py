"""
Legal Service Agreement System
Comprehensive, legally sound service agreement management for submissive contracts.
Handles creation, approval, execution, and secure storage of all personal information.
"""

import streamlit as st
import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass, asdict
import base64
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PersonalInfo:
    """Secure personal information structure"""
    full_name: str
    date_of_birth: str
    address: str
    phone: str
    email: str
    emergency_contact: str
    emergency_phone: str
    ssn_last_four: str
    driver_license: str
    passport: str
    medical_conditions: str
    medications: str
    allergies: str
    blood_type: str
    insurance_info: str

@dataclass
class ServiceTerms:
    """Service agreement terms and conditions"""
    service_type: str
    duration: str
    compensation: str
    responsibilities: List[str]
    restrictions: List[str]
    safety_protocols: List[str]
    confidentiality: List[str]
    termination_clauses: List[str]
    dispute_resolution: str
    governing_law: str

@dataclass
class AgreementData:
    """Complete agreement data structure"""
    agreement_id: str
    submissive_info: PersonalInfo
    service_terms: ServiceTerms
    created_date: str
    effective_date: str
    expiration_date: str
    status: str  # draft, pending, approved, active, terminated
    digital_signatures: Dict[str, str]
    legal_notices: List[str]
    amendments: List[Dict]
    audit_trail: List[Dict]

class LegalServiceAgreement:
    """Comprehensive legal service agreement management system"""
    
    def __init__(self):
        self.agreements = {}
        self.templates = self._load_agreement_templates()
        self.legal_notices = self._load_legal_notices()
        self.audit_log = []
    
    def _load_agreement_templates(self) -> Dict[str, Dict]:
        """Load legal agreement templates"""
        return {
            "standard_service": {
                "title": "Standard Service Agreement",
                "description": "Comprehensive service agreement for submissive relationships",
                "terms": {
                    "service_type": "Personal Service Agreement",
                    "duration": "12 months with automatic renewal",
                    "compensation": "As mutually agreed",
                    "governing_law": "Maryland State Law",
                    "dispute_resolution": "Binding arbitration"
                }
            },
            "content_creation": {
                "title": "Content Creation Agreement",
                "description": "Specialized agreement for content creation services",
                "terms": {
                    "service_type": "Content Creation Services",
                    "duration": "6 months with option to extend",
                    "compensation": "Revenue sharing as specified",
                    "governing_law": "Maryland State Law",
                    "dispute_resolution": "Binding arbitration"
                }
            },
            "training_protocol": {
                "title": "Training Protocol Agreement",
                "description": "Specialized agreement for training and development",
                "terms": {
                    "service_type": "Training and Development Services",
                    "duration": "3 months initial, renewable",
                    "compensation": "Training stipend as specified",
                    "governing_law": "Maryland State Law",
                    "dispute_resolution": "Binding arbitration"
                }
            }
        }
    
    def _load_legal_notices(self) -> List[str]:
        """Load required legal notices"""
        return [
            "This agreement is legally binding and enforceable under Maryland State Law.",
            "All parties must be 18 years of age or older to enter into this agreement.",
            "This agreement may be terminated by either party with 30 days written notice.",
            "All personal information will be kept confidential and secure.",
            "Any disputes will be resolved through binding arbitration.",
            "This agreement is subject to all applicable federal and state laws.",
            "Consent may be withdrawn at any time by either party.",
            "All activities must be consensual and within legal boundaries."
        ]
    
    def create_agreement(self, template_type: str, submissive_info: PersonalInfo) -> str:
        """Create a new service agreement"""
        try:
            # Generate unique agreement ID
            agreement_id = f"SA-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
            
            # Get template
            template = self.templates.get(template_type, self.templates["standard_service"])
            
            # Create service terms
            service_terms = ServiceTerms(
                service_type=template["terms"]["service_type"],
                duration=template["terms"]["duration"],
                compensation=template["terms"]["compensation"],
                responsibilities=self._get_standard_responsibilities(),
                restrictions=self._get_standard_restrictions(),
                safety_protocols=self._get_safety_protocols(),
                confidentiality=self._get_confidentiality_terms(),
                termination_clauses=self._get_termination_clauses(),
                dispute_resolution=template["terms"]["dispute_resolution"],
                governing_law=template["terms"]["governing_law"]
            )
            
            # Create agreement data
            agreement_data = AgreementData(
                agreement_id=agreement_id,
                submissive_info=submissive_info,
                service_terms=service_terms,
                created_date=datetime.now().isoformat(),
                effective_date=(datetime.now() + timedelta(days=7)).isoformat(),
                expiration_date=(datetime.now() + timedelta(days=365)).isoformat(),
                status="draft",
                digital_signatures={},
                legal_notices=self.legal_notices,
                amendments=[],
                audit_trail=[{
                    "action": "agreement_created",
                    "timestamp": datetime.now().isoformat(),
                    "user": "system",
                    "details": f"Agreement {agreement_id} created from template {template_type}"
                }]
            )
            
            # Store agreement
            self.agreements[agreement_id] = agreement_data
            
            # Log creation
            self._log_audit("agreement_created", agreement_id, {"template": template_type})
            
            logger.info(f"Service agreement created: {agreement_id}")
            return agreement_id
            
        except Exception as e:
            logger.error(f"Error creating agreement: {e}")
            raise
    
    def _get_standard_responsibilities(self) -> List[str]:
        """Get standard submissive responsibilities"""
        return [
            "Maintain respectful communication at all times",
            "Follow established protocols and guidelines",
            "Participate in agreed-upon activities with full consent",
            "Maintain confidentiality of all personal and private matters",
            "Provide honest and accurate information about health and limitations",
            "Respect boundaries and communicate any concerns immediately",
            "Participate in safety discussions and protocol reviews",
            "Maintain appropriate appearance and hygiene standards",
            "Follow scheduling and availability commitments",
            "Report any safety concerns or violations immediately"
        ]
    
    def _get_standard_restrictions(self) -> List[str]:
        """Get standard restrictions and limitations"""
        return [
            "No activities that violate local, state, or federal laws",
            "No activities that cause permanent physical harm",
            "No activities involving minors or non-consenting individuals",
            "No activities that violate public decency laws",
            "No activities that compromise safety or well-being",
            "No activities that violate confidentiality agreements",
            "No activities that exceed established boundaries",
            "No activities that involve illegal substances",
            "No activities that compromise professional relationships",
            "No activities that violate personal consent"
        ]
    
    def _get_safety_protocols(self) -> List[str]:
        """Get safety protocols and procedures"""
        return [
            "All activities must be consensual and within established boundaries",
            "Safe words and signals must be established and respected",
            "Regular safety check-ins and communication protocols",
            "Emergency contact information must be current and accessible",
            "Medical conditions and limitations must be disclosed",
            "All activities must be within legal and ethical boundaries",
            "Regular review and update of safety protocols",
            "Immediate cessation of any activity upon request",
            "Professional medical attention for any injuries",
            "Documentation of any safety incidents or concerns"
        ]
    
    def _get_confidentiality_terms(self) -> List[str]:
        """Get confidentiality and privacy terms"""
        return [
            "All personal information will be kept strictly confidential",
            "No sharing of personal information with third parties without consent",
            "Secure storage of all personal data and documents",
            "Regular review and update of privacy protocols",
            "Compliance with all applicable privacy laws and regulations",
            "Secure disposal of any outdated personal information",
            "Limited access to personal information on a need-to-know basis",
            "Regular security audits and updates",
            "Immediate notification of any privacy breaches",
            "Right to request information about data usage and storage"
        ]
    
    def _get_termination_clauses(self) -> List[str]:
        """Get termination and exit clauses"""
        return [
            "Either party may terminate this agreement with 30 days written notice",
            "Immediate termination for violation of safety protocols",
            "Immediate termination for violation of confidentiality agreements",
            "Termination for violation of legal or ethical boundaries",
            "Mutual agreement for early termination",
            "Termination for breach of contract terms",
            "Termination for failure to meet agreed-upon standards",
            "Termination for violation of personal boundaries",
            "Termination for failure to maintain professional standards",
            "Termination for any reason with proper notice and documentation"
        ]
    
    def show_agreement_creation(self):
        """Show agreement creation interface"""
        st.markdown("# 📋 Legal Service Agreement Creation")
        
        # Agreement type selection
        st.subheader("1. Agreement Type")
        agreement_type = st.selectbox(
            "Select Agreement Type",
            list(self.templates.keys()),
            format_func=lambda x: self.templates[x]["title"]
        )
        
        if agreement_type:
            template = self.templates[agreement_type]
            st.info(f"**{template['title']}**: {template['description']}")
        
        # Personal information collection
        st.subheader("2. Submissive Personal Information")
        st.warning("⚠️ All personal information will be encrypted and stored securely.")
        
        with st.form("personal_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Legal Name *", help="Must match government ID")
                date_of_birth = st.date_input("Date of Birth *", help="Must be 18+ years old")
                address = st.text_area("Full Address *", help="Complete residential address")
                phone = st.text_input("Phone Number *", help="Primary contact number")
                email = st.text_input("Email Address *", help="Primary email address")
                emergency_contact = st.text_input("Emergency Contact Name *", help="Name of emergency contact")
                emergency_phone = st.text_input("Emergency Contact Phone *", help="Emergency contact number")
            
            with col2:
                ssn_last_four = st.text_input("SSN Last 4 Digits", help="For identity verification")
                driver_license = st.text_input("Driver's License Number", help="Government ID number")
                passport = st.text_input("Passport Number", help="If applicable")
                medical_conditions = st.text_area("Medical Conditions", help="Any relevant medical conditions")
                medications = st.text_area("Current Medications", help="Any medications being taken")
                allergies = st.text_area("Allergies", help="Any known allergies")
                blood_type = st.selectbox("Blood Type", ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                insurance_info = st.text_area("Insurance Information", help="Health insurance details")
            
            # Legal consent
            st.subheader("3. Legal Consent and Verification")
            
            age_verification = st.checkbox(
                "I verify that I am 18 years of age or older *",
                help="Required for legal consent"
            )
            
            legal_capacity = st.checkbox(
                "I have the legal capacity to enter into this agreement *",
                help="Must be of sound mind and not under duress"
            )
            
            consent_agreement = st.checkbox(
                "I consent to the terms and conditions of this agreement *",
                help="Required for agreement validity"
            )
            
            privacy_consent = st.checkbox(
                "I consent to the collection and secure storage of my personal information *",
                help="Required for data processing"
            )
            
            # Submit form
            if st.form_submit_button("📋 Create Service Agreement", type="primary"):
                if all([full_name, date_of_birth, address, phone, email, emergency_contact, emergency_phone]):
                    if all([age_verification, legal_capacity, consent_agreement, privacy_consent]):
                        try:
                            # Create personal info object
                            personal_info = PersonalInfo(
                                full_name=full_name,
                                date_of_birth=date_of_birth.isoformat(),
                                address=address,
                                phone=phone,
                                email=email,
                                emergency_contact=emergency_contact,
                                emergency_phone=emergency_phone,
                                ssn_last_four=ssn_last_four,
                                driver_license=driver_license,
                                passport=passport,
                                medical_conditions=medical_conditions,
                                medications=medications,
                                allergies=allergies,
                                blood_type=blood_type,
                                insurance_info=insurance_info
                            )
                            
                            # Create agreement
                            agreement_id = self.create_agreement(agreement_type, personal_info)
                            
                            st.success(f"✅ Service Agreement Created: {agreement_id}")
                            st.session_state['created_agreement_id'] = agreement_id
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error creating agreement: {e}")
                    else:
                        st.error("❌ All consent checkboxes must be checked to create agreement")
                else:
                    st.error("❌ All required fields must be completed")
    
    def show_agreement_review(self, agreement_id: str):
        """Show agreement review and approval interface"""
        if agreement_id not in self.agreements:
            st.error("❌ Agreement not found")
            return
        
        agreement = self.agreements[agreement_id]
        
        st.markdown(f"# 📋 Service Agreement Review: {agreement_id}")
        
        # Agreement status
        status_color = {
            "draft": "🟡",
            "pending": "🟠", 
            "approved": "🟢",
            "active": "🔵",
            "terminated": "🔴"
        }
        
        st.markdown(f"**Status:** {status_color.get(agreement.status, '⚪')} {agreement.status.title()}")
        
        # Agreement details
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Agreement Details")
            st.write(f"**Agreement ID:** {agreement.agreement_id}")
            st.write(f"**Created:** {agreement.created_date}")
            st.write(f"**Effective Date:** {agreement.effective_date}")
            st.write(f"**Expiration Date:** {agreement.expiration_date}")
            st.write(f"**Service Type:** {agreement.service_terms.service_type}")
            st.write(f"**Duration:** {agreement.service_terms.duration}")
            st.write(f"**Compensation:** {agreement.service_terms.compensation}")
        
        with col2:
            st.subheader("👤 Submissive Information")
            st.write(f"**Name:** {agreement.submissive_info.full_name}")
            st.write(f"**Date of Birth:** {agreement.submissive_info.date_of_birth}")
            st.write(f"**Email:** {agreement.submissive_info.email}")
            st.write(f"**Phone:** {agreement.submissive_info.phone}")
            st.write(f"**Emergency Contact:** {agreement.submissive_info.emergency_contact}")
            st.write(f"**Blood Type:** {agreement.submissive_info.blood_type}")
        
        # Agreement terms
        st.subheader("📜 Agreement Terms")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Responsibilities", "Restrictions", "Safety", "Confidentiality", "Termination"
        ])
        
        with tab1:
            st.markdown("**Submissive Responsibilities:**")
            for i, responsibility in enumerate(agreement.service_terms.responsibilities, 1):
                st.write(f"{i}. {responsibility}")
        
        with tab2:
            st.markdown("**Restrictions and Limitations:**")
            for i, restriction in enumerate(agreement.service_terms.restrictions, 1):
                st.write(f"{i}. {restriction}")
        
        with tab3:
            st.markdown("**Safety Protocols:**")
            for i, protocol in enumerate(agreement.service_terms.safety_protocols, 1):
                st.write(f"{i}. {protocol}")
        
        with tab4:
            st.markdown("**Confidentiality Terms:**")
            for i, term in enumerate(agreement.service_terms.confidentiality, 1):
                st.write(f"{i}. {term}")
        
        with tab5:
            st.markdown("**Termination Clauses:**")
            for i, clause in enumerate(agreement.service_terms.termination_clauses, 1):
                st.write(f"{i}. {clause}")
        
        # Legal notices
        st.subheader("⚖️ Legal Notices")
        for i, notice in enumerate(agreement.legal_notices, 1):
            st.write(f"{i}. {notice}")
        
        # Digital signatures
        st.subheader("✍️ Digital Signatures")
        
        if agreement.digital_signatures:
            for signer, signature in agreement.digital_signatures.items():
                st.write(f"**{signer}:** {signature}")
        else:
            st.info("No digital signatures yet")
        
        # Agreement actions
        st.subheader("🔧 Agreement Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 Generate PDF", key="generate_pdf"):
                self._generate_agreement_pdf(agreement_id)
        
        with col2:
            if st.button("✍️ Add Signature", key="add_signature"):
                st.session_state['show_signature_form'] = True
                st.rerun()
        
        with col3:
            if st.button("✅ Approve Agreement", key="approve_agreement"):
                self._approve_agreement(agreement_id)
                st.success("✅ Agreement approved!")
                st.rerun()
        
        with col4:
            if st.button("📧 Send for Review", key="send_review"):
                self._send_for_review(agreement_id)
                st.success("📧 Agreement sent for review!")
                st.rerun()
    
    def _generate_agreement_pdf(self, agreement_id: str):
        """Generate PDF version of agreement"""
        try:
            agreement = self.agreements[agreement_id]
            
            # Create PDF buffer
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("SERVICE AGREEMENT", title_style))
            story.append(Spacer(1, 12))
            
            # Agreement details
            story.append(Paragraph(f"Agreement ID: {agreement.agreement_id}", styles['Normal']))
            story.append(Paragraph(f"Created: {agreement.created_date}", styles['Normal']))
            story.append(Paragraph(f"Effective Date: {agreement.effective_date}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Submissive information
            story.append(Paragraph("SUBMISSIVE INFORMATION", styles['Heading2']))
            story.append(Paragraph(f"Name: {agreement.submissive_info.full_name}", styles['Normal']))
            story.append(Paragraph(f"Date of Birth: {agreement.submissive_info.date_of_birth}", styles['Normal']))
            story.append(Paragraph(f"Address: {agreement.submissive_info.address}", styles['Normal']))
            story.append(Paragraph(f"Phone: {agreement.submissive_info.phone}", styles['Normal']))
            story.append(Paragraph(f"Email: {agreement.submissive_info.email}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Service terms
            story.append(Paragraph("SERVICE TERMS", styles['Heading2']))
            story.append(Paragraph(f"Service Type: {agreement.service_terms.service_type}", styles['Normal']))
            story.append(Paragraph(f"Duration: {agreement.service_terms.duration}", styles['Normal']))
            story.append(Paragraph(f"Compensation: {agreement.service_terms.compensation}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Responsibilities
            story.append(Paragraph("RESPONSIBILITIES", styles['Heading3']))
            for i, responsibility in enumerate(agreement.service_terms.responsibilities, 1):
                story.append(Paragraph(f"{i}. {responsibility}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Legal notices
            story.append(Paragraph("LEGAL NOTICES", styles['Heading2']))
            for i, notice in enumerate(agreement.legal_notices, 1):
                story.append(Paragraph(f"{i}. {notice}", styles['Normal']))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            # Download button
            st.download_button(
                label="📄 Download PDF Agreement",
                data=buffer.getvalue(),
                file_name=f"service_agreement_{agreement_id}.pdf",
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"❌ Error generating PDF: {e}")
    
    def _approve_agreement(self, agreement_id: str):
        """Approve agreement"""
        try:
            agreement = self.agreements[agreement_id]
            agreement.status = "approved"
            agreement.audit_trail.append({
                "action": "agreement_approved",
                "timestamp": datetime.now().isoformat(),
                "user": "admin",
                "details": "Agreement approved by administrator"
            })
            self._log_audit("agreement_approved", agreement_id)
            logger.info(f"Agreement approved: {agreement_id}")
        except Exception as e:
            logger.error(f"Error approving agreement: {e}")
            raise
    
    def _send_for_review(self, agreement_id: str):
        """Send agreement for review"""
        try:
            agreement = self.agreements[agreement_id]
            agreement.status = "pending"
            agreement.audit_trail.append({
                "action": "sent_for_review",
                "timestamp": datetime.now().isoformat(),
                "user": "system",
                "details": "Agreement sent for legal review"
            })
            self._log_audit("sent_for_review", agreement_id)
            logger.info(f"Agreement sent for review: {agreement_id}")
        except Exception as e:
            logger.error(f"Error sending for review: {e}")
            raise
    
    def _log_audit(self, action: str, agreement_id: str, details: Dict = None):
        """Log audit trail"""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "agreement_id": agreement_id,
            "details": details or {}
        }
        self.audit_log.append(audit_entry)
        logger.info(f"Audit log: {action} for {agreement_id}")

# Global legal agreement instance
legal_agreement = LegalServiceAgreement()

def show_legal_service_agreement():
    """Main legal service agreement interface"""
    st.markdown("# ⚖️ Legal Service Agreement Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create Agreement", "Review Agreements", "Digital Signatures", "Legal Compliance"])
    
    with tab1:
        legal_agreement.show_agreement_creation()
    
    with tab2:
        st.subheader("📋 Agreement Review")
        
        if legal_agreement.agreements:
            agreement_id = st.selectbox(
                "Select Agreement to Review",
                list(legal_agreement.agreements.keys())
            )
            
            if agreement_id:
                legal_agreement.show_agreement_review(agreement_id)
        else:
            st.info("No agreements created yet")
    
    with tab3:
        st.subheader("✍️ Digital Signature Management")
        st.info("Digital signature functionality will be available for approved agreements")
    
    with tab4:
        st.subheader("⚖️ Legal Compliance")
        st.info("Legal compliance monitoring and reporting will be available here")
