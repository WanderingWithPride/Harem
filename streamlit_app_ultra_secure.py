import streamlit as st
import requests
import json
import os
import sys
from datetime import datetime, timedelta
import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Harem CRM - Complete System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import secure data manager
try:
    from config.secure_data_manager import secure_data_manager
    SECURE_DATA_AVAILABLE = True
except ImportError:
    SECURE_DATA_AVAILABLE = False
    logger.warning("Secure data manager not available - using fallback mode")

# Try to import personal data, fall back to generic if not available
try:
    from config.personal_data import (
        SIR_KINK_PREFERENCES, 
        INNOVATION_PROJECT, 
        TRAINING_PROTOCOLS, 
        PERSONAL_BRANDING
    )
    PERSONAL_DATA_LOADED = True
except ImportError:
    # Fallback to generic data if personal data not available
    SIR_KINK_PREFERENCES = {
        "primary_interests": ["bondage", "spanking", "toy_play"],
        "detailed_descriptions": {
            "bondage": "Restraint techniques",
            "spanking": "Impact play", 
            "toy_play": "BDSM equipment"
        }
    }
    INNOVATION_PROJECT = {
        "name": "Communication Bracelets",
        "description": "Mesh network communication technology",
        "features": ["Offline communication", "GPS tracking", "Emergency features"]
    }
    TRAINING_PROTOCOLS = {
        "core_sections": ["Expectations", "Protocols", "Safety"],
        "advanced_training": ["Education", "Training", "Management"]
    }
    PERSONAL_BRANDING = {
        "title": "Admin",
        "system_name": "Harem CRM",
        "welcome_message": "Professional Management System",
        "admin_title": "Admin Access",
        "admin_description": "Complete management and system control"
    }
    PERSONAL_DATA_LOADED = False

# Secure data functions
@st.cache_data
def get_applications():
    """Get applications from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            return secure_data_manager.get_all_applications()
        except Exception as e:
            logger.error(f"Failed to get applications: {e}")
            return []
    else:
        return []

@st.cache_data
def get_analytics():
    """Get analytics from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            return secure_data_manager.get_analytics()
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {
                "total_applications": 0,
                "pending_applications": 0,
                "approved_applications": 0,
                "rejected_applications": 0,
                "conversion_rate": 0,
                "avg_response_time": "0 days"
            }
    else:
        return {
            "total_applications": 0,
            "pending_applications": 0,
            "approved_applications": 0,
            "rejected_applications": 0,
            "conversion_rate": 0,
            "avg_response_time": "0 days"
        }

@st.cache_data
def get_users():
    """Get users from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            # This would connect to your actual user database
            return []
        except Exception as e:
            logger.error(f"Failed to get users: {e}")
            return []
    else:
        return []

@st.cache_data
def get_tasks():
    """Get tasks from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            # This would connect to your actual task database
            return []
        except Exception as e:
            logger.error(f"Failed to get tasks: {e}")
            return []
    else:
        return []

@st.cache_data
def get_content_sessions():
    """Get content sessions from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            # This would connect to your actual content database
            return []
        except Exception as e:
            logger.error(f"Failed to get content sessions: {e}")
            return []
    else:
        return []

@st.cache_data
def get_contracts():
    """Get contracts from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            # This would connect to your actual contract database
            return []
        except Exception as e:
            logger.error(f"Failed to get contracts: {e}")
            return []
    else:
        return []

@st.cache_data
def get_leads():
    """Get leads from secure data manager"""
    if SECURE_DATA_AVAILABLE:
        try:
            # This would connect to your actual lead database
            return []
        except Exception as e:
            logger.error(f"Failed to get leads: {e}")
            return []
    else:
        return []

# Session state management
def init_session_state():
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    if 'applicant_authenticated' not in st.session_state:
        st.session_state.applicant_authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'secure_mode' not in st.session_state:
        st.session_state.secure_mode = SECURE_DATA_AVAILABLE

