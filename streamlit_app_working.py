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

# Use Streamlit's native styling - no custom CSS needed

# Real data structure - will connect to your actual CRM database
@st.cache_data
def get_applications():
    """Get applications from database with caching"""
    # TODO: Connect to your actual Supabase database
    # For now, return empty list - will be populated from real data
    return []

@st.cache_data
def get_analytics():
    """Get analytics from database with caching"""
    # TODO: Connect to your actual Supabase database
    # For now, return empty metrics - will be populated from real data
    return {
        "total_applications": 0,
        "pending_applications": 0,
        "approved_applications": 0,
        "rejected_applications": 0,
        "this_week_applications": 0,
        "conversion_rate": 0,
        "avg_response_time": "0 days"
    }

@st.cache_data
def get_users():
    """Get users from database with caching"""
    # TODO: Connect to your actual Supabase database
    return []

@st.cache_data
def get_tasks():
    """Get tasks from database with caching"""
    # TODO: Connect to your actual Supabase database
    return []

@st.cache_data
def get_content_sessions():
    """Get content sessions from database with caching"""
    # TODO: Connect to your actual Supabase database
    return []

@st.cache_data
def get_contracts():
    """Get contracts from database with caching"""
    # TODO: Connect to your actual Supabase database
    return []

@st.cache_data
def get_leads():
    """Get leads from database with caching"""
    # TODO: Connect to your actual Supabase database
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

def show_landing_page():
    st.title("🏛️ Harem CRM")
    st.subheader("Professional Application Management System")
    
    st.info("Welcome to Harem CRM! Please select your role to continue:")
    
    # Landing page with role selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👑 Admin Access")
        st.write("Manage applications, view analytics, and control the system")
        st.write("**Features:**")
        st.write("• View all applications")
        st.write("• Approve/reject candidates") 
        st.write("• Analytics and reporting")
        st.write("• System settings")
        
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.user_type = "admin"
            st.rerun()
    
    with col2:
        st.subheader("📝 Applicant Portal")
        st.write("Submit applications, check status, and manage your profile")
        st.write("**Features:**")
        st.write("• Submit new applications")
        st.write("• Check application status")
        st.write("• Update your profile")
        st.write("• View your progress")
        
        if st.button("📋 Applicant Portal", use_container_width=True):
            st.session_state.user_type = "applicant"
            st.rerun()

def show_admin_login():
    st.title("👑 Admin Login")
    st.subheader("Owner/Admin Access Required")
    
    # Database connection status
    st.info("💡 **Database Connection:** Ready to connect to Supabase when configured")
    
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
    st.title("👑 Harem CRM - Admin Dashboard")
    st.subheader(f"Welcome back, {st.session_state.current_user.get('username', 'Admin')}")
    
    # Database connection status
    st.success("✅ **System Status:** Ready for database connection")
    
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
    
    # Database connection info
    st.subheader("🔗 Database Connection")
    st.info("💡 **Ready to connect:** Configure Supabase credentials in Streamlit secrets to enable real-time data")
    
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
        df = pd.DataFrame(applications)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("📊 **No applications data available yet.** Connect to your database to see real applications.")
    
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

def show_roster_management():
    st.header("👥 Roster Management")
    st.subheader("Active Participants")
    
    # Roster management features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Active", "0", "No data available")
    
    with col2:
        st.metric("New This Month", "0", "No data available")
    
    with col3:
        st.metric("Compliance Rate", "0%", "No data available")
    
    # Roster list
    st.subheader("Active Roster")
    
    st.info("📊 **No roster data available yet.** Connect to your database to see active participants.")
    
    # Roster actions
    st.subheader("👥 Roster Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Profile Management**")
        st.write("• View detailed profiles")
        st.write("• Update user information")
        st.write("• Manage preferences")
    
    with col2:
        st.write("**Performance Tracking**")
        st.write("• Service logs")
        st.write("• Quality scores")
        st.write("• Compliance monitoring")
    
    with col3:
        st.write("**Communication**")
        st.write("• Send messages")
        st.write("• Schedule meetings")
        st.write("• Assign tasks")

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
        st.metric("Total Sections", "0", "No data available")
    
    with col2:
        st.metric("Active Version", "v1.0", "No data available")
    
    with col3:
        st.metric("Completion Rate", "0%", "No data available")
    
    # Bible sections
    st.subheader("Bible Sections")
    
    st.info("📊 **No bible data available yet.** Connect to your database to see training materials and documentation.")
    
    # Bible actions
    st.subheader("📖 Bible Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Content Management**")
        st.write("• Create sections")
        st.write("• Edit content")
        st.write("• Version control")
    
    with col2:
        st.write("**Access Control**")
        st.write("• Role-based access")
        st.write("• Visibility settings")
        st.write("• Permission management")
    
    with col3:
        st.write("**Analytics**")
        st.write("• Usage tracking")
        st.write("• Completion rates")
        st.write("• Performance metrics")

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
    
    # Database connection info
    st.subheader("🔗 Database Connection")
    st.info("💡 **Ready to connect:** Configure Supabase credentials in Streamlit secrets to enable real-time data")
    
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
        
        interests = st.text_area(
            "What are your primary interests and desires? *",
            help="Describe what you are looking for and what excites you in a dynamic.",
            height=100
        )
        
        limits = st.text_area(
            "Do you have any hard limits or boundaries? *",
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
        
        referral = st.text_input("How did you hear about us?", help="e.g., website, friend, specific event.")
        
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
                # In a real application, you would send this data to your backend API
                # For this example, we'll just display it.
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
                    "referral": referral,
                    "anything_else": anything_else,
                }
                
                st.success("✅ Application submitted successfully! We will review it shortly.")
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
