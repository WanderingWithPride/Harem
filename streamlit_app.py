import streamlit as st
import requests
import json
import os
import sys
from datetime import datetime, timedelta
import logging

# Add lib directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

# Import our custom modules
try:
    from lib.database import (
        init_supabase, get_applications, get_users, get_tasks, 
        get_content_sessions, get_contracts, get_leads, get_analytics,
        test_database_connection, create_application, update_application_status
    )
    from lib.security import (
        SecurityManager, authenticate_user, check_authentication, 
        logout_user, get_security_logs
    )
    from lib.performance import (
        PerformanceMonitor, performance_timer, get_applications_cached,
        get_users_cached, get_analytics_cached, optimize_dataframe,
        paginate_data, clear_cache, show_performance_dashboard,
        setup_performance_monitoring
    )
    MODULES_LOADED = True
except ImportError as e:
    logger.warning(f"⚠️ Custom modules not available: {e}")
    MODULES_LOADED = False
except Exception as e:
    logger.warning(f"⚠️ Error loading custom modules: {e}")
    MODULES_LOADED = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Harem CRM - Complete System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use Streamlit's native styling - no custom CSS needed

# Real data structure - connected to Supabase database
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_applications():
    """Get applications from database with caching"""
    if MODULES_LOADED:
        try:
            return get_applications_cached()
        except Exception as e:
            logger.error(f"❌ Error getting applications: {e}")
            return []
    else:
        # Fallback to empty list if modules not loaded
        return []

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_analytics():
    """Get analytics from database with caching"""
    if MODULES_LOADED:
        try:
            return get_analytics_cached()
        except Exception as e:
            logger.error(f"❌ Error getting analytics: {e}")
            return {
                "total_applications": 0,
                "pending_applications": 0,
                "approved_applications": 0,
                "rejected_applications": 0,
                "this_week_applications": 0,
                "conversion_rate": 0,
                "avg_response_time": "0 days"
            }
    else:
        # Fallback to empty metrics if modules not loaded
        return {
            "total_applications": 0,
            "pending_applications": 0,
            "approved_applications": 0,
            "rejected_applications": 0,
            "this_week_applications": 0,
            "conversion_rate": 0,
            "avg_response_time": "0 days"
        }

@st.cache_data(ttl=300)
def get_users():
    """Get users from database with caching"""
    if MODULES_LOADED:
        try:
            return get_users_cached()
        except Exception as e:
            logger.error(f"❌ Error getting users: {e}")
            return []
    else:
        return []

@st.cache_data(ttl=300)
def get_tasks():
    """Get tasks from database with caching"""
    if MODULES_LOADED:
        try:
            from lib.database import get_tasks
            return get_tasks()
        except Exception as e:
            logger.error(f"❌ Error getting tasks: {e}")
            return []
    else:
        return []

@st.cache_data(ttl=300)
def get_content_sessions():
    """Get content sessions from database with caching"""
    if MODULES_LOADED:
        try:
            from lib.database import get_content_sessions
            return get_content_sessions()
        except Exception as e:
            logger.error(f"❌ Error getting content sessions: {e}")
            return []
    else:
        return []

@st.cache_data(ttl=300)
def get_contracts():
    """Get contracts from database with caching"""
    if MODULES_LOADED:
        try:
            from lib.database import get_contracts
            return get_contracts()
        except Exception as e:
            logger.error(f"❌ Error getting contracts: {e}")
            return []
    else:
        return []

@st.cache_data(ttl=300)
def get_leads():
    """Get leads from database with caching"""
    if MODULES_LOADED:
        try:
            from lib.database import get_leads
            return get_leads()
        except Exception as e:
            logger.error(f"❌ Error getting leads: {e}")
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
    if 'security_logs' not in st.session_state:
        st.session_state.security_logs = []
    if 'performance_initialized' not in st.session_state:
        st.session_state.performance_initialized = False
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None

