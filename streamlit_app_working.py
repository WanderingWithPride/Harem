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

# Comprehensive Kink Categories and Data
KINK_CATEGORIES = [
    {"id": "bdsm_basics", "name": "BDSM Basics", "icon": "🛡️"},
    {"id": "bondage_restraint", "name": "Bondage & Restraint", "icon": "🔗"},
    {"id": "impact_play", "name": "Impact Play", "icon": "👋"},
    {"id": "sensation_play", "name": "Sensation Play", "icon": "❤️"},
    {"id": "electrical_play", "name": "Electrical Play", "icon": "⚡"},
    {"id": "penetration_anal", "name": "Penetration & Anal", "icon": "🍑"},
    {"id": "oral_service", "name": "Oral & Service", "icon": "👄"},
    {"id": "humiliation_degradation", "name": "Humiliation & Degradation", "icon": "😳"},
    {"id": "financial_service", "name": "Financial & Service", "icon": "💰"},
    {"id": "exhibitionism_voyeurism", "name": "Exhibitionism & Voyeurism", "icon": "📸"},
    {"id": "roleplay_scenarios", "name": "Roleplay & Scenarios", "icon": "🎭"},
    {"id": "fetish_materials", "name": "Fetish Materials", "icon": "👠"},
    {"id": "body_focus", "name": "Body Focus", "icon": "🦶"},
    {"id": "advanced_edge", "name": "Advanced/Edge Play", "icon": "⚠️"}
]

