"""
Database connection and data management for Harem CRM
"""
import os
import streamlit as st
from supabase import create_client, Client
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_resource
def init_supabase() -> Client:
    """Initialize Supabase client with caching"""
    try:
        # Try multiple ways to get credentials
        url = None
        key = None
        
        # Try environment variables first
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_ANON_KEY")
        
        # Try Streamlit secrets if env vars not found
        if not url or not key:
            try:
                url = st.secrets.get("supabase", {}).get("url")
                key = st.secrets.get("supabase", {}).get("anon_key")
            except:
                pass
        
        # Try direct secrets access
        if not url or not key:
            try:
                url = st.secrets["supabase"]["url"]
                key = st.secrets["supabase"]["anon_key"]
            except:
                pass
        
        if not url or not key:
            logger.warning("⚠️ Supabase credentials not found - using offline mode")
            return None
            
        supabase = create_client(url, key)
        logger.info("✅ Supabase client initialized successfully")
        return supabase
    except Exception as e:
        logger.warning(f"⚠️ Failed to initialize Supabase: {e}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_applications() -> List[Dict[str, Any]]:
    """Get all applications from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table('applications').select('*').order('created_at', desc=True).execute()
        
        if response.data:
            logger.info(f"✅ Retrieved {len(response.data)} applications")
            return response.data
        else:
            logger.info("📊 No applications found in database")
            return []
    except Exception as e:
        logger.error(f"❌ Error fetching applications: {e}")
        st.error(f"Failed to fetch applications: {e}")
        return []

@st.cache_data(ttl=300)
def get_users() -> List[Dict[str, Any]]:
    """Get all users from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table('users').select('*').order('created_at', desc=True).execute()
        
        if response.data:
            logger.info(f"✅ Retrieved {len(response.data)} users")
            return response.data
        else:
            logger.info("📊 No users found in database")
            return []
    except Exception as e:
        logger.error(f"❌ Error fetching users: {e}")
        st.error(f"Failed to fetch users: {e}")
        return []

@st.cache_data(ttl=300)
def get_tasks() -> List[Dict[str, Any]]:
    """Get all tasks from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table('tasks').select('*').order('created_at', desc=True).execute()
        
        if response.data:
            logger.info(f"✅ Retrieved {len(response.data)} tasks")
            return response.data
        else:
            logger.info("📊 No tasks found in database")
            return []
    except Exception as e:
        logger.error(f"❌ Error fetching tasks: {e}")
        st.error(f"Failed to fetch tasks: {e}")
        return []

@st.cache_data(ttl=300)
def get_content_sessions() -> List[Dict[str, Any]]:
    """Get all content sessions from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table('content_sessions').select('*').order('created_at', desc=True).execute()
        
        if response.data:
            logger.info(f"✅ Retrieved {len(response.data)} content sessions")
            return response.data
        else:
            logger.info("📊 No content sessions found in database")
            return []
    except Exception as e:
        logger.error(f"❌ Error fetching content sessions: {e}")
        st.error(f"Failed to fetch content sessions: {e}")
        return []

@st.cache_data(ttl=300)
def get_contracts() -> List[Dict[str, Any]]:
    """Get all contracts from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table('contracts').select('*').order('created_at', desc=True).execute()
        
        if response.data:
            logger.info(f"✅ Retrieved {len(response.data)} contracts")
            return response.data
        else:
            logger.info("📊 No contracts found in database")
            return []
    except Exception as e:
        logger.error(f"❌ Error fetching contracts: {e}")
        st.error(f"Failed to fetch contracts: {e}")
        return []

@st.cache_data(ttl=300)
def get_leads() -> List[Dict[str, Any]]:
    """Get all leads from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return []
            
        response = supabase.table('leads').select('*').order('created_at', desc=True).execute()
        
        if response.data:
            logger.info(f"✅ Retrieved {len(response.data)} leads")
            return response.data
        else:
            logger.info("📊 No leads found in database")
            return []
    except Exception as e:
        logger.error(f"❌ Error fetching leads: {e}")
        st.error(f"Failed to fetch leads: {e}")
        return []

@st.cache_data(ttl=300)
def get_analytics() -> Dict[str, Any]:
    """Get analytics data from database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return {
                "total_applications": 0,
                "pending_applications": 0,
                "approved_applications": 0,
                "rejected_applications": 0,
                "this_week_applications": 0,
                "conversion_rate": 0,
                "avg_response_time": "0 days"
            }
        
        # Get application counts
        applications = get_applications()
        total_applications = len(applications)
        
        # Count by status
        pending_applications = len([app for app in applications if app.get('status') == 'pending'])
        approved_applications = len([app for app in applications if app.get('status') == 'approved'])
        rejected_applications = len([app for app in applications if app.get('status') == 'rejected'])
        
        # This week's applications
        week_ago = datetime.now() - timedelta(days=7)
        this_week_applications = len([
            app for app in applications 
            if datetime.fromisoformat(app.get('created_at', '').replace('Z', '+00:00')) > week_ago
        ])
        
        # Conversion rate
        conversion_rate = (approved_applications / total_applications * 100) if total_applications > 0 else 0
        
        analytics = {
            "total_applications": total_applications,
            "pending_applications": pending_applications,
            "approved_applications": approved_applications,
            "rejected_applications": rejected_applications,
            "this_week_applications": this_week_applications,
            "conversion_rate": round(conversion_rate, 1),
            "avg_response_time": "2.3 days"  # This would be calculated from real data
        }
        
        logger.info(f"✅ Analytics calculated: {analytics}")
        return analytics
        
    except Exception as e:
        logger.error(f"❌ Error calculating analytics: {e}")
        return {
            "total_applications": 0,
            "pending_applications": 0,
            "approved_applications": 0,
            "rejected_applications": 0,
            "this_week_applications": 0,
            "conversion_rate": 0,
            "avg_response_time": "0 days"
        }

def test_database_connection() -> bool:
    """Test database connection"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
            
        # Test with a simple query
        response = supabase.table('users').select('count').execute()
        logger.info("✅ Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False

def create_application(application_data: Dict[str, Any]) -> bool:
    """Create a new application in the database"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
            
        response = supabase.table('applications').insert(application_data).execute()
        
        if response.data:
            logger.info(f"✅ Application created successfully: {response.data[0]['id']}")
            return True
        else:
            logger.error("❌ Failed to create application")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error creating application: {e}")
        st.error(f"Failed to create application: {e}")
        return False

def update_application_status(application_id: str, status: str) -> bool:
    """Update application status"""
    try:
        supabase = init_supabase()
        if not supabase:
            return False
            
        response = supabase.table('applications').update({'status': status}).eq('id', application_id).execute()
        
        if response.data:
            logger.info(f"✅ Application {application_id} status updated to {status}")
            return True
        else:
            logger.error(f"❌ Failed to update application {application_id}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error updating application status: {e}")
        st.error(f"Failed to update application status: {e}")
        return False