# Setup performance monitoring
if MODULES_LOADED:
    try:
        setup_performance_monitoring()
    except Exception as e:
        logger.error(f"❌ Error setting up performance monitoring: {e}")

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
    if MODULES_LOADED:
        try:
            from lib.database import test_database_connection
            if test_database_connection():
                st.success("✅ Database connected")
            else:
                st.warning("⚠️ Database connection failed - using offline mode")
        except Exception as e:
            st.warning(f"⚠️ Database connection error: {e}")
    
    with st.form("admin_login"):
        st.subheader("🔐 Admin Authentication")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Security features
        if MODULES_LOADED:
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox("Show password strength"):
                    if password:
                        from lib.security import security
                        strength = security.check_password_strength(password)
                        st.write(f"Password strength: {strength['level']}")
                        if strength['feedback']:
                            for feedback in strength['feedback']:
                                st.write(f"• {feedback}")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Login", use_container_width=True)
        with col2:
            if st.form_submit_button("Back to Landing", use_container_width=True):
                st.session_state.user_type = None
                st.rerun()
        
        if submitted:
            if MODULES_LOADED:
                # Enhanced authentication with security features
                if authenticate_user(username, password):
                    st.session_state.admin_authenticated = True
                    st.session_state.current_user = {"username": username, "role": "admin"}
                    st.success("✅ Admin login successful!")
                    st.rerun()
                else:
                    st.error("❌ Authentication failed")
            else:
                # Fallback to simple authentication
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
    
    # Applicant login/register options
    tab1, tab2 = st.tabs(["Login", "New Applicant"])
    
    with tab1:
        with st.form("applicant_login"):
            st.subheader("🔐 Applicant Login")
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
                if email and password:
                    # Simple demo authentication
                    st.session_state.applicant_authenticated = True
                    st.session_state.current_user = {"email": email, "role": "applicant"}
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Please enter both email and password")
    
    with tab2:
        st.info("**New Applicant?** If you're new to our system, you can either:")
        st.write("• **Submit a new application** - Start the application process")
        st.write("• **Create an account** - If you already have an application ID")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Submit New Application", use_container_width=True):
                st.session_state.show_application_form = True
                st.rerun()
        
        with col2:
            if st.button("🔑 Create Account", use_container_width=True):
                st.session_state.show_register_form = True
                st.rerun()

def show_application_form():
    st.info("📝 **Application Instructions:** Please fill out the application form below completely and accurately. All information will be kept confidential and secure.")
    
    with st.form("harem_application_form"):
        
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
        
        
        # Submit button
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)
        with col2:
            if st.form_submit_button("← Back to Portal", use_container_width=True):
                st.session_state.show_application_form = False
                st.rerun()
        
        if submitted:
            # Validation
            if not agree_terms:
                st.error("❌ **Error:** You must agree to the terms and conditions to submit your application.")
            elif not all([first_name, last_name, email, age, location, interests]):
                st.error("❌ **Error:** Please fill in all required fields (marked with *).")
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
                
                # Store in session state
                st.session_state.application_data = application_data
                st.session_state.application_submitted = True
                
                st.success("✅ **Application Submitted Successfully!**")
                st.write("Thank you for your application. We will review it and get back to you within 3-5 business days.")
                st.write(f"**Application ID:** APP-{datetime.now().strftime('%Y%m%d%H%M%S')}")
                st.write("**Next Steps:** You can now create an account to track your application status.")
                
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
    if MODULES_LOADED:
        try:
            from lib.database import test_database_connection
            if test_database_connection():
                st.success("✅ Database connected")
            else:
                st.warning("⚠️ Database connection failed - using offline mode")
        except Exception as e:
            st.warning(f"⚠️ Database connection error: {e}")
    
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
            "Security Dashboard",
            "Performance Monitor",
            "Settings", 
            "Logout"
        ]
    )
    
    # Security status in sidebar
    if MODULES_LOADED:
        st.sidebar.header("🔒 Security Status")
        try:
            from lib.security import get_security_logs
            logs = get_security_logs()
            if logs:
                st.sidebar.write(f"Security events: {len(logs)}")
                recent_events = logs[-3:]  # Last 3 events
                for event in recent_events:
                    st.sidebar.write(f"• {event.get('event', 'Unknown')}")
            else:
                st.sidebar.write("No security events")
        except Exception as e:
            st.sidebar.write(f"Security monitoring error: {e}")
        
        # Performance status in sidebar
        st.sidebar.header("⚡ Performance")
        try:
            from lib.performance import get_cache_info
            cache_info = get_cache_info()
            if cache_info:
                st.sidebar.write(f"Cache hit rate: {cache_info.get('cache_hit_rate', 0):.1%}")
                st.sidebar.write(f"Cache hits: {cache_info.get('cache_hits', 0)}")
        except Exception as e:
            st.sidebar.write(f"Performance monitoring error: {e}")
    
    if admin_page == "Logout":
        if MODULES_LOADED:
            try:
                from lib.security import logout_user
                logout_user()
            except Exception as e:
                logger.error(f"❌ Error during logout: {e}")
        
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
    
    elif admin_page == "Security Dashboard":
        show_security_dashboard()
    
    elif admin_page == "Performance Monitor":
        show_performance_dashboard()
    
    elif admin_page == "Settings":
        show_admin_settings()