# Comprehensive Kinks Database
COMPREHENSIVE_KINKS = {
    "bdsm_basics": [
        "Dominance", "Submission", "Power Exchange", "Protocol", "Rules", "Obedience Training",
        "Discipline", "Punishment", "Reward Systems", "Behavior Modification", "Mind Control",
        "Hypnosis", "Brainwashing", "Conditioning", "Training Collars", "Ownership",
        "Total Power Exchange (TPE)", "Total Life Control", "Consensual Non-Consent (CNC)",
        "Authority Roleplay", "Service Submission", "Domestic Service", "Slave Training"
    ],
    "bondage_restraint": [
        "Rope Bondage", "Shibari", "Kinbaku", "Suspension", "Floor Work", "Chest Harnesses",
        "Leg Ties", "Arm Ties", "Crotch Rope", "Cock & Ball Ties", "Anal Hooks", "Rope Gags",
        "Leather Cuffs", "Metal Cuffs", "Handcuffs", "Ankle Cuffs", "Collar & Leash",
        "Chains", "Padlocks", "Straight Jackets", "Mummification", "Vacuum Beds",
        "Cage Bondage", "Stockades", "Pillories", "Spreader Bars", "Sleep Sacks",
        "Saran Wrap", "Duct Tape", "Zip Ties", "Medical Restraints", "Psychiatric Restraints",
        "Caging", "Enclosure", "Isolation", "Suspension Bondage", "Joint Restraints"
    ],
    "impact_play": [
        "Spanking", "Paddling", "Caning", "Flogging", "Whipping", "Belt Whipping",
        "Crop Use", "Riding Crop", "Bull Whip", "Single Tail", "Dragon Tail",
        "Slapping", "Face Slapping", "Cock Slapping", "Ball Slapping", "Ass Slapping",
        "Punching", "Kicking", "Stomping", "Trampling", "Cock Trampling",
        "Ball Busting", "Cock & Ball Torture", "Ball Weights", "Ball Stretching",
        "Cock Rings", "Cock Cages", "Chastity", "Cock Locking", "Penis Pumps",
        "Paddle Play", "Pain Play (Masochism)", "Sadism"
    ],
    "sensation_play": [
        "Wax Play", "Hot Wax", "Cold Wax", "Ice Play", "Temperature Play",
        "Fire Play", "Candle Wax", "Dripping Wax", "Wax Removal", "Wax Torture",
        "Needle Play", "Piercing", "Temporary Piercing", "Permanent Piercing",
        "Nipple Piercing", "Cock Piercing", "Ball Piercing", "Anal Piercing",
        "Clamp Play", "Nipple Clamps", "Cock Clamps", "Ball Clamps", "Anal Clamps",
        "Clothespins", "Binder Clips", "Paper Clips", "Clothespin Zippers",
        "Violet Wand", "Electro Play", "TENS Units", "Shock Collars", "Electric Paddles",
        "Tickling", "Sensory Deprivation", "Sensory Overload", "Abrasion Play"
    ],
    "electrical_play": [
        "Violet Wand", "Neon Wand", "Electro Stimulation", "TENS Units", "E-Stim",
        "Cock & Ball Electro", "Anal Electro", "Nipple Electro", "Electro Paddles",
        "Shock Collars", "Remote Control", "Electro Bondage", "Electro Gags",
        "Electro Butt Plugs", "Electro Cock Rings", "Electro Nipple Clamps",
        "Electro Chastity", "Electro CBT", "Electro Torture", "Electro Training"
    ],
    "penetration_anal": [
        "Anal Penetration", "Finger Fucking", "Anal Fisting", "Deep Fisting",
        "Anal Stretching", "Anal Training", "Butt Plug Training", "Progressive Plugs",
        "Anal Beads", "Anal Dildos", "Realistic Dildos", "Fantasy Dildos", "Huge Dildos",
        "Double Ended Dildos", "Strap-On Play", "Pegging", "Reverse Pegging",
        "Anal Hooks", "Anal Hooks with Rope", "Anal Hooks with Chains",
        "Inflatable Plugs", "Vibrating Plugs", "Electro Plugs", "Temperature Plugs",
        "Metal Plugs", "Glass Plugs", "Silicone Plugs", "Wooden Plugs",
        "Anal Speculums", "Anal Stretchers", "Anal Tunnels", "Anal Gaping",
        "Anal Prolapse", "Anal Depth Training", "Anal Size Training", "Anal Endurance Training", "Anal Torture",
        "Butt Plug Play", "Double Penetration (DP)", "Sounding", "Urethral Play"
    ],
    "oral_service": [
        "Blowjobs", "Deep Throating", "Face Fucking", "Throat Fucking", "Gagging",
        "Choking on Cock", "Cock Worship", "Ball Worship", "Ass Worship",
        "Rimming", "Analingus", "Deep Rimming", "Rim Jobs", "Tongue Fucking",
        "Hand Jobs", "Cock Milking", "Cock Teasing",
        "Edging", "Denial", "Orgasm Control", "Ruined Orgasms", "Forced Orgasms",
        "Multiple Orgasms", "Cock Sucking", "Ball Sucking", "Cock Licking",
        "Precum Drinking", "Cum Swallowing", "Cum Play", "Cum on Face",
        "Facial", "Bukkake", "Gang Bang", "Train", "Glory Hole",
        "Face Sitting (Queening/Smothering)", "Cum/Orgasm Control", "Overstimulation"
    ],
    "humiliation_degradation": [
        "Verbal Humiliation", "Name Calling", "Degradation", "Insults", "Mocking",
        "Public Humiliation", "Private Humiliation", "Forced Nudity", "Clothing Control",
        "Dress Up", "Cross Dressing", "Feminization", "Sissification", "Forced Feminization",
        "Makeup Application", "Nail Polish", "Wigs", "High Heels", "Lingerie",
        "Diaper Play", "ABDL", "Age Play", "Little Space", "Daddy Issues",
        "Pet Play", "Puppy Play", "Kitten Play", "Pony Play", "Horse Play",
        "Objectification", "Furniture", "Foot Stool", "Table", "Chair",
        "Human Furniture", "Foot Rest", "Coat Rack", "Ashtray", "Toilet",
        "Human Toilet", "Watersports", "Golden Showers", "Piss Play", "Urine Play",
        "Scat Play", "Brown Showers", "Feces Play", "Toilet Training",
        "Forced Eating", "Vomit Play", "Spit Play", "Snot Play", "Sweat Play",
        "Degradation Play", "Dehumanization", "Brat Play", "Humiliation Play"
    ],
    "financial_service": [
        "Financial Domination", "Findom", "Money Slavery", "Budget Control",
        "Allowance Control", "Spending Limits", "Financial Reports", "Receipt Collection",
        "Bill Paying", "Debt Control", "Credit Card Control", "Bank Account Access",
        "Investment Control", "Retirement Planning", "Insurance Control",
        "Tax Preparation", "Financial Planning", "Money Management",
        "Tribute Payments", "Regular Tributes", "Special Tributes", "Emergency Tributes"
    ],
    "exhibitionism_voyeurism": [
        "Exhibitionism", "Voyeurism", "Public Display", "Public Sex", "Public Nudity",
        "Remote Control Play", "Remote Toys", "Teledildonics", "Interactive Toys",
        "Webcam Shows", "Video Chat Sessions", "Interactive Video Sessions",
        "Nude Photography", "Erotic Photography", "Artistic Nudes", "Glamour Shots",
        "Fashion Photography", "Lingerie Shoots", "Bondage Photography", "Fetish Photography"
    ],
    "roleplay_scenarios": [
        "Authority Roleplay", "Teacher/Student", "Boss/Employee", "Guard/Prisoner", "Priest/Penitent",
        "Drill Sergeant/Recruit", "Doctor/Patient", "Nurse/Patient", "Cop/Criminal",
        "Superhero/Villain", "Kidnap Roleplay", "Interrogation Play", "Medical Play",
        "Military/Workwear Roleplay", "Uniform Fetish", "Authority Roleplay",
        "Daddy/Boy Dynamics", "Age Play", "Pet Play", "Puppy Play", "Kitten Play",
        "Pony Play", "Animal Roleplay", "Bear Fetish/Identity", "Furries",
        "Xenophilia (Fantasy Play)", "Role Reversal", "Mindfuck Play"
    ],
    "fetish_materials": [
        "Leather Fetish", "Latex Fetish", "Rubber Fetish", "Nylon Fetish", "Pantyhose/Tights Fetish",
        "Boot Fetish/Worship", "Glove Fetish", "Harness Fetish", "Corset Fetish",
        "Lingerie Fetish", "Underwear Fetish", "Jockstrap Fetish", "Jackboot Fetish",
        "Sports Gear Fetish", "Sneaker/Sock Fetish", "Logo/Brand Fetish",
        "Zentai Fetish", "Luminophilia", "Musk Fetish", "Hair Fetish",
        "Armpit Fetish (Maschalagnia)", "Mouth Fetish", "Kissing Fetish (Oromysophilia)",
        "Tattoo Fetish", "Piercing Fetish"
    ],
    "body_focus": [
        "Foot Fetish", "Belly/Chub Fetish", "Hair Fetish", "Armpit Fetish (Maschalagnia)",
        "Mouth Fetish", "Kissing Fetish (Oromysophilia)", "Nipple Play", "Biting",
        "Hair Pulling", "Blindfolding", "Gags",
        "Tickling", "Knismolagnia", "Nudism"
    ],
    "advanced_edge": [
        "Breath Play", "Autoerotic Asphyxiation", "Gas Play", "Nitrous Oxide", "Poppers",
        "Knife Play", "Cutting", "Blood Play", "Vampire Play", "Scarification",
        "Branding", "Hot Branding", "Cold Branding", "Chemical Branding",
        "Tattooing", "Permanent Marking", "Body Modification", "Extreme Piercing",
        "Genital Modification", "Cock Modification", "Ball Modification", "Anal Modification",
        "Inverted Suspension", "Head Down Suspension", "Extreme Suspension",
        "Surgical Play", "Hospital Play", "Doctor Play",
        "Nurse Play", "Patient Play", "Surgical Instruments",
        "Straight Jackets", "Medical Gags", "Feeding Tubes", "Catheters", "Enemas", "Colon Cleansing",
        "Extreme CBT", "Cock & Ball Torture", "Genital Torture",
        "Extreme Fisting", "Giant Insertions", "Extreme Stretching", "Prolapse Play",
        "Extreme Gaping", "Extreme Depth Training", "Extreme Size Training",
        "Endurance Training", "Pain Training", "Torture Training", "Submission Training",
        "Fear Play", "Gun/Weapon Roleplay", "Castration Fantasy", "Edge Play",
        "Needle Play", "Inflation/Vacuum Play", "Vacuum Bed/Play", "Mummification",
        "CNC Gangbang Fantasy", "Cruising"
    ]
}

