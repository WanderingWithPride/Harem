import streamlit as st
import requests
import json
import os
from datetime import datetime
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

# Real data structure - will connect to your actual CRM database
@st.cache_data
def get_applications():
    # TODO: Connect to your actual Supabase database
    # For now, return empty list - will be populated from real data
    return []

@st.cache_data
def get_sample_analytics():
    return {
        "total_applications": 47,
        "pending_applications": 12,
        "approved_applications": 28,
        "rejected_applications": 7,
        "this_week_applications": 8,
        "conversion_rate": 59.6,
        "avg_response_time": "2.3 days"
    }

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
    analytics = get_sample_analytics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Applications",
            value=analytics["total_applications"],
            delta=f"+{analytics['this_week_applications']} this week"
        )
    
    with col2:
        st.metric(
            label="Pending Review",
            value=analytics["pending_applications"],
            delta="12 new today"
        )
    
    with col3:
        st.metric(
            label="Approved",
            value=analytics["approved_applications"],
            delta=f"{analytics['conversion_rate']}% conversion"
        )
    
    with col4:
        st.metric(
            label="Avg Response Time",
            value=analytics["avg_response_time"],
            delta="-0.5 days"
        )
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Applications over time
        dates = pd.date_range(start='2025-01-01', end='2025-01-15', freq='D')
        applications_data = [2, 3, 1, 4, 2, 3, 5, 2, 1, 3, 4, 2, 3, 1, 2]
        
        fig = px.line(
            x=dates, 
            y=applications_data,
            title="Applications Over Time",
            labels={'x': 'Date', 'y': 'Applications'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Status distribution
        status_data = {
            'Status': ['Pending', 'Under Review', 'Approved', 'Rejected'],
            'Count': [12, 8, 28, 7]
        }
        
        fig = px.pie(
            values=status_data['Count'],
            names=status_data['Status'],
            title="Application Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
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
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Application funnel
            funnel_data = {
                'Stage': ['Applications', 'Under Review', 'Approved', 'Active'],
                'Count': [47, 20, 28, 15]
            }
            
            fig = px.funnel(
                x=funnel_data['Count'],
                y=funnel_data['Stage'],
                title="Application Funnel"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Conversion rates
            conversion_data = {
                'Metric': ['Application to Review', 'Review to Approval', 'Approval to Active'],
                'Rate': [42.6, 70.0, 53.6]
            }
            
            fig = px.bar(
                x=conversion_data['Metric'],
                y=conversion_data['Rate'],
                title="Conversion Rates (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("⚡ Performance Metrics")
        
        # Performance metrics
        metrics_data = {
            'Metric': ['Avg Response Time', 'Review Time', 'Approval Time', 'Onboarding Time'],
            'Days': [2.3, 1.5, 0.8, 3.2]
        }
        
        fig = px.bar(
            x=metrics_data['Metric'],
            y=metrics_data['Days'],
            title="Performance Metrics (Days)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🗺️ Geographic Distribution")
        
        # Geographic data
        geo_data = {
            'Location': ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Other'],
            'Applications': [12, 8, 6, 4, 17]
        }
        
        fig = px.pie(
            values=geo_data['Applications'],
            names=geo_data['Location'],
            title="Applications by Location"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("📈 Trends Analysis")
        
        # Weekly trends
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        applications = [8, 12, 15, 12]
        approvals = [5, 8, 10, 7]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks, y=applications, name='Applications', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=weeks, y=approvals, name='Approvals', line=dict(color='green')))
        
        fig.update_layout(title="Weekly Trends", xaxis_title="Week", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

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
        st.metric("Total Active", "12", "+2 this month")
    
    with col2:
        st.metric("New This Month", "3", "+1 from last month")
    
    with col3:
        st.metric("Compliance Rate", "95%", "+2% improvement")
    
    # Roster list
    st.subheader("Active Roster")
    
    # Sample roster data
    roster_data = [
        {"name": "Sarah Johnson", "status": "Active", "last_activity": "2025-01-15", "compliance": "Complete"},
        {"name": "Emma Davis", "status": "Active", "last_activity": "2025-01-14", "compliance": "Pending"},
        {"name": "Jessica Wilson", "status": "On Leave", "last_activity": "2025-01-10", "compliance": "Complete"},
    ]
    
    for member in roster_data:
        with st.expander(f"{member['name']} - {member['status']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Status:** {member['status']}")
                st.write(f"**Last Activity:** {member['last_activity']}")
            with col2:
                st.write(f"**Compliance:** {member['compliance']}")
                if st.button(f"View Profile", key=f"profile_{member['name']}"):
                    st.info("Profile view would open here")

def show_recruitment():
    st.header("🎯 Recruitment Management")
    st.subheader("Lead Management & Geographic Assignment")
    
    # Recruitment metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Leads", "8", "+3 this week")
    
    with col2:
        st.metric("Content Partners", "5", "+1 this month")
    
    with col3:
        st.metric("Conversion Rate", "62%", "+5% improvement")
    
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
    leads_data = [
        {"name": "Alex Thompson", "location": "New York", "status": "Contacted", "priority": "High"},
        {"name": "Maria Garcia", "location": "Los Angeles", "status": "Initial Contact", "priority": "Medium"},
        {"name": "Jordan Smith", "location": "Chicago", "status": "Follow-up", "priority": "High"},
    ]
    
    for lead in leads_data:
        with st.expander(f"{lead['name']} - {lead['location']} ({lead['status']})"):
            st.write(f"**Location:** {lead['location']}")
            st.write(f"**Status:** {lead['status']}")
            st.write(f"**Priority:** {lead['priority']}")

def show_calendar():
    st.header("📅 Calendar Management")
    st.subheader("Schedule and Task Management")
    
    # Calendar metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Upcoming Events", "12", "+3 this week")
    
    with col2:
        st.metric("Tasks Due", "5", "-2 from yesterday")
    
    with col3:
        st.metric("Completion Rate", "87%", "+3% improvement")
    
    # Calendar view
    st.subheader("Upcoming Events")
    
    # Sample calendar data
    events_data = [
        {"title": "Content Session - Sarah", "date": "2025-01-16", "time": "2:00 PM", "type": "Content"},
        {"title": "Photo Verification - Emma", "date": "2025-01-17", "time": "10:00 AM", "type": "Verification"},
        {"title": "Contract Review", "date": "2025-01-18", "time": "3:00 PM", "type": "Administrative"},
    ]
    
    for event in events_data:
        with st.container():
            st.write(f"**{event['title']}**")
            st.write(f"📅 {event['date']} at {event['time']} | Type: {event['type']}")

def show_tasks():
    st.header("✅ Task Management")
    st.subheader("Service Tasks and Assignments")
    
    # Task metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Tasks", "15", "+3 this week")
    
    with col2:
        st.metric("Completed Today", "8", "+2 from yesterday")
    
    with col3:
        st.metric("On Time Rate", "92%", "+4% improvement")
    
    # Task categories
    st.subheader("Task Categories")
    
    task_categories = [
        {"name": "Domestic Services", "count": 5, "completed": 3},
        {"name": "Administrative", "count": 4, "completed": 4},
        {"name": "Content Creation", "count": 3, "completed": 1},
        {"name": "Technical Support", "count": 3, "completed": 0},
    ]
    
    for category in task_categories:
        progress = category['completed'] / category['count'] if category['count'] > 0 else 0
        st.write(f"**{category['name']}:** {category['completed']}/{category['count']} completed")
        st.progress(progress)

def show_content_management():
    st.header("🎬 Content Management")
    st.subheader("Content Sessions and Releases")
    
    # Content metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Sessions", "4", "+1 this week")
    
    with col2:
        st.metric("Revenue This Month", "$2,400", "+15% growth")
    
    with col3:
        st.metric("Compliance Rate", "95%", "+2% improvement")
    
    # Content sessions
    st.subheader("Upcoming Content Sessions")
    
    sessions_data = [
        {"title": "Solo Content Session", "date": "2025-01-16", "participants": 1, "status": "Scheduled"},
        {"title": "Partnered Content Session", "date": "2025-01-18", "participants": 2, "status": "Pending Consent"},
        {"title": "Group Content Session", "date": "2025-01-20", "participants": 3, "status": "Confirmed"},
    ]
    
    for session in sessions_data:
        with st.expander(f"{session['title']} - {session['date']}"):
            st.write(f"**Participants:** {session['participants']}")
            st.write(f"**Status:** {session['status']}")

def show_photo_verification():
    st.header("📸 Photo Verification")
    st.subheader("Comprehensive Metadata Analysis")
    
    # Photo verification metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Pending Verification", "3", "+1 this week")
    
    with col2:
        st.metric("Verified This Month", "12", "+2 from last month")
    
    with col3:
        st.metric("Compliance Rate", "98%", "+1% improvement")
    
    # Photo schedule
    st.subheader("Photo Update Schedule")
    
    schedule_data = [
        {"name": "Sarah Johnson", "last_update": "2025-01-01", "next_due": "2025-07-01", "status": "Current"},
        {"name": "Emma Davis", "last_update": "2024-12-15", "next_due": "2025-06-15", "status": "Current"},
        {"name": "Jessica Wilson", "last_update": "2024-11-20", "next_due": "2025-05-20", "status": "Due Soon"},
    ]
    
    for item in schedule_data:
        with st.expander(f"{item['name']} - {item['status']}"):
            st.write(f"**Last Update:** {item['last_update']}")
            st.write(f"**Next Due:** {item['next_due']}")
            st.write(f"**Status:** {item['status']}")

def show_contracts():
    st.header("📋 Contracts & MSAs")
    st.subheader("Master Service Agreements and Legal Documents")
    
    # Contract metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Contracts", "8", "+2 this month")
    
    with col2:
        st.metric("Pending Review", "3", "+1 this week")
    
    with col3:
        st.metric("Compliance Rate", "100%", "Perfect compliance")
    
    # Contract management
    st.subheader("Contract Management")
    
    contracts_data = [
        {"name": "Sarah Johnson", "type": "MSA", "status": "Active", "expires": "2025-12-31"},
        {"name": "Emma Davis", "type": "Content Release", "status": "Pending", "expires": "N/A"},
        {"name": "Jessica Wilson", "type": "MSA", "status": "Active", "expires": "2025-11-30"},
    ]
    
    for contract in contracts_data:
        with st.expander(f"{contract['name']} - {contract['type']} ({contract['status']})"):
            st.write(f"**Type:** {contract['type']}")
            st.write(f"**Status:** {contract['status']}")
            st.write(f"**Expires:** {contract['expires']}")

def show_bible_management():
    st.header("📖 Bible Management")
    st.subheader("Training Materials and Documentation")
    
    # Bible metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sections", "24", "+2 this month")
    
    with col2:
        st.metric("Active Users", "15", "+3 this week")
    
    with col3:
        st.metric("Completion Rate", "78%", "+5% improvement")
    
    # Bible sections
    st.subheader("Bible Sections")
    
    bible_sections = [
        {"title": "Introduction to Service", "status": "Published", "users": 15},
        {"title": "Domestic Service Guidelines", "status": "Published", "users": 12},
        {"title": "Content Creation Standards", "status": "Draft", "users": 0},
        {"title": "Safety Protocols", "status": "Published", "users": 14},
    ]
    
    for section in bible_sections:
        with st.expander(f"{section['title']} - {section['status']}"):
            st.write(f"**Status:** {section['status']}")
            st.write(f"**Active Users:** {section['users']}")

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