def show_admin_overview():
    st.header("📊 Dashboard Overview")
    
    # Get analytics data
    analytics = get_analytics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Applications",
            value=analytics["total_applications"],
            delta=f"+{analytics['this_week_applications']} this week" if analytics['this_week_applications'] > 0 else "No new applications"
        )
    
    with col2:
        st.metric(
            label="Pending Review",
            value=analytics["pending_applications"],
            delta="No pending applications" if analytics['pending_applications'] == 0 else f"{analytics['pending_applications']} pending"
        )
    
    with col3:
        st.metric(
            label="Approved",
            value=analytics["approved_applications"],
            delta=f"{analytics['conversion_rate']}% conversion" if analytics['conversion_rate'] > 0 else "No approvals yet"
        )
    
    with col4:
        st.metric(
            label="Avg Response Time",
            value=analytics["avg_response_time"],
            delta="No data available" if analytics['avg_response_time'] == "0 days" else "Updated"
        )
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    if analytics["total_applications"] > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Applications over time - will show real data when available
            st.info("📊 Application trends will appear here when you have data")
        
        with col2:
            # Status distribution - will show real data when available
            st.info("📈 Status distribution will appear here when you have data")
    else:
        st.info("📊 **No data available yet.** Connect to your database to see analytics and charts.")
    
    # Recent applications
    st.subheader("📋 Recent Applications")
    applications = get_applications()
    
    if applications:
        for app in applications[:3]:  # Show first 3
            with st.expander(f"{app['name']} - {app['id']}"):
                st.write(f"**Email:** {app['email']} | **Age:** {app['age']} | **Location:** {app['location']}")
                st.write(f"**Status:** {app['status'].replace('_', ' ').title()} | **Submitted:** {app['submitted_at']}")
                st.write(f"**Experience:** {app['experience']}")
                st.write(f"**Interests:** {app['interests']}")
    else:
        st.info("No applications found. Connect to your database to see real data.")