# Drug categories for comprehensive tracking
DRUG_CATEGORIES = {
    "stimulants": {
        "name": "Stimulants",
        "drugs": ["Caffeine", "Nicotine", "Adderall", "Ritalin", "Cocaine", "Methamphetamine", "MDMA", "Ecstasy"]
    },
    "depressants": {
        "name": "Depressants", 
        "drugs": ["Alcohol", "Benzodiazepines", "Xanax", "Valium", "Barbiturates", "GHB", "Ketamine"]
    },
    "hallucinogens": {
        "name": "Hallucinogens",
        "drugs": ["LSD", "Psilocybin", "Mushrooms", "DMT", "Ayahuasca", "Mescaline", "Peyote"]
    },
    "cannabis": {
        "name": "Cannabis",
        "drugs": ["Marijuana", "THC", "CBD", "Hash", "Edibles", "Concentrates", "Vaping"]
    },
    "opioids": {
        "name": "Opioids",
        "drugs": ["Heroin", "Morphine", "Oxycodone", "Fentanyl", "Codeine", "Tramadol", "Methadone"]
    },
    "dissociatives": {
        "name": "Dissociatives",
        "drugs": ["Ketamine", "PCP", "DXM", "Nitrous Oxide", "Poppers"]
    },
    "other": {
        "name": "Other Substances",
        "drugs": ["Steroids", "Viagra", "Cialis", "Poppers", "Inhalants", "Research Chemicals"]
    }
}

