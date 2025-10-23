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

# Custom CSS for complete system
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
    .admin-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
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
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    .application-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-pending { color: #ffc107; font-weight: bold; }
    .status-approved { color: #28a745; font-weight: bold; }
    .status-rejected { color: #dc3545; font-weight: bold; }
    .status-review { color: #17a2b8; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sample data for demo
@st.cache_data
def get_sample_applications():
    return [
        {
            "id": "APP-001",
            "name": "Sarah Johnson",
            "email": "sarah.j@email.com",
            "age": 25,
            "location": "New York, NY",
            "status": "pending",
            "submitted_at": "2025-01-15 10:30:00",
            "experience": "2 years in service industry",
            "interests": "Domestic services, content creation",
            "availability": "Weekends and evenings"
        },
        {
            "id": "APP-002", 
            "name": "Emma Davis",
            "email": "emma.d@email.com",
            "age": 28,
            "location": "Los Angeles, CA",
            "status": "under_review",
            "submitted_at": "2025-01-14 14:20:00",
            "experience": "5 years in hospitality",
            "interests": "Administrative work, content creation",
            "availability": "Full-time"
        },
        {
            "id": "APP-003",
            "name": "Jessica Wilson",
            "email": "jessica.w@email.com", 
            "age": 23,
            "location": "Chicago, IL",
            "status": "approved",
            "submitted_at": "2025-01-13 09:15:00",
            "experience": "3 years in customer service",
            "interests": "Technical support, content creation",
            "availability": "Flexible schedule"
        }
    ]

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

# Admin authentication
def check_admin_auth():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    return st.session_state.admin_authenticated

def admin_login():
    st.markdown("""
    <div class="admin-header">
        <h1>👑 Harem CRM Admin Dashboard</h1>
        <p>Owner/Admin Access Required</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login"):
        st.subheader("🔐 Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # Simple authentication (replace with secure auth in production)
            if username == "admin" and password == "harem2025":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")

def show_application_form():
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
                
                # Store in session state
                st.session_state.application_data = application_data
                st.session_state.application_submitted = True
                
                st.markdown("""
                <div class="success-message">
                    <h3>✅ Application Submitted Successfully!</h3>
                    <p>Thank you for your application. We will review it and get back to you within 3-5 business days.</p>
                    <p><strong>Application ID:</strong> {}</p>
                </div>
                """.format(f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}"), unsafe_allow_html=True)

def show_application_status():
    st.header("🔍 Check Application Status")
    
    st.markdown("""
    <div class="info-box">
        <p>Enter your email address to check the status of your application.</p>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Email Address", help="Enter the email address you used for your application")
    
    if st.button("Check Status", use_container_width=True):
        if email:
            # Mock status check
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

def show_admin_dashboard():
    st.markdown("""
    <div class="admin-header">
        <h1>👑 Harem CRM Admin Dashboard</h1>
        <p>Complete Application Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Admin Navigation")
    admin_page = st.sidebar.selectbox(
        "Choose a section:",
        ["Dashboard Overview", "Applications", "Analytics", "Settings", "Logout"]
    )
    
    if admin_page == "Logout":
        st.session_state.admin_authenticated = False
        st.rerun()
    
    elif admin_page == "Dashboard Overview":
        show_admin_overview()
    
    elif admin_page == "Applications":
        show_admin_applications()
    
    elif admin_page == "Analytics":
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
    applications = get_sample_applications()
    
    for app in applications[:3]:  # Show first 3
        with st.container():
            st.markdown(f"""
            <div class="application-card">
                <h4>{app['name']} - {app['id']}</h4>
                <p><strong>Email:</strong> {app['email']} | <strong>Age:</strong> {app['age']} | <strong>Location:</strong> {app['location']}</p>
                <p><strong>Status:</strong> <span class="status-{app['status']}">{app['status'].replace('_', ' ').title()}</span> | <strong>Submitted:</strong> {app['submitted_at']}</p>
                <p><strong>Experience:</strong> {app['experience']}</p>
                <p><strong>Interests:</strong> {app['interests']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_admin_applications():
    st.header("📋 Application Management")
    
    applications = get_sample_applications()
    
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

def show_about():
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

def show_contact():
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

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ Harem CRM - Complete System</h1>
        <p>Professional Application Management & Admin Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Check if user is admin
    if check_admin_auth():
        # Admin is logged in
        st.sidebar.success("👑 Admin Access")
        if st.sidebar.button("Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()
        
        # Admin navigation
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["Admin Dashboard", "Public Application Form", "Application Status", "About", "Contact"]
        )
    else:
        # Public user
        page = st.sidebar.selectbox(
            "Choose a page:",
            ["Application Form", "Application Status", "About", "Contact", "Admin Login"]
        )
    
    # Route to appropriate page
    if page == "Admin Login":
        admin_login()
    elif page == "Admin Dashboard":
        show_admin_dashboard()
    elif page == "Public Application Form":
        show_application_form()
    elif page == "Application Form":
        show_application_form()
    elif page == "Application Status":
        show_application_status()
    elif page == "About":
        show_about()
    elif page == "Contact":
        show_contact()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>© 2025 Harem CRM. All rights reserved. | <a href="/privacy">Privacy Policy</a> | <a href="/terms">Terms of Service</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