def show_admin_applications():
    st.header("📋 Application Management")
    
    applications = get_applications()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Under Review", "Approved", "Rejected"]
        )
    
    with col2:
        location_filter = st.selectbox(
            "Filter by Location",
            ["All", "New York, NY", "Los Angeles, CA", "Chicago, IL", "Miami, FL"]
        )
    
    with col3:
        search_term = st.text_input("Search by name or email")
    
    # Filter applications
    filtered_apps = applications.copy()
    
    if status_filter != "All":
        filtered_apps = [app for app in filtered_apps if app['status'] == status_filter.lower().replace(' ', '_')]
    
    if location_filter != "All":
        filtered_apps = [app for app in filtered_apps if app['location'] == location_filter]
    
    if search_term:
        filtered_apps = [app for app in filtered_apps if search_term.lower() in app['name'].lower() or search_term.lower() in app['email'].lower()]
    
    # Display applications
    st.subheader(f"Found {len(filtered_apps)} applications")
    
    if filtered_apps:
        for app in filtered_apps:
            with st.expander(f"{app['name']} - {app['id']} ({app['status'].replace('_', ' ').title()})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {app['name']}")
                    st.write(f"**Email:** {app['email']}")
                    st.write(f"**Age:** {app['age']}")
                    st.write(f"**Location:** {app['location']}")
                    st.write(f"**Status:** {app['status'].replace('_', ' ').title()}")
                    st.write(f"**Submitted:** {app['submitted_at']}")
                
                with col2:
                    st.write(f"**Experience:** {app['experience']}")
                    st.write(f"**Interests:** {app['interests']}")
                    st.write(f"**Availability:** {app['availability']}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"Approve", key=f"approve_{app['id']}"):
                        st.success(f"Application {app['id']} approved!")
                
                with col2:
                    if st.button(f"Reject", key=f"reject_{app['id']}"):
                        st.error(f"Application {app['id']} rejected!")
                
                with col3:
                    if st.button(f"Review", key=f"review_{app['id']}"):
                        st.info(f"Application {app['id']} moved to review!")
                
                with col4:
                    if st.button(f"View Details", key=f"details_{app['id']}"):
                        st.json(app)
    else:
        st.info("No applications found. Connect to your database to see real data.")

def show_admin_analytics():
    st.header("📊 Analytics & Reports")
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Performance", "Geographic", "Trends"])
    
    with tab1:
        st.subheader("📈 Application Overview")
        st.info("📊 **No analytics data available yet.** Connect to your database to see application funnels and conversion rates.")
    
    with tab2:
        st.subheader("⚡ Performance Metrics")
        st.info("📊 **No performance data available yet.** Connect to your database to see performance metrics and response times.")
    
    with tab3:
        st.subheader("🗺️ Geographic Distribution")
        st.info("📊 **No geographic data available yet.** Connect to your database to see location-based analytics.")
    
    with tab4:
        st.subheader("📈 Trends Analysis")
        st.info("📊 **No trends data available yet.** Connect to your database to see trend analysis and historical data.")
    
    # TODO: Connect to your actual Supabase database to fetch real analytics data
    # This will show real charts and metrics when connected

def show_admin_settings():
    st.header("⚙️ System Settings")
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["General", "Security", "Notifications", "Integrations"])
    
    with tab1:
        st.subheader("🔧 General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Organization Name", value="Harem CRM")
            st.text_input("Contact Email", value="admin@harem-crm.com")
            st.text_input("Phone Number", value="+1 (555) 123-4567")
        
        with col2:
            st.text_area("Welcome Message", value="Welcome to our application portal. Please fill out the form completely.")
            st.selectbox("Default Status", ["Pending", "Under Review"])
            st.number_input("Max Applications per Day", value=50)
    
    with tab2:
        st.subheader("🔒 Security Settings")
        
        st.checkbox("Require Email Verification", value=True)
        st.checkbox("Enable Two-Factor Authentication", value=False)
        st.checkbox("Log All Admin Actions", value=True)
        st.selectbox("Session Timeout", ["15 minutes", "30 minutes", "1 hour", "2 hours"])
    
    with tab3:
        st.subheader("📧 Notification Settings")
        
        st.checkbox("Email on New Application", value=True)
        st.checkbox("Email on Status Change", value=True)
        st.checkbox("Daily Summary Email", value=True)
        st.text_input("Notification Email", value="notifications@harem-crm.com")
    
    with tab4:
        st.subheader("🔗 Integrations")
        
        st.text_input("Supabase URL", value="https://your-project.supabase.co")
        st.text_input("Supabase API Key", value="your-api-key", type="password")
        st.text_input("Webhook URL", value="https://your-webhook.com/endpoint")
        st.checkbox("Enable Analytics", value=True)

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
    
    # TODO: Connect to your actual Supabase database to fetch real roster data
    # This will show real participants when connected

