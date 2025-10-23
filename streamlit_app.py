import streamlit as st
import requests
import json
import os
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Harem CRM - Application Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .application-form {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏛️ Harem CRM Application Portal</h1>
    <p>Professional Application Management System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Application Form", "Application Status", "About", "Contact"]
)

if page == "Application Form":
    st.markdown("""
    <div class="info-box">
        <h3>📝 Application Instructions</h3>
        <p>Please fill out the application form below completely and accurately. All information will be kept confidential and secure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("harem_application_form"):
        st.markdown('<div class="application-form">', unsafe_allow_html=True)
        
        # Personal Information Section
        st.header("👤 Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", help="Your legal first name")
            last_name = st.text_input("Last Name *", help="Your legal last name")
            email = st.text_input("Email Address *", help="Your primary email for communication")
            phone = st.text_input("Phone Number", help="Your contact phone number")
        
        with col2:
            age = st.number_input("Age *", min_value=18, max_value=99, help="You must be 18 or older to apply")
            location = st.text_input("Location (City, State) *", help="Where are you currently located?")
            pronouns = st.selectbox("Pronouns", ["Prefer not to say", "she/her", "he/him", "they/them", "other"])
        
        # Physical Information Section
        st.header("💪 Physical Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            height_ft = st.number_input("Height (Feet)", min_value=4, max_value=7, value=5)
            height_in = st.number_input("Height (Inches)", min_value=0, max_value=11, value=6)
        
        with col2:
            weight = st.number_input("Weight (lbs)", min_value=80, max_value=300, value=140)
            body_type = st.selectbox("Body Type", ["Not specified", "Slim", "Athletic", "Average", "Curvy", "Plus Size"])
        
        with col3:
            hair_color = st.selectbox("Hair Color", ["Not specified", "Black", "Brown", "Blonde", "Red", "Gray", "Other"])
            eye_color = st.selectbox("Eye Color", ["Not specified", "Brown", "Blue", "Green", "Hazel", "Gray"])
        
        # Service Preferences Section
        st.header("🎯 Service Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Service Categories")
            domestic_services = st.checkbox("Domestic Services", help="Cleaning, cooking, household management")
            administrative = st.checkbox("Administrative", help="Office work, scheduling, organization")
            technical = st.checkbox("Technical", help="IT support, digital tasks, technical assistance")
            content_creation = st.checkbox("Content Creation", help="Photo/video content, social media, creative work")
        
        with col2:
            st.subheader("Availability")
            full_time = st.checkbox("Full Time", help="Available for full-time work")
            part_time = st.checkbox("Part Time", help="Available for part-time work")
            weekends = st.checkbox("Weekends", help="Available on weekends")
            evenings = st.checkbox("Evenings", help="Available in the evenings")
        
        # Experience and Interests Section
        st.header("🌟 Experience and Interests")
        
        experience = st.text_area(
            "Describe your relevant experience *",
            help="Tell us about your background, skills, and experience that would be relevant to this role.",
            height=100
        )
        
        skills = st.text_area(
            "What skills do you bring?",
            help="List any specific skills, talents, or abilities you have.",
            height=100
        )
        
        interests = st.text_area(
            "What are your primary interests and desires? *",
            help="Describe what you are looking for and what excites you in a dynamic.",
            height=100
        )
        
        limits = st.text_area(
            "Do you have any hard limits or boundaries?",
            help="Please list any activities or situations you absolutely will not engage in.",
            height=100
        )
        
        # Additional Information Section
        st.header("📋 Additional Information")
        
        availability = st.text_area(
            "Describe your general availability",
            help="How often are you available and during what times?",
            height=80
        )
        
        commitment = st.selectbox(
            "What level of commitment are you seeking?",
            ["Not specified", "Casual", "Regular", "Long-term", "Exclusive"],
            help="What kind of relationship or dynamic are you hoping for?"
        )
        
        referral = st.text_input("How did you hear about us?", help="e.g., website, friend, specific event")
        
        anything_else = st.text_area(
            "Is there anything else you'd like us to know?",
            help="Any additional information you'd like to share.",
            height=80
        )
        
        # Terms and Conditions
        st.markdown("---")
        agree_terms = st.checkbox(
            "I agree to the terms and conditions and privacy policy *",
            help="You must agree to the terms to submit your application"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
        
        if submitted:
            # Validation
            if not agree_terms:
                st.markdown("""
                <div class="error-message">
                    <strong>Error:</strong> You must agree to the terms and conditions to submit your application.
                </div>
                """, unsafe_allow_html=True)
            elif not all([first_name, last_name, email, age, location, interests]):
                st.markdown("""
                <div class="error-message">
                    <strong>Error:</strong> Please fill in all required fields (marked with *).
                </div>
                """, unsafe_allow_html=True)
            else:
                # Prepare application data
                application_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "age": age,
                    "location": location,
                    "pronouns": pronouns,
                    "height_ft": height_ft,
                    "height_in": height_in,
                    "weight": weight,
                    "body_type": body_type,
                    "hair_color": hair_color,
                    "eye_color": eye_color,
                    "domestic_services": domestic_services,
                    "administrative": administrative,
                    "technical": technical,
                    "content_creation": content_creation,
                    "full_time": full_time,
                    "part_time": part_time,
                    "weekends": weekends,
                    "evenings": evenings,
                    "experience": experience,
                    "skills": skills,
                    "interests": interests,
                    "limits": limits,
                    "availability": availability,
                    "commitment": commitment,
                    "referral": referral,
                    "anything_else": anything_else,
                    "submitted_at": datetime.now().isoformat(),
                    "source": "streamlit_portal"
                }
                
                # In a real implementation, you would send this to your backend API
                # For now, we'll store it in session state and show a success message
                st.session_state.application_data = application_data
                st.session_state.application_submitted = True
                
                st.markdown("""
                <div class="success-message">
                    <h3>✅ Application Submitted Successfully!</h3>
                    <p>Thank you for your application. We will review it and get back to you within 3-5 business days.</p>
                    <p><strong>Application ID:</strong> {}</p>
                </div>
                """.format(f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}"), unsafe_allow_html=True)
                
                # Show submitted data for confirmation
                with st.expander("📋 Review Your Application", expanded=False):
                    st.json(application_data)

elif page == "Application Status":
    st.header("🔍 Check Application Status")
    
    st.markdown("""
    <div class="info-box">
        <p>Enter your email address to check the status of your application.</p>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Email Address", help="Enter the email address you used for your application")
    
    if st.button("Check Status", use_container_width=True):
        if email:
            # In a real implementation, you would query your database
            # For demo purposes, we'll show a mock status
            st.markdown("""
            <div class="success-message">
                <h3>📊 Application Status</h3>
                <p><strong>Status:</strong> Under Review</p>
                <p><strong>Submitted:</strong> {}</p>
                <p><strong>Estimated Review Time:</strong> 3-5 business days</p>
            </div>
            """.format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-message">
                <strong>Error:</strong> Please enter your email address.
            </div>
            """, unsafe_allow_html=True)

elif page == "About":
    st.header("🏛️ About Harem CRM")
    
    st.markdown("""
    <div class="info-box">
        <h3>Professional Application Management System</h3>
        <p>Harem CRM is a comprehensive application management system designed to streamline the recruitment and management process for professional services.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Our Mission")
        st.write("""
        To provide a secure, efficient, and professional platform for managing applications and building strong professional relationships.
        """)
        
        st.subheader("🔒 Security & Privacy")
        st.write("""
        - End-to-end encryption for all sensitive data
        - GDPR and CCPA compliant
        - Secure file upload and storage
        - Regular security audits
        """)
    
    with col2:
        st.subheader("✨ Features")
        st.write("""
        - Comprehensive application forms
        - Real-time status tracking
        - Secure document management
        - Professional communication tools
        """)
        
        st.subheader("📊 Analytics")
        st.write("""
        - Application tracking and analytics
        - Performance metrics
        - Reporting and insights
        - Data-driven decision making
        """)

elif page == "Contact":
    st.header("📞 Contact Information")
    
    st.markdown("""
    <div class="info-box">
        <h3>Get in Touch</h3>
        <p>Have questions about the application process or need assistance? We're here to help.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📧 Email Support")
        st.write("**General Inquiries:** support@harem-crm.com")
        st.write("**Technical Support:** tech@harem-crm.com")
        st.write("**Privacy Questions:** privacy@harem-crm.com")
    
    with col2:
        st.subheader("⏰ Support Hours")
        st.write("**Monday - Friday:** 9:00 AM - 6:00 PM EST")
        st.write("**Saturday:** 10:00 AM - 4:00 PM EST")
        st.write("**Sunday:** Closed")
    
    st.subheader("🔒 Privacy & Security")
    st.write("""
    - All communications are encrypted and secure
    - Your privacy is our top priority
    - We never share your information without consent
    - Regular security audits ensure your data is protected
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>© 2025 Harem CRM. All rights reserved. | <a href="/privacy">Privacy Policy</a> | <a href="/terms">Terms of Service</a></p>
</div>
""", unsafe_allow_html=True)
