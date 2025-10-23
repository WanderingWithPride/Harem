import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Harem CRM - Admin Dashboard",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for admin dashboard
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
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

# Admin authentication (simple for demo)
def check_admin_auth():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
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
        return False
    
    return True

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
        },
        {
            "id": "APP-004",
            "name": "Ashley Brown",
            "email": "ashley.b@email.com",
            "age": 26,
            "location": "Miami, FL", 
            "status": "rejected",
            "submitted_at": "2025-01-12 16:45:00",
            "experience": "1 year in retail",
            "interests": "Domestic services only",
            "availability": "Part-time only"
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

def main():
    if not check_admin_auth():
        return
    
    # Main header
    st.markdown("""
    <div class="admin-header">
        <h1>👑 Harem CRM Admin Dashboard</h1>
        <p>Complete Application Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Dashboard Overview", "Applications", "Analytics", "Settings", "Logout"]
    )
    
    if page == "Logout":
        st.session_state.admin_authenticated = False
        st.rerun()
    
    elif page == "Dashboard Overview":
        show_dashboard_overview()
    
    elif page == "Applications":
        show_applications_management()
    
    elif page == "Analytics":
        show_analytics()
    
    elif page == "Settings":
        show_settings()

def show_dashboard_overview():
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

def show_applications_management():
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

def show_analytics():
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

def show_settings():
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

if __name__ == "__main__":
    main()