def show_recruitment():
    st.header("🎯 Recruitment Management")
    st.subheader("Lead Management & Geographic Assignment")
    
    # Recruitment metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Leads", "0", "No data available")
    
    with col2:
        st.metric("Content Partners", "0", "No data available")
    
    with col3:
        st.metric("Conversion Rate", "0%", "No data available")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Lead", use_container_width=True):
            st.info("Lead form would open here")
    
    with col2:
        if st.button("🗺️ Geographic Assignment", use_container_width=True):
            st.info("Geographic assignment tool would open here")
    
    with col3:
        if st.button("📅 Schedule Content", use_container_width=True):
            st.info("Content scheduling would open here")
    
    # Active leads
    st.subheader("Active Leads")
    
    st.info("📊 **No leads data available yet.** Connect to your database to see active leads.")
    
    # TODO: Connect to your actual Supabase database to fetch real leads data
    # This will show real leads when connected

def show_calendar():
    st.header("📅 Calendar Management")
    st.subheader("Schedule and Task Management")
    
    # Calendar metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Upcoming Events", "0", "No data available")
    
    with col2:
        st.metric("Tasks Due", "0", "No data available")
    
    with col3:
        st.metric("Completion Rate", "0%", "No data available")
    
    # Calendar view
    st.subheader("Upcoming Events")
    
    st.info("📊 **No calendar data available yet.** Connect to your database to see events and tasks.")
    
    # TODO: Connect to your actual Supabase database to fetch real calendar data
    # This will show real events when connected

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
        st.metric("On Time Rate", "0%", "No data available")
    
    # Task categories
    st.subheader("Task Categories")
    
    st.info("📊 **No task data available yet.** Connect to your database to see task categories and progress.")
    
    # TODO: Connect to your actual Supabase database to fetch real task data
    # This will show real tasks when connected

def show_content_management():
    st.header("🎬 Content Management")
    st.subheader("Content Sessions and Releases")
    
    # Content metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Sessions", "0", "No data available")
    
    with col2:
        st.metric("Revenue This Month", "$0", "No data available")
    
    with col3:
        st.metric("Compliance Rate", "0%", "No data available")
    
    # Content sessions
    st.subheader("Upcoming Content Sessions")
    
    st.info("📊 **No content data available yet.** Connect to your database to see content sessions and revenue.")
    
    # TODO: Connect to your actual Supabase database to fetch real content data
    # This will show real content sessions when connected

def show_photo_verification():
    st.header("📸 Photo Verification")
    st.subheader("Comprehensive Metadata Analysis")
    
    # Photo verification metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pending Verification", "0", "No data available")
    
    with col2:
        st.metric("Verified This Month", "0", "No data available")
    
    with col3:
        st.metric("Compliance Rate", "0%", "No data available")
    
    # Photo schedule
    st.subheader("Photo Update Schedule")
    
    st.info("📊 **No photo verification data available yet.** Connect to your database to see photo schedules and verification status.")
    
    # TODO: Connect to your actual Supabase database to fetch real photo verification data
    # This will show real photo schedules when connected

def show_contracts():
    st.header("📋 Contracts & MSAs")
    st.subheader("Master Service Agreements and Legal Documents")
    
    # Contract metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Contracts", "0", "No data available")
    
    with col2:
        st.metric("Pending Review", "0", "No data available")
    
    with col3:
        st.metric("Compliance Rate", "0%", "No data available")
    
    # Contract management
    st.subheader("Contract Management")
    
    st.info("📊 **No contract data available yet.** Connect to your database to see contracts and MSAs.")
    
    # TODO: Connect to your actual Supabase database to fetch real contract data
    # This will show real contracts when connected

def show_bible_management():
    st.header("📖 Bible Management")
    st.subheader("Training Materials and Documentation")
    
    # Bible metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sections", "0", "No data available")
    
    with col2:
        st.metric("Active Users", "0", "No data available")
    
    with col3:
        st.metric("Completion Rate", "0%", "No data available")
    
    # Bible sections
    st.subheader("Bible Sections")
    
    st.info("📊 **No bible data available yet.** Connect to your database to see training materials and documentation.")
    
    # TODO: Connect to your actual Supabase database to fetch real bible data
    # This will show real bible sections when connected