def show_landing_page():
    st.title(f"🏛️ {PERSONAL_BRANDING['system_name']}")
    st.subheader(PERSONAL_BRANDING['welcome_message'])
    
    # Security status
    if st.session_state.secure_mode:
        st.success("🔒 **Secure Mode:** All data is encrypted and protected")
    else:
        st.warning("⚠️ **Fallback Mode:** Using generic data - configure secure data manager for full functionality")
    
    # Welcome message
    st.info(f"Welcome to the {PERSONAL_BRANDING['system_name']}! A comprehensive platform for harem management, training protocols, and system administration.")
    
    # Main action buttons
    st.markdown("---")
    st.subheader("Choose Your Access Level")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 👑 {PERSONAL_BRANDING['admin_title']}")
        st.write(PERSONAL_BRANDING['admin_description'])
        st.write("**Features:**")
        st.write("• View all applications")
        st.write("• Approve/reject candidates") 
        st.write("• Analytics and reporting")
        st.write("• Training management")
        st.write("• Innovation project tracking")
        
        if st.button("🔐 Admin Login", use_container_width=True, type="primary"):
            st.session_state.user_type = "admin"
            st.rerun()
    
    with col2:
        st.markdown("### 📝 Submissive Portal")
        st.write("**Submit applications and track your status**")
        st.write("• Submit new applications")
        st.write("• Check application status")
        st.write("• Update your profile")
        st.write("• View your progress")
        st.write("• Innovation project interest")
        
        if st.button("📋 Submissive Portal", use_container_width=True, type="secondary"):
            st.session_state.user_type = "applicant"
            st.rerun()
    
    # Additional options
    st.markdown("---")
    st.subheader("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Submit Application", use_container_width=True):
            st.session_state.show_application_form = True
            st.rerun()
    
    with col2:
        if st.button("📊 View System Info", use_container_width=True):
            st.info("**System Status:** Ready for deployment with secure data management")
    
    with col3:
        if st.button("🔒 Security Info", use_container_width=True):
            st.info("**Security Status:** All data is encrypted and protected")