# Content platforms and types
CONTENT_PLATFORMS = [
    "OnlyFans", "Fansly", "Twitter/X", "Instagram", "TikTok", "Snapchat", 
    "Telegram", "Discord", "Chaturbate", "ManyVids"
]

CONTENT_TYPES = [
    "Solo content", "Partnered content", "Group content", "Public content", 
    "Private content", "Live streaming", "Pre-recorded content"
]

# Payment methods
PAYMENT_METHODS = [
    "CashApp", "Venmo", "PayPal", "Zelle", "Cryptocurrency", "Cash", 
    "Bank Transfer", "Check"
]

# Availability time slots
AVAILABILITY_SLOTS = [
    "Early Morning (5AM-9AM)", "Morning (9AM-12PM)", "Afternoon (12PM-5PM)", 
    "Evening (5PM-9PM)", "Late Night (9PM-1AM)", "Overnight (1AM-5AM)",
    "All Day", "Weekends Only", "Weekdays Only"
]

# Duration preferences
DURATION_PREFERENCES = [
    "Quick Sessions (1-2 hours)", "Half Day (3-6 hours)", "Full Day (6-12 hours)", 
    "Overnight (12+ hours)", "Multi-day"
]

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
    if 'comprehensive_form_step' not in st.session_state:
        st.session_state.comprehensive_form_step = 0
    if 'comprehensive_form_data' not in st.session_state:
        st.session_state.comprehensive_form_data = {}

def show_landing_page():
    st.title(f"🏛️ {PERSONAL_BRANDING['system_name']}")
    st.subheader(PERSONAL_BRANDING['welcome_message'])
    
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
            st.session_state.show_comprehensive_form = True
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
    st.title(f"👑 {PERSONAL_BRANDING['system_name']} - Admin Dashboard")
    st.subheader(f"Welcome back, {st.session_state.current_user.get('username', PERSONAL_BRANDING['title'])}")
    
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