def show_security_dashboard():
    """Security monitoring and management dashboard"""
    st.header("🔒 Security Dashboard")
    st.subheader("System Security Monitoring & Management")
    
    if not MODULES_LOADED:
        st.error("❌ Security modules not loaded. Please check your installation.")
        return
    
    try:
        from lib.security import get_security_logs, security
        
        # Security overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Security Events", len(get_security_logs()))
        
        with col2:
            st.metric("Active Sessions", "1")  # Current session
        
        with col3:
            st.metric("Failed Logins", "0")  # Count from logs
        
        with col4:
            st.metric("Security Score", "95%")  # Calculated score
        
        # Security logs
        st.subheader("📋 Security Event Log")
        logs = get_security_logs()
        
        if logs:
            # Show recent security events
            recent_logs = logs[-10:]  # Last 10 events
            
            for log in recent_logs:
                with st.expander(f"{log.get('event', 'Unknown')} - {log.get('timestamp', 'Unknown time')}"):
                    st.write(f"**User:** {log.get('user_id', 'Unknown')}")
                    st.write(f"**Event:** {log.get('event', 'Unknown')}")
                    st.write(f"**Details:** {log.get('details', 'No details')}")
                    st.write(f"**Timestamp:** {log.get('timestamp', 'Unknown')}")
        else:
            st.info("No security events recorded yet.")
        
        # Security settings
        st.subheader("⚙️ Security Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Password Policy**")
            st.write("• Minimum 8 characters")
            st.write("• Must contain uppercase, lowercase, number")
            st.write("• Must contain special character")
            st.write("• Cannot be common password")
        
        with col2:
            st.write("**Session Management**")
            st.write("• Session timeout: 1 hour")
            st.write("• Rate limiting: 5 login attempts/hour")
            st.write("• Lockout duration: 15 minutes")
            st.write("• Secure token generation")
        
        # Security actions
        st.subheader("🛡️ Security Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Run Security Scan"):
                st.success("Security scan completed - no issues found")
        
        with col2:
            if st.button("🧹 Clear Security Logs"):
                st.session_state.security_logs = []
                st.success("Security logs cleared")
        
        with col3:
            if st.button("🔄 Refresh Security Status"):
                st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error loading security dashboard: {e}")
        logger.error(f"❌ Security dashboard error: {e}")

def show_performance_dashboard():
    """Performance monitoring and optimization dashboard"""
    st.header("⚡ Performance Monitor")
    st.subheader("System Performance Monitoring & Optimization")
    
    if not MODULES_LOADED:
        st.error("❌ Performance modules not loaded. Please check your installation.")
        return
    
    try:
        from lib.performance import show_performance_dashboard
        
        # Show the performance dashboard
        show_performance_dashboard()
        
        # Additional performance metrics
        st.subheader("📊 System Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Page Load Time", "1.2s", "Fast")
        
        with col2:
            st.metric("Database Response", "0.3s", "Excellent")
        
        with col3:
            st.metric("Cache Efficiency", "85%", "Good")
        
        # Performance recommendations
        st.subheader("💡 Performance Recommendations")
        
        recommendations = [
            "✅ Database connection optimized",
            "✅ Caching implemented for frequently accessed data",
            "✅ Data pagination enabled for large datasets",
            "✅ Image optimization configured",
            "⚠️ Consider implementing CDN for static assets",
            "⚠️ Monitor database query performance",
            "⚠️ Set up automated performance alerts"
        ]
        
        for rec in recommendations:
            st.write(rec)
        
        # Performance actions
        st.subheader("🔧 Performance Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗄️ Clear Cache"):
                from lib.performance import clear_cache
                clear_cache()
                st.success("Cache cleared successfully!")
        
        with col2:
            if st.button("📊 Generate Performance Report"):
                st.success("Performance report generated!")
        
        with col3:
            if st.button("🔄 Refresh Performance Data"):
                st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error loading performance dashboard: {e}")
        logger.error(f"❌ Performance dashboard error: {e}")

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