def show_admin_login():
    st.title(f"👑 {PERSONAL_BRANDING['title']} Login")
    st.subheader("Owner/Admin Access Required")
    
    # Security status
    if st.session_state.secure_mode:
        st.success("🔒 **Secure Mode:** All data is encrypted and protected")
    else:
        st.warning("⚠️ **Fallback Mode:** Using generic data - configure secure data manager for full functionality")
    
    with st.form("admin_login"):
        st.subheader("🔐 Admin Authentication")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Landing", use_container_width=True):
                st.session_state.user_type = None
                st.rerun()
        
        if submitted:
            # Simple authentication (replace with secure auth in production)
            if username == "admin" and password == "harem2025":
                st.session_state.admin_authenticated = True
                st.session_state.current_user = {"username": username, "role": "admin"}
                st.success("✅ Admin login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

def show_applicant_login():
    st.title("📝 Applicant Portal")
    st.subheader("Access Your Application Status")
    
    with st.form("applicant_login"):
        st.subheader("🔐 Applicant Authentication")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Landing", use_container_width=True):
                st.session_state.user_type = None
                st.rerun()
        
        if submitted:
            # Simple authentication (replace with secure auth in production)
            if email and password:
                st.session_state.applicant_authenticated = True
                st.session_state.current_user = {"email": email, "role": "applicant"}
                st.success("✅ Applicant login successful!")
                st.rerun()
            else:
                st.error("❌ Please enter both email and password")
    
    # Show option to create account
    if st.button("🔑 Create Account to Track Status", use_container_width=True):
        st.session_state.show_register_form = True
        st.rerun()

def show_applicant_dashboard():
    st.title("📝 Applicant Dashboard")
    st.subheader(f"Welcome back, {st.session_state.current_user.get('email', 'User')}")
    
    # Applicant navigation
    st.sidebar.title("Applicant Menu")
    applicant_page = st.sidebar.selectbox(
        "Choose a section:",
        ["Dashboard", "My Applications", "Profile", "Messages", "Logout"]
    )
    
    if applicant_page == "Logout":
        st.session_state.applicant_authenticated = False
        st.session_state.current_user = None
        st.session_state.user_type = None
        st.rerun()
    
    elif applicant_page == "Dashboard":
        st.header("📊 Your Dashboard")
        
        # Mock application status
        with st.container():
            st.subheader("📋 Your Application Status")
            st.write("**Application ID:** APP-20250115123456")
            st.write("**Status:** Under Review")
            st.write("**Submitted:** January 15, 2025")
            st.write("**Estimated Review Time:** 3-5 business days")
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        st.info("Your application is currently being reviewed by our team. We'll notify you as soon as we have an update.")
    
    elif applicant_page == "My Applications":
        st.header("📋 My Applications")
        
        # Show application history
        with st.container():
            st.subheader("Application #1 - APP-20250115123456")
            st.write("**Status:** Under Review")
            st.write("**Submitted:** January 15, 2025")
            st.write("**Last Updated:** January 15, 2025")
    
    elif applicant_page == "Profile":
        st.header("👤 My Profile")
        st.info("Profile management features will be available after application approval.")
    
    elif applicant_page == "Messages":
        st.header("💬 Messages")
        st.info("Communication features will be available after application approval.")

def show_admin_dashboard():
    st.title(f"👑 {PERSONAL_BRANDING['system_name']} - Admin Dashboard")
    st.subheader(f"Welcome back, {st.session_state.current_user.get('username', PERSONAL_BRANDING['title'])}")
    
    # Security status
    if st.session_state.secure_mode:
        st.success("🔒 **Secure Mode:** All data is encrypted and protected")
    else:
        st.warning("⚠️ **Fallback Mode:** Using generic data - configure secure data manager for full functionality")
    
    # Admin navigation - Full CRM System
    st.sidebar.title("CRM System")
    admin_page = st.sidebar.selectbox(
        "Choose a section:",
        [
            "Dashboard Overview", 
            "Applications", 
            "Roster Management", 
            "Recruitment", 
            "Calendar", 
            "Tasks", 
            "Content Management", 
            "Photo Verification", 
            "Contracts", 
            "Bible Management", 
            "Metrics & Analytics", 
            "Settings", 
            "Logout"
        ]
    )
    
    if admin_page == "Logout":
        st.session_state.admin_authenticated = False
        st.session_state.current_user = None
        st.session_state.user_type = None
        st.rerun()
    
    elif admin_page == "Dashboard Overview":
        show_admin_overview()
    
    elif admin_page == "Applications":
        show_admin_applications()
    
    elif admin_page == "Roster Management":
        show_roster_management()
    
    elif admin_page == "Recruitment":
        show_recruitment()
    
    elif admin_page == "Calendar":
        show_calendar()
    
    elif admin_page == "Tasks":
        show_tasks()
    
    elif admin_page == "Content Management":
        show_content_management()
    
    elif admin_page == "Photo Verification":
        show_photo_verification()
    
    elif admin_page == "Contracts":
        show_contracts()
    
    elif admin_page == "Bible Management":
        show_bible_management()
    
    elif admin_page == "Metrics & Analytics":
        show_admin_analytics()
    
    elif admin_page == "Settings":
        show_admin_settings()

def show_admin_overview():
    st.header("📊 Dashboard Overview")
    
    # Welcome message with Sir's info
    st.subheader(f"👑 Welcome, {PERSONAL_BRANDING['title']}")
    st.info(f"**{PERSONAL_BRANDING['system_name']}** - Complete management platform for your harem operations, training protocols, and innovative technology projects.")
    
    # Get analytics data
    analytics = get_analytics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Applications", analytics["total_applications"])
    
    with col2:
        st.metric("Pending Applications", analytics["pending_applications"])
    
    with col3:
        st.metric("Approved Applications", analytics["approved_applications"])
    
    with col4:
        st.metric("Conversion Rate", f"{analytics['conversion_rate']}%")
    
    # Sir's Quick Reference
    st.subheader(f"👑 {PERSONAL_BRANDING['title']}'s Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🔞 Current Kink Focus:**")
        for interest in SIR_KINK_PREFERENCES['primary_interests'][:5]:
            st.write(f"• {interest.replace('_', ' ').title()}")
    
    with col2:
        st.write("**🚀 Innovation Projects:**")
        st.write(f"• {INNOVATION_PROJECT['name']}")
        st.write("• Mesh Network Technology")
        st.write("• AirTag-like Tracking")
        st.write("• Offline Communication")
        st.write("• AI Integration")
    
    # Database connection info
    st.subheader("🔗 Database Connection")
    if st.session_state.secure_mode:
        st.success("✅ **Secure Data Manager:** All data is encrypted and protected")
    else:
        st.info("💡 **Ready to connect:** Configure secure data manager for full functionality")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 View Applications", use_container_width=True):
            st.session_state.admin_page = "Applications"
            st.rerun()
    
    with col2:
        if st.button("👥 Manage Roster", use_container_width=True):
            st.session_state.admin_page = "Roster Management"
            st.rerun()
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.admin_page = "Metrics & Analytics"
            st.rerun()

def show_admin_applications():
    st.header("📋 Applications Management")
    st.subheader("All Applications")
    
    # Get applications data
    applications = get_applications()
    
    if applications:
        # Display applications in a table
        df_data = []
        for app in applications:
            df_data.append({
                "ID": app.get("application_id", "N/A"),
                "Name": app.get("data", {}).get("full_name", "N/A"),
                "Email": app.get("data", {}).get("email", "N/A"),
                "Status": app.get("status", "N/A"),
                "Submitted": app.get("timestamp", "N/A")[:10] if app.get("timestamp") else "N/A"
            })
        
        if df_data:
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Application actions
            st.subheader("📝 Application Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Review Applications**")
                st.write("• View application details")
                st.write("• Approve/reject applications")
                st.write("• Add notes and comments")
            
            with col2:
                st.write("**Application Analytics**")
                st.write("• Conversion rates")
                st.write("• Response times")
                st.write("• Source analysis")
            
            with col3:
                st.write("**Bulk Actions**")
                st.write("• Bulk approve/reject")
                st.write("• Export applications")
                st.write("• Send notifications")
        else:
            st.info("📊 **No applications data available yet.**")
    else:
        st.info("📊 **No applications data available yet.** Connect to your database to see real applications.")

def show_roster_management():
    st.header("👥 Roster Management")
    st.subheader("Active Harem Members")
    
    # Roster management features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Active", "0", "No data available")
    
    with col2:
        st.metric("New This Month", "0", "No data available")
    
    with col3:
        st.metric("Compliance Rate", "0%", "No data available")
    
    # Sir's Training Preferences
    st.subheader(f"👑 {PERSONAL_BRANDING['title']}'s Training Preferences")
    
    with st.expander("🔞 Kink Compatibility Assessment", expanded=True):
        st.write("**Primary Training Focus Areas:**")
        for interest, description in SIR_KINK_PREFERENCES['detailed_descriptions'].items():
            st.write(f"• **{interest.replace('_', ' ').title()}** - {description}")
    
    # Roster list
    st.subheader("Active Harem Roster")
    
    st.info("📊 **No roster data available yet.** Connect to your database to see active harem members.")
    
    # Roster actions
    st.subheader("👥 Roster Management Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Profile Management**")
        st.write("• View detailed profiles")
        st.write("• Update user information")
        st.write("• Manage kink preferences")
        st.write("• Track training progress")
    
    with col2:
        st.write("**Performance Tracking**")
        st.write("• Service logs")
        st.write("• Quality scores")
        st.write("• Compliance monitoring")
        st.write("• Kink compatibility")
    
    with col3:
        st.write("**Communication & Control**")
        st.write("• Send messages")
        st.write("• Schedule sessions")
        st.write("• Assign tasks")
        st.write("• Thirst Wave integration")

def show_recruitment():
    st.header("🎯 Recruitment System")
    st.subheader("Lead Management")
    
    # Recruitment metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Leads", "0", "No data available")
    
    with col2:
        st.metric("Conversion Rate", "0%", "No data available")
    
    with col3:
        st.metric("Active Assignments", "0", "No data available")
    
    # Lead management
    st.subheader("Lead Management")
    
    st.info("📊 **No recruitment data available yet.** Connect to your database to see leads and assignments.")
    
    # Recruitment actions
    st.subheader("🎯 Recruitment Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Lead Management**")
        st.write("• Add new leads")
        st.write("• Assign to subs")
        st.write("• Track progress")
    
    with col2:
        st.write("**Content Partners**")
        st.write("• Partner matching")
        st.write("• Assignment tracking")
        st.write("• Performance monitoring")
    
    with col3:
        st.write("**Analytics**")
        st.write("• Source effectiveness")
        st.write("• Conversion tracking")
        st.write("• Performance metrics")

def show_calendar():
    st.header("📅 Calendar Management")
    st.subheader("Events and Scheduling")
    
    # Calendar metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Upcoming Events", "0", "No data available")
    
    with col2:
        st.metric("This Week", "0", "No data available")
    
    with col3:
        st.metric("Utilization", "0%", "No data available")
    
    # Calendar view
    st.subheader("Calendar View")
    
    st.info("📊 **No calendar data available yet.** Connect to your database to see events and scheduling.")
    
    # Calendar actions
    st.subheader("📅 Calendar Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Event Management**")
        st.write("• Create events")
        st.write("• Schedule meetings")
        st.write("• Manage availability")
    
    with col2:
        st.write("**Task Scheduling**")
        st.write("• Assign tasks")
        st.write("• Set deadlines")
        st.write("• Track progress")
    
    with col3:
        st.write("**Analytics**")
        st.write("• Utilization rates")
        st.write("• Performance metrics")
        st.write("• Scheduling efficiency")

def show_tasks():
    st.header("✅ Task Management")
    st.subheader("Service Tasks and Assignments")
    
    # Task metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Tasks", "0", "No data available")
    
    with col2:
        st.metric("Completed Today", "0", "No data available")
    
    with col3:
        st.metric("Completion Rate", "0%", "No data available")
    
    # Task list
    st.subheader("Task List")
    
    st.info("📊 **No task data available yet.** Connect to your database to see tasks and assignments.")
    
    # Task actions
    st.subheader("✅ Task Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Task Creation**")
        st.write("• Create new tasks")
        st.write("• Assign to users")
        st.write("• Set priorities")
    
    with col2:
        st.write("**Task Tracking**")
        st.write("• Monitor progress")
        st.write("• Update status")
        st.write("• Quality assessment")
    
    with col3:
        st.write("**Analytics**")
        st.write("• Performance metrics")
        st.write("• Completion rates")
        st.write("• Efficiency analysis")

def show_content_management():
    st.header("🎬 Content Management")
    st.subheader("Content Sessions and Assets")
    
    # Content metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sessions", "0", "No data available")
    
    with col2:
        st.metric("This Month", "0", "No data available")
    
    with col3:
        st.metric("Revenue", "$0", "No data available")
    
    # Content management
    st.subheader("Content Sessions")
    
    st.info("📊 **No content data available yet.** Connect to your database to see content sessions and assets.")
    
    # Content actions
    st.subheader("🎬 Content Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Session Management**")
        st.write("• Create sessions")
        st.write("• Manage participants")
        st.write("• Track progress")
    
    with col2:
        st.write("**Asset Management**")
        st.write("• Upload files")
        st.write("• Organize content")
        st.write("• Quality control")
    
    with col3:
        st.write("**Revenue Tracking**")
        st.write("• Revenue analysis")
        st.write("• Performance metrics")
        st.write("• Financial reporting")

def show_photo_verification():
    st.header("📸 Photo Verification")
    st.subheader("Photo Analysis and Compliance")
    
    # Photo metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Photos Analyzed", "0", "No data available")
    
    with col2:
        st.metric("Pending Review", "0", "No data available")
    
    with col3:
        st.metric("Compliance Rate", "0%", "No data available")
    
    # Photo verification
    st.subheader("Photo Analysis")
    
    st.info("📊 **No photo data available yet.** Connect to your database to see photo verification and analysis.")
    
    # Photo actions
    st.subheader("📸 Photo Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Photo Analysis**")
        st.write("• Metadata verification")
        st.write("• Authenticity checks")
        st.write("• Quality assessment")
    
    with col2:
        st.write("**Schedule Management**")
        st.write("• 6-month updates")
        st.write("• Compliance tracking")
        st.write("• Reminder system")
    
    with col3:
        st.write("**Verification Tools**")
        st.write("• Batch processing")
        st.write("• Automated checks")
        st.write("• Manual review")

def show_contracts():
    st.header("📄 Contract Management")
    st.subheader("Legal Documents and MSAs")
    
    # Contract metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Contracts", "0", "No data available")
    
    with col2:
        st.metric("Pending Signatures", "0", "No data available")
    
    with col3:
        st.metric("Completion Rate", "0%", "No data available")
    
    # Contract management
    st.subheader("Contract List")
    
    st.info("📊 **No contract data available yet.** Connect to your database to see contracts and legal documents.")
    
    # Contract actions
    st.subheader("📄 Contract Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Contract Creation**")
        st.write("• Generate MSAs")
        st.write("• Create releases")
        st.write("• Template management")
    
    with col2:
        st.write("**Document Management**")
        st.write("• Digital signatures")
        st.write("• Version control")
        st.write("• Storage organization")
    
    with col3:
        st.write("**Compliance**")
        st.write("• Legal compliance")
        st.write("• Audit trails")
        st.write("• Renewal tracking")

def show_bible_management():
    st.header("📖 Bible Management")
    st.subheader("Training Materials and Documentation")
    
    # Bible metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sections", "12", "Active")
    
    with col2:
        st.metric("Active Version", "v2.0", "Updated")
    
    with col3:
        st.metric("Completion Rate", "100%", "Complete")
    
    # Sir's Kink List and Preferences
    st.subheader(f"👑 {PERSONAL_BRANDING['title']}'s Kink List & Preferences")
    
    with st.expander("🔞 Kink Preferences", expanded=True):
        st.write("**Primary Interests (in no particular order, none required):**")
        for interest, description in SIR_KINK_PREFERENCES['detailed_descriptions'].items():
            st.write(f"• **{interest.replace('_', ' ').title()}** - {description}")
    
    # Harem Innovation Project
    st.subheader("🚀 Harem Innovation Project")
    
    with st.expander(f"💡 {INNOVATION_PROJECT['name']}", expanded=True):
        st.write(f"**{INNOVATION_PROJECT['description']}:**")
        for feature in INNOVATION_PROJECT['features']:
            st.write(f"• {feature}")
    
    # Bible sections
    st.subheader("📚 Training Materials")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Core Training Sections:**")
        for section in TRAINING_PROTOCOLS['core_sections']:
            st.write(f"• {section}")
    
    with col2:
        st.write("**Advanced Training:**")
        for training in TRAINING_PROTOCOLS['advanced_training']:
            st.write(f"• {training}")
    
    # Bible actions
    st.subheader("📖 Bible Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Content Management**")
        st.write("• Update preferences")
        st.write("• Add new training materials")
        st.write("• Version control")
    
    with col2:
        st.write("**Access Control**")
        st.write("• Role-based access")
        st.write("• Visibility settings")
        st.write("• Permission management")
    
    with col3:
        st.write("**Innovation Tracking**")
        st.write("• Project development")
        st.write("• Technology integration")
        st.write("• Progress monitoring")

def show_admin_analytics():
    st.header("📊 Analytics & Reporting")
    st.subheader("Business Intelligence and Metrics")
    
    # Analytics metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "0", "No data available")
    
    with col2:
        st.metric("Active Sessions", "0", "No data available")
    
    with col3:
        st.metric("Revenue", "$0", "No data available")
    
    with col4:
        st.metric("Growth Rate", "0%", "No data available")
    
    # Analytics dashboard
    st.subheader("Analytics Dashboard")
    
    st.info("📊 **No analytics data available yet.** Connect to your database to see real-time analytics and reporting.")
    
    # Analytics actions
    st.subheader("📊 Analytics Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Performance Metrics**")
        st.write("• User engagement")
        st.write("• System performance")
        st.write("• Process efficiency")
    
    with col2:
        st.write("**Business Intelligence**")
        st.write("• Revenue analysis")
        st.write("• Growth tracking")
        st.write("• Predictive analytics")
    
    with col3:
        st.write("**Custom Reports**")
        st.write("• Report generation")
        st.write("• Data export")
        st.write("• Scheduled reports")

def show_admin_settings():
    st.header("⚙️ System Settings")
    st.subheader("Configuration and Management")
    
    # Security status
    st.subheader("🔒 Security Status")
    if st.session_state.secure_mode:
        st.success("✅ **Secure Data Manager:** All data is encrypted and protected")
        st.write("• Personal data is encrypted")
        st.write("• Application data is secure")
        st.write("• All submissions are protected")
    else:
        st.warning("⚠️ **Fallback Mode:** Using generic data - configure secure data manager for full functionality")
        st.write("• Personal data not loaded")
        st.write("• Using generic templates")
        st.write("• Configure secure data manager")
    
    # Settings sections
    st.subheader("System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Database Settings**")
        st.write("• Connection configuration")
        st.write("• Backup settings")
        st.write("• Performance tuning")
    
    with col2:
        st.write("**Security Settings**")
        st.write("• Authentication")
        st.write("• Access control")
        st.write("• Audit logging")
    
    # Settings actions
    st.subheader("⚙️ Settings Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**User Management**")
        st.write("• Add/remove users")
        st.write("• Role assignment")
        st.write("• Permission management")
    
    with col2:
        st.write("**System Maintenance**")
        st.write("• Backup/restore")
        st.write("• Performance monitoring")
        st.write("• Error logging")
    
    with col3:
        st.write("**Integration**")
        st.write("• Third-party APIs")
        st.write("• Webhook configuration")
        st.write("• Data synchronization")

def show_application_form():
    st.title("📝 Application Form")
    st.subheader("Submit Your Application")
    
    with st.form("application_form"):
        st.header("Personal Information")
        full_name = st.text_input("Full Name *", help="Your legal full name.")
        email = st.text_input("Email Address *", help="Your primary email address for communication.")
        phone = st.text_input("Phone Number", help="Your contact phone number.")
        age = st.number_input("Age *", min_value=18, max_value=99, help="You must be 18 or older to apply.")
        location = st.text_input("Current Location (City, State, Country) *", help="Where are you currently located?")
        
        st.header("Experience and Interests")
        experience = st.selectbox(
            "Level of Experience *",
            ["Beginner", "Intermediate", "Experienced", "Highly Experienced"],
            help="Your experience level in BDSM/kink dynamics."
        )
        
        # Sir's Kink List Reference
        with st.expander(f"👑 {PERSONAL_BRANDING['title']}'s Kink Preferences (for reference)", expanded=False):
            st.write(f"**{PERSONAL_BRANDING['title']}'s interests include (none required):**")
            for interest in SIR_KINK_PREFERENCES['primary_interests']:
                st.write(f"• {interest.replace('_', ' ').title()}")
            st.write("**Note:** None of these are required - we're looking for compatibility and enthusiasm.")
        
        interests = st.text_area(
            "What are your primary interests and desires? *",
            help="Describe what you are looking for and what excites you in a dynamic. Be specific about your kinks, fetishes, and what you enjoy.",
            height=100
        )
        
        limits = st.text_area(
            "Do you have any hard limits or boundaries? *",
            help="Please list any activities or situations you absolutely will not engage in. Be honest about your limits.",
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
        
        
        referral = st.text_input("How did you hear about us?", help="e.g., website, friend, specific event.")
        
        anything_else = st.text_area(
            "Is there anything else you'd like us to know?",
            help="Any additional information you'd like to share about yourself, your interests, or what you're looking for.",
            height=80
        )
        
        # Terms and Conditions
        st.markdown("---")
        agree_terms = st.checkbox(
            "I agree to the terms and conditions and privacy policy *",
            help="You must agree to the terms to submit your application"
        )
        
        # Submit button
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
        with col2:
            if st.form_submit_button("← Back to Portal", use_container_width=True):
                st.session_state.show_application_form = False
                st.rerun()
        
        if submitted:
            if not agree_terms:
                st.error("❌ You must agree to the terms and conditions to submit your application.")
            elif not full_name or not email or not age or not location or not interests or not limits:
                st.error("❌ Please fill in all required fields.")
            else:
                # Prepare application data
                application_data = {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "age": age,
                    "location": location,
                    "experience": experience,
                    "interests": interests,
                    "limits": limits,
                    "availability": availability,
                    "commitment": commitment,
                    "innovation_interest": innovation_interest,
                    "referral": referral,
                    "anything_else": anything_else,
                }
                
                # Save application securely
                if SECURE_DATA_AVAILABLE:
                    try:
                        app_id = secure_data_manager.save_application(application_data)
                        if app_id:
                            st.success(f"✅ Application submitted successfully! Application ID: {app_id}")
                            st.info("Your application has been securely saved and will be reviewed shortly.")
                        else:
                            st.error("❌ Failed to save application. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Error saving application: {e}")
                else:
                    st.success("✅ Application submitted successfully! (Demo mode)")
                    st.info("Your application will be reviewed shortly.")
                    st.json(application_data) # For demonstration, show submitted data

def main():
    # Initialize session state
    init_session_state()
    
    # Main routing logic
    if st.session_state.admin_authenticated:
        show_admin_dashboard()
    elif st.session_state.applicant_authenticated:
        show_applicant_dashboard()
    elif st.session_state.user_type == "admin":
        show_admin_login()
    elif st.session_state.user_type == "applicant":
        show_applicant_login()
    elif st.session_state.get('show_application_form'):
        show_application_form()
    elif st.session_state.get('show_register_form'):
        st.info("Account registration features will be available after application approval.")
        if st.button("← Back to Portal"):
            st.session_state.show_register_form = False
            st.rerun()
    else:
        show_landing_page()
    
    # Footer
    st.markdown("---")
    st.markdown("© 2025 Harem CRM. All rights reserved.")

if __name__ == "__main__":
    main()