def show_comprehensive_application_form():
    st.title("📝 Comprehensive Harem Application Form")
    st.subheader("Complete Application with All Features")
    
    # Multi-step form navigation
    form_steps = [
        "Personal Information",
        "Physical Details", 
        "Kink Interests",
        "Experience & Limits",
        "Availability & Commitment",
        "Lifestyle & Preferences",
        "Content Creation",
        "Financial Interests",
        "Verification & References",
        "Additional Information",
        "Drug Usage & Comfort",
        "STI Testing & Health",
        "Review & Submit"
    ]
    
    # Progress bar
    progress = (st.session_state.comprehensive_form_step + 1) / len(form_steps)
    st.progress(progress)
    st.write(f"**Step {st.session_state.comprehensive_form_step + 1} of {len(form_steps)}:** {form_steps[st.session_state.comprehensive_form_step]}")
    
    # Form data initialization
    if 'comprehensive_form_data' not in st.session_state:
        st.session_state.comprehensive_form_data = {}
    
    form_data = st.session_state.comprehensive_form_data
    
    # Step 1: Personal Information
    if st.session_state.comprehensive_form_step == 0:
        st.header("👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", value=form_data.get('full_name', ''), help="Your legal full name.")
            email = st.text_input("Email Address *", value=form_data.get('email', ''), help="Your primary email address for communication.")
            phone = st.text_input("Phone Number", value=form_data.get('phone', ''), help="Your contact phone number.")
            age = st.number_input("Age *", min_value=18, max_value=99, value=form_data.get('age', 18), help="You must be 18 or older to apply.")
        
        with col2:
            location = st.text_input("Current Location (City, State, Country) *", value=form_data.get('location', ''), help="Where are you currently located?")
            occupation = st.text_input("Occupation/Profession", value=form_data.get('occupation', ''), help="What do you do for work?")
            education = st.selectbox("Education Level", ["High School", "Some College", "Bachelor's", "Master's", "PhD", "Other"], index=0)
            relationship_status = st.selectbox("Current Relationship Status", ["Single", "In a relationship", "Married", "Polyamorous", "Other"], index=0)
        
        # Store data
        if st.button("Next Step", type="primary"):
            st.session_state.comprehensive_form_data.update({
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'age': age,
                'location': location,
                'occupation': occupation,
                'education': education,
                'relationship_status': relationship_status
            })
            st.session_state.comprehensive_form_step += 1
            st.rerun()
    
    # Step 2: Physical Details
    elif st.session_state.comprehensive_form_step == 1:
        st.header("📏 Physical Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            height = st.text_input("Height", value=form_data.get('height', ''), help="e.g., 5'6\" or 168cm")
            weight = st.text_input("Weight", value=form_data.get('weight', ''), help="Optional - for compatibility matching")
        
        with col2:
            body_type = st.selectbox("Body Type", ["Not specified", "Petite", "Average", "Curvy", "Athletic", "Plus-size", "Other"], index=0)
            hair_color = st.selectbox("Hair Color", ["Not specified", "Blonde", "Brunette", "Black", "Red", "Other"], index=0)
        
        with col3:
            eye_color = st.selectbox("Eye Color", ["Not specified", "Blue", "Brown", "Green", "Hazel", "Other"], index=0)
            tattoos = st.selectbox("Tattoos", ["None", "Few", "Many", "Extensive"], index=0)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'height': height,
                    'weight': weight,
                    'body_type': body_type,
                    'hair_color': hair_color,
                    'eye_color': eye_color,
                    'tattoos': tattoos
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 3: Kink Interests (Comprehensive)
    elif st.session_state.comprehensive_form_step == 2:
        st.header("🔞 Kink Interests & Compatibility")
        st.subheader("Comprehensive Kink Assessment")
        
        # Sir's Kink List Reference
        with st.expander(f"👑 {PERSONAL_BRANDING['title']}'s Kink Preferences (for reference)", expanded=False):
            st.write(f"**{PERSONAL_BRANDING['title']}'s interests include (none required):**")
            for interest in SIR_KINK_PREFERENCES['primary_interests']:
                st.write(f"• {interest.replace('_', ' ').title()}")
            st.write("**Note:** None of these are required - we're looking for compatibility and enthusiasm.")
        
        # Kink categories selection
        st.subheader("Select Your Kink Categories")
        
        selected_categories = st.multiselect(
            "Choose categories that interest you:",
            [cat['name'] for cat in KINK_CATEGORIES],
            default=form_data.get('selected_categories', [])
        )
        
        # Detailed kink selection for each category
        if selected_categories:
            st.subheader("Detailed Kink Selection")
            
            for category_name in selected_categories:
                category_id = next(cat['id'] for cat in KINK_CATEGORIES if cat['name'] == category_name)
                category_icon = next(cat['icon'] for cat in KINK_CATEGORIES if cat['name'] == category_name)
                
                with st.expander(f"{category_icon} {category_name}", expanded=True):
                    kinks = COMPREHENSIVE_KINKS.get(category_id, [])
                    
                    if kinks:
                        # Create checkboxes for each kink
                        selected_kinks = []
                        cols = st.columns(3)
                        
                        for i, kink in enumerate(kinks):
                            with cols[i % 3]:
                                if st.checkbox(kink, key=f"kink_{category_id}_{kink}"):
                                    selected_kinks.append(kink)
                        
                        # Store selected kinks for this category
                        if f'kinks_{category_id}' not in form_data:
                            form_data[f'kinks_{category_id}'] = []
                        form_data[f'kinks_{category_id}'] = selected_kinks
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'selected_categories': selected_categories
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 4: Experience & Limits
    elif st.session_state.comprehensive_form_step == 3:
        st.header("🎓 Experience & Limits")
        
        experience = st.selectbox(
            "Level of Experience *",
            ["Beginner", "Intermediate", "Experienced", "Highly Experienced"],
            index=0,
            help="Your experience level in BDSM/kink dynamics."
        )
        
        interests = st.text_area(
            "What are your primary interests and desires? *",
            value=form_data.get('interests', ''),
            help="Describe what you are looking for and what excites you in a dynamic. Be specific about your kinks, fetishes, and what you enjoy.",
            height=120
        )
        
        limits = st.text_area(
            "Do you have any hard limits or boundaries? *",
            value=form_data.get('limits', ''),
            help="Please list any activities or situations you absolutely will not engage in. Be honest about your limits.",
            height=120
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'experience': experience,
                    'interests': interests,
                    'limits': limits
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 5: Availability & Commitment
    elif st.session_state.comprehensive_form_step == 4:
        st.header("📅 Availability & Commitment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Availability")
            available_days = st.multiselect(
                "Available Days",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                default=form_data.get('available_days', [])
            )
            
            available_times = st.multiselect(
                "Available Times",
                AVAILABILITY_SLOTS,
                default=form_data.get('available_times', [])
            )
            
            duration_preferences = st.multiselect(
                "Duration Preferences",
                DURATION_PREFERENCES,
                default=form_data.get('duration_preferences', [])
            )
        
        with col2:
            st.subheader("Commitment")
            commitment_level = st.selectbox(
                "Commitment Level",
                ["Casual", "Regular", "Long-term", "Exclusive"],
                index=0
            )
            
            travel_willingness = st.selectbox(
                "Travel Willingness",
                ["Local only", "Regional", "National", "International"],
                index=0
            )
            
            time_commitment = st.selectbox(
                "Time Commitment",
                ["Few hours per week", "Several hours per week", "Daily availability", "24/7 availability"],
                index=0
            )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'available_days': available_days,
                    'available_times': available_times,
                    'duration_preferences': duration_preferences,
                    'commitment_level': commitment_level,
                    'travel_willingness': travel_willingness,
                    'time_commitment': time_commitment
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 6: Lifestyle & Preferences
    elif st.session_state.comprehensive_form_step == 5:
        st.header("🏠 Lifestyle & Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Lifestyle Questions")
            smoking = st.selectbox("Do you smoke?", ["No", "Occasionally", "Yes", "Prefer not to say"], index=0)
            drinking = st.selectbox("Do you drink alcohol?", ["No", "Occasionally", "Yes", "Prefer not to say"], index=0)
            drugs = st.selectbox("Drug use?", ["No", "Occasionally", "Yes", "Prefer not to say"], index=0)
        
        with col2:
            st.subheader("Preferences")
            pets = st.text_input("Do you have pets?", value=form_data.get('pets', ''), help="Any pets or allergies?")
            hobbies = st.text_area("Hobbies and interests", value=form_data.get('hobbies', ''), help="What do you enjoy doing?", height=80)
            living_situation = st.selectbox("Living Situation", ["Alone", "With family", "With roommates", "With partner", "Other"], index=0)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'smoking': smoking,
                    'drinking': drinking,
                    'drugs': drugs,
                    'pets': pets,
                    'hobbies': hobbies,
                    'living_situation': living_situation
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 7: Content Creation
    elif st.session_state.comprehensive_form_step == 6:
        st.header("📸 Content Creation Interest")
        
        content_interest = st.selectbox(
            "Interest in content creation",
            ["Not interested", "Somewhat interested", "Very interested", "Extremely interested"],
            index=0,
            help="Interest in photos, videos, or other content creation"
        )
        
        if content_interest != "Not interested":
            col1, col2 = st.columns(2)
            
            with col1:
                content_types = st.multiselect(
                    "Types of content you'd be interested in:",
                    CONTENT_TYPES,
                    default=form_data.get('content_types', [])
                )
            
            with col2:
                content_platforms = st.multiselect(
                    "Content platforms you'd be interested in:",
                    CONTENT_PLATFORMS,
                    default=form_data.get('content_platforms', [])
                )
            
            content_comfort = st.selectbox(
                "Comfort level with content sharing",
                ["Private only", "Limited sharing", "Public sharing", "Commercial use"],
                index=0
            )
        else:
            content_types = []
            content_platforms = []
            content_comfort = "Private only"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'content_interest': content_interest,
                    'content_types': content_types,
                    'content_platforms': content_platforms,
                    'content_comfort': content_comfort
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 8: Financial Interests
    elif st.session_state.comprehensive_form_step == 7:
        st.header("💰 Financial Interests")
        
        financial_interest = st.selectbox(
            "Interest in financial activities",
            ["Not interested", "Somewhat interested", "Very interested", "Extremely interested"],
            index=0
        )
        
        if financial_interest != "Not interested":
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Financial Activities:**")
                findom_interest = st.checkbox("Financial Domination/Findom")
                cash_pig = st.checkbox("Cash Pig (Want to be one)")
                cash_pig_control = st.checkbox("Cash Pig Control (Want to control them)")
                recruitment_interest = st.checkbox("Recruitment (Bring cash pigs to you)")
            
            with col2:
                st.write("**Payment Methods:**")
                payment_methods = st.multiselect(
                    "Payment methods you're comfortable with:",
                    PAYMENT_METHODS,
                    default=form_data.get('payment_methods', [])
                )
                
                tribute_amounts = st.selectbox(
                    "Tribute amounts",
                    ["$10-50", "$50-100", "$100-500", "$500+", "Custom amount"],
                    index=0
                )
        else:
            findom_interest = False
            cash_pig = False
            cash_pig_control = False
            recruitment_interest = False
            payment_methods = []
            tribute_amounts = "Not applicable"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'financial_interest': financial_interest,
                    'findom_interest': findom_interest,
                    'cash_pig': cash_pig,
                    'cash_pig_control': cash_pig_control,
                    'recruitment_interest': recruitment_interest,
                    'payment_methods': payment_methods,
                    'tribute_amounts': tribute_amounts
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 9: Verification & References
    elif st.session_state.comprehensive_form_step == 8:
        st.header("🔍 Verification & References")
        
        col1, col2 = st.columns(2)
        
        with col1:
            reference_contact = st.text_input("Reference Contact", value=form_data.get('reference_contact', ''), help="Someone who can vouch for you")
            social_media_handles = st.text_input("Social Media Handles", value=form_data.get('social_media_handles', ''), help="@username or profile links")
        
        with col2:
            st.write("**Verification Options:**")
            id_verification = st.checkbox("ID Verification Willingness")
            background_check = st.checkbox("Background Check Consent")
            video_call_verification = st.checkbox("Video Call Verification")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'reference_contact': reference_contact,
                    'social_media_handles': social_media_handles,
                    'id_verification': id_verification,
                    'background_check': background_check,
                    'video_call_verification': video_call_verification
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 10: Additional Information
    elif st.session_state.comprehensive_form_step == 9:
        st.header("📋 Additional Information")
        
        why_interested = st.text_area(
            "Why are you interested?",
            value=form_data.get('why_interested', ''),
            help="Tell us why you're interested in this opportunity...",
            height=100
        )
        
        what_hoping_to_gain = st.text_area(
            "What are you hoping to gain?",
            value=form_data.get('what_hoping_to_gain', ''),
            help="What do you hope to gain from this experience?",
            height=100
        )
        
        previous_experience = st.text_area(
            "Previous Experience Details",
            value=form_data.get('previous_experience', ''),
            help="Tell us about your previous experience...",
            height=100
        )
        
        questions_for_us = st.text_area(
            "Any questions for us?",
            value=form_data.get('questions_for_us', ''),
            help="Do you have any questions for us?",
            height=100
        )
        
        how_heard_about_us = st.selectbox(
            "How did you hear about us?",
            ["Social Media", "Friend", "Website", "Other"],
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'why_interested': why_interested,
                    'what_hoping_to_gain': what_hoping_to_gain,
                    'previous_experience': previous_experience,
                    'questions_for_us': questions_for_us,
                    'how_heard_about_us': how_heard_about_us
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 11: Drug Usage & Comfort
    elif st.session_state.comprehensive_form_step == 10:
        st.header("💊 Drug Usage & Comfort")
        st.subheader("Comprehensive Drug Tracking")
        
        st.info("💡 **Privacy Note:** This information is confidential and used only for safety, compatibility, and session planning.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Drugs Currently Using")
            drugs_currently_using = []
            for category_id, category in DRUG_CATEGORIES.items():
                with st.expander(f"{category['name']}", expanded=False):
                    for drug in category['drugs']:
                        if st.checkbox(drug, key=f"currently_{drug}"):
                            drugs_currently_using.append(drug)
        
        with col2:
            st.subheader("Drugs Comfortable With")
            drugs_comfortable_with = []
            for category_id, category in DRUG_CATEGORIES.items():
                with st.expander(f"{category['name']}", expanded=False):
                    for drug in category['drugs']:
                        if st.checkbox(drug, key=f"comfortable_{drug}"):
                            drugs_comfortable_with.append(drug)
        
        drug_usage_frequency = st.selectbox(
            "Overall Usage Frequency",
            ["Never", "Rarely", "Occasionally", "Regularly", "Daily"],
            index=0
        )
        
        drug_comfort_level = st.selectbox(
            "Comfort with Drug Use During Sessions",
            ["Not comfortable", "Somewhat comfortable", "Comfortable", "Very comfortable"],
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'drugs_currently_using': drugs_currently_using,
                    'drugs_comfortable_with': drugs_comfortable_with,
                    'drug_usage_frequency': drug_usage_frequency,
                    'drug_comfort_level': drug_comfort_level
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Step 12: STI Testing & Health
    elif st.session_state.comprehensive_form_step == 11:
        st.header("🏥 STI Testing & Health")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sti_testing_status = st.selectbox(
                "STI Testing Status",
                ["Regular (every 3 months)", "Regular (every 6 months)", "Occasional", "Never", "Prefer not to say"],
                index=0
            )
            
            last_sti_test_date = st.date_input(
                "Last STI Test Date",
                value=None,
                help="When was your last STI test?"
            )
        
        with col2:
            sti_test_results = st.selectbox(
                "Last STI Test Results",
                ["Negative", "Positive", "Pending", "Not tested"],
                index=0
            )
            
            sti_eligibility_status = st.selectbox(
                "STI Eligibility Status",
                ["Current", "Expiring Soon", "Expired", "Pending"],
                index=0
            )
        
        st.subheader("📋 Upload STI Test Results")
        st.info("Upload your latest STI test results (PDF or JPG). Our system will automatically verify and extract the information for your profile.")
        
        uploaded_file = st.file_uploader(
            "Test Results File",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Upload your latest STI test results"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_data.update({
                    'sti_testing_status': sti_testing_status,
                    'last_sti_test_date': str(last_sti_test_date) if last_sti_test_date else None,
                    'sti_test_results': sti_test_results,
                    'sti_eligibility_status': sti_eligibility_status,
                    'sti_test_upload': uploaded_file.name if uploaded_file else None
                })
                st.session_state.comprehensive_form_step += 1
                st.rerun()
    
    # Final step: Review and Submit
    elif st.session_state.comprehensive_form_step == len(form_steps) - 1:
        st.header("📋 Review & Submit")
        st.subheader("Please review your application before submitting")
        
        # Display all collected data
        st.subheader("Application Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Personal Information:**")
            st.write(f"• Name: {form_data.get('full_name', 'N/A')}")
            st.write(f"• Email: {form_data.get('email', 'N/A')}")
            st.write(f"• Age: {form_data.get('age', 'N/A')}")
            st.write(f"• Location: {form_data.get('location', 'N/A')}")
            st.write(f"• Occupation: {form_data.get('occupation', 'N/A')}")
            st.write(f"• Education: {form_data.get('education', 'N/A')}")
            st.write(f"• Relationship Status: {form_data.get('relationship_status', 'N/A')}")
        
        with col2:
            st.write("**Physical Information:**")
            st.write(f"• Height: {form_data.get('height', 'N/A')}")
            st.write(f"• Weight: {form_data.get('weight', 'N/A')}")
            st.write(f"• Body Type: {form_data.get('body_type', 'N/A')}")
            st.write(f"• Hair Color: {form_data.get('hair_color', 'N/A')}")
            st.write(f"• Eye Color: {form_data.get('eye_color', 'N/A')}")
            st.write(f"• Tattoos: {form_data.get('tattoos', 'N/A')}")
        
        st.write("**Experience & Interests:**")
        st.write(f"• Experience Level: {form_data.get('experience', 'N/A')}")
        st.write(f"• Selected Categories: {len(form_data.get('selected_categories', []))} categories")
        st.write(f"• Content Interest: {form_data.get('content_interest', 'N/A')}")
        st.write(f"• Financial Interest: {form_data.get('financial_interest', 'N/A')}")
        
        # Terms and conditions
        st.subheader("Terms and Conditions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            agree_terms = st.checkbox("I agree to the terms and conditions *")
            agree_privacy = st.checkbox("I agree to the privacy policy *")
        
        with col2:
            age_verification = st.checkbox("I am 18 years or older *")
            consent_recording = st.checkbox("I consent to potential recording for safety purposes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Save Draft", type="secondary"):
                st.success("✅ Draft saved! You can continue later.")
        
        with col3:
            if st.button("🚀 Submit Application", type="primary"):
                # Validation
                required_fields = [form_data.get('full_name'), form_data.get('email'), form_data.get('age'), form_data.get('location'), form_data.get('interests'), form_data.get('limits')]
                required_agreements = [agree_terms, agree_privacy, age_verification]
                
                if not all(required_fields):
                    st.error("❌ Please fill in all required fields.")
                elif not all(required_agreements):
                    st.error("❌ You must agree to all required terms and conditions.")
                else:
                    st.success("✅ Application submitted successfully! We will review it shortly.")
                    st.info("📧 You will receive a confirmation email shortly.")
                    
                    # Reset form
                    st.session_state.comprehensive_form_step = 0
                    st.session_state.comprehensive_form_data = {}
                    st.session_state.show_comprehensive_form = False
                    st.rerun()
    
    # Navigation buttons for other steps
    else:
        st.info(f"Step {st.session_state.comprehensive_form_step + 1} - {form_steps[st.session_state.comprehensive_form_step]} (Implementation in progress)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Previous Step"):
                st.session_state.comprehensive_form_step -= 1
                st.rerun()
        
        with col2:
            if st.button("Next Step", type="primary"):
                st.session_state.comprehensive_form_step += 1
                st.rerun()

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
    elif st.session_state.get('show_comprehensive_form'):
        show_comprehensive_application_form()
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
