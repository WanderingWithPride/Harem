"""
Sir's Briefing and Memory Management System
Comprehensive briefing system to keep Sir's memory up to date on all subs, preferences, plans, and status.
Provides detailed information and context for effective harem management.
"""

import streamlit as st
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SirBriefingSystem:
    """Comprehensive briefing system for Sir's memory management"""
    
    def __init__(self):
        self.sub_profiles = {}
        self.briefing_history = {}
        self.memory_notes = {}
        self.relationship_tracking = {}
        self.performance_metrics = {}
        self.plans_and_goals = {}
    
    def create_sub_profile(self, sub_data: Dict) -> str:
        """Create comprehensive sub profile"""
        try:
            profile_id = f"SUB-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
            
            profile = {
                "profile_id": profile_id,
                "basic_info": {
                    "name": sub_data.get("name", ""),
                    "age": sub_data.get("age", ""),
                    "location": sub_data.get("location", ""),
                    "occupation": sub_data.get("occupation", ""),
                    "relationship_status": sub_data.get("relationship_status", ""),
                    "contact_info": sub_data.get("contact_info", {}),
                    "emergency_contact": sub_data.get("emergency_contact", {})
                },
                "physical_profile": {
                    "height": sub_data.get("height", ""),
                    "weight": sub_data.get("weight", ""),
                    "body_type": sub_data.get("body_type", ""),
                    "hair_color": sub_data.get("hair_color", ""),
                    "eye_color": sub_data.get("eye_color", ""),
                    "distinguishing_features": sub_data.get("distinguishing_features", ""),
                    "health_conditions": sub_data.get("health_conditions", ""),
                    "medications": sub_data.get("medications", ""),
                    "allergies": sub_data.get("allergies", ""),
                    "blood_type": sub_data.get("blood_type", "")
                },
                "kink_profile": {
                    "experience_level": sub_data.get("experience_level", ""),
                    "primary_interests": sub_data.get("primary_interests", []),
                    "kink_ratings": sub_data.get("kink_ratings", {}),
                    "hard_limits": sub_data.get("hard_limits", []),
                    "soft_limits": sub_data.get("soft_limits", []),
                    "favorite_activities": sub_data.get("favorite_activities", []),
                    "turn_ons": sub_data.get("turn_ons", []),
                    "turn_offs": sub_data.get("turn_offs", []),
                    "safety_concerns": sub_data.get("safety_concerns", [])
                },
                "service_profile": {
                    "service_type": sub_data.get("service_type", ""),
                    "availability": sub_data.get("availability", {}),
                    "commitment_level": sub_data.get("commitment_level", ""),
                    "special_skills": sub_data.get("special_skills", []),
                    "training_goals": sub_data.get("training_goals", []),
                    "performance_metrics": sub_data.get("performance_metrics", {}),
                    "service_history": sub_data.get("service_history", [])
                },
                "relationship_dynamics": {
                    "relationship_type": sub_data.get("relationship_type", ""),
                    "communication_style": sub_data.get("communication_style", ""),
                    "preferred_interaction": sub_data.get("preferred_interaction", ""),
                    "emotional_needs": sub_data.get("emotional_needs", []),
                    "boundaries": sub_data.get("boundaries", {}),
                    "expectations": sub_data.get("expectations", []),
                    "relationship_goals": sub_data.get("relationship_goals", [])
                },
                "sir_notes": {
                    "personal_observations": sub_data.get("personal_observations", ""),
                    "behavior_patterns": sub_data.get("behavior_patterns", ""),
                    "strengths": sub_data.get("strengths", []),
                    "areas_for_improvement": sub_data.get("areas_for_improvement", []),
                    "special_considerations": sub_data.get("special_considerations", ""),
                    "memory_aids": sub_data.get("memory_aids", ""),
                    "relationship_notes": sub_data.get("relationship_notes", "")
                },
                "current_status": {
                    "status": sub_data.get("status", "active"),
                    "last_contact": sub_data.get("last_contact", ""),
                    "next_scheduled": sub_data.get("next_scheduled", ""),
                    "current_goals": sub_data.get("current_goals", []),
                    "recent_activities": sub_data.get("recent_activities", []),
                    "upcoming_plans": sub_data.get("upcoming_plans", [])
                },
                "created_date": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "update_count": 0
            }
            
            # Store profile
            self.sub_profiles[profile_id] = profile
            
            # Log creation
            self._log_briefing("profile_created", profile_id, {"name": profile["basic_info"]["name"]})
            
            logger.info(f"Sub profile created: {profile_id}")
            return profile_id
            
        except Exception as e:
            logger.error(f"Error creating sub profile: {e}")
            raise
    
    def show_sir_briefing_dashboard(self):
        """Show comprehensive Sir's briefing dashboard"""
        st.markdown("# 👑 Sir's Briefing Dashboard")
        st.subheader("Complete Memory Management System")
        
        # Quick overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_subs = len(self.sub_profiles)
            st.metric("Total Subs", total_subs)
        
        with col2:
            active_subs = len([p for p in self.sub_profiles.values() if p["current_status"]["status"] == "active"])
            st.metric("Active Subs", active_subs)
        
        with col3:
            recent_contacts = len([p for p in self.sub_profiles.values() 
                                 if p["current_status"]["last_contact"] and 
                                 datetime.fromisoformat(p["current_status"]["last_contact"]) > datetime.now() - timedelta(days=7)])
            st.metric("Recent Contacts", recent_contacts)
        
        with col4:
            pending_plans = len([p for p in self.sub_profiles.values() 
                               if p["current_status"]["upcoming_plans"]])
            st.metric("Pending Plans", pending_plans)
        
        # Main briefing tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Quick Briefings", "👥 Sub Profiles", "📊 Performance Overview", 
            "🎯 Plans & Goals", "🧠 Memory Management"
        ])
        
        with tab1:
            self._show_quick_briefings()
        
        with tab2:
            self._show_sub_profiles()
        
        with tab3:
            self._show_performance_overview()
        
        with tab4:
            self._show_plans_and_goals()
        
        with tab5:
            self._show_memory_management()
    
    def _show_quick_briefings(self):
        """Show quick briefing summaries"""
        st.subheader("📋 Quick Briefings")
        
        if self.sub_profiles:
            # Recent activity briefing
            st.markdown("### 🔥 Recent Activity")
            
            recent_subs = []
            for profile_id, profile in self.sub_profiles.items():
                if profile["current_status"]["last_contact"]:
                    last_contact = datetime.fromisoformat(profile["current_status"]["last_contact"])
                    if last_contact > datetime.now() - timedelta(days=7):
                        recent_subs.append((profile_id, profile, last_contact))
            
            recent_subs.sort(key=lambda x: x[2], reverse=True)
            
            for profile_id, profile, last_contact in recent_subs[:5]:
                with st.expander(f"🔥 {profile['basic_info']['name']} - {last_contact.strftime('%m/%d %H:%M')}"):
                    self._show_sub_quick_brief(profile)
            
            # Upcoming plans briefing
            st.markdown("### 📅 Upcoming Plans")
            
            upcoming_subs = []
            for profile_id, profile in self.sub_profiles.items():
                if profile["current_status"]["upcoming_plans"]:
                    upcoming_subs.append((profile_id, profile))
            
            for profile_id, profile in upcoming_subs[:5]:
                with st.expander(f"📅 {profile['basic_info']['name']} - Upcoming Plans"):
                    st.write("**Upcoming Plans:**")
                    for plan in profile["current_status"]["upcoming_plans"]:
                        st.write(f"• {plan}")
            
            # Performance highlights
            st.markdown("### ⭐ Performance Highlights")
            
            high_performers = []
            for profile_id, profile in self.sub_profiles.items():
                if profile["service_profile"]["performance_metrics"]:
                    performance = profile["service_profile"]["performance_metrics"]
                    if performance.get("overall_rating", 0) >= 4.0:
                        high_performers.append((profile_id, profile, performance.get("overall_rating", 0)))
            
            high_performers.sort(key=lambda x: x[2], reverse=True)
            
            for profile_id, profile, rating in high_performers[:3]:
                with st.expander(f"⭐ {profile['basic_info']['name']} - Rating: {rating}/5"):
                    st.write(f"**Performance Rating:** {rating}/5")
                    st.write(f"**Recent Activities:** {', '.join(profile['current_status']['recent_activities'][:3])}")
        else:
            st.info("No sub profiles available for briefing")
    
    def _show_sub_quick_brief(self, profile: Dict):
        """Show quick briefing for a sub"""
        st.write(f"**Name:** {profile['basic_info']['name']}")
        st.write(f"**Age:** {profile['basic_info']['age']}")
        st.write(f"**Location:** {profile['basic_info']['location']}")
        st.write(f"**Status:** {profile['current_status']['status']}")
        
        if profile["kink_profile"]["primary_interests"]:
            st.write(f"**Primary Interests:** {', '.join(profile['kink_profile']['primary_interests'][:3])}")
        
        if profile["current_status"]["recent_activities"]:
            st.write(f"**Recent Activities:** {', '.join(profile['current_status']['recent_activities'][:2])}")
        
        if profile["sir_notes"]["personal_observations"]:
            st.write(f"**Sir's Notes:** {profile['sir_notes']['personal_observations']}")
    
    def _show_sub_profiles(self):
        """Show detailed sub profiles"""
        st.subheader("👥 Sub Profiles")
        
        if self.sub_profiles:
            # Profile selection
            profile_options = {f"{p['basic_info']['name']} ({p['profile_id']})": p_id 
                             for p_id, p in self.sub_profiles.items()}
            
            selected_profile = st.selectbox("Select Sub Profile", list(profile_options.keys()))
            
            if selected_profile:
                profile_id = profile_options[selected_profile]
                profile = self.sub_profiles[profile_id]
                
                # Show detailed profile
                self._show_detailed_sub_profile(profile)
        else:
            st.info("No sub profiles available")
    
    def _show_detailed_sub_profile(self, profile: Dict):
        """Show detailed sub profile"""
        st.markdown(f"### 👤 {profile['basic_info']['name']} - Detailed Profile")
        
        # Basic information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Basic Information**")
            st.write(f"**Name:** {profile['basic_info']['name']}")
            st.write(f"**Age:** {profile['basic_info']['age']}")
            st.write(f"**Location:** {profile['basic_info']['location']}")
            st.write(f"**Occupation:** {profile['basic_info']['occupation']}")
            st.write(f"**Relationship Status:** {profile['basic_info']['relationship_status']}")
            
            st.markdown("**🏥 Physical Profile**")
            st.write(f"**Height:** {profile['physical_profile']['height']}")
            st.write(f"**Weight:** {profile['physical_profile']['weight']}")
            st.write(f"**Body Type:** {profile['physical_profile']['body_type']}")
            st.write(f"**Hair Color:** {profile['physical_profile']['hair_color']}")
            st.write(f"**Eye Color:** {profile['physical_profile']['eye_color']}")
            st.write(f"**Blood Type:** {profile['physical_profile']['blood_type']}")
        
        with col2:
            st.markdown("**🔞 Kink Profile**")
            st.write(f"**Experience Level:** {profile['kink_profile']['experience_level']}")
            st.write(f"**Primary Interests:** {', '.join(profile['kink_profile']['primary_interests'])}")
            st.write(f"**Hard Limits:** {', '.join(profile['kink_profile']['hard_limits'])}")
            st.write(f"**Soft Limits:** {', '.join(profile['kink_profile']['soft_limits'])}")
            st.write(f"**Favorite Activities:** {', '.join(profile['kink_profile']['favorite_activities'])}")
            
            st.markdown("**🎯 Service Profile**")
            st.write(f"**Service Type:** {profile['service_profile']['service_type']}")
            st.write(f"**Commitment Level:** {profile['service_profile']['commitment_level']}")
            st.write(f"**Special Skills:** {', '.join(profile['service_profile']['special_skills'])}")
            st.write(f"**Training Goals:** {', '.join(profile['service_profile']['training_goals'])}")
        
        # Sir's notes and observations
        st.markdown("**👑 Sir's Notes & Observations**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Personal Observations:** {profile['sir_notes']['personal_observations']}")
            st.write(f"**Behavior Patterns:** {profile['sir_notes']['behavior_patterns']}")
            st.write(f"**Strengths:** {', '.join(profile['sir_notes']['strengths'])}")
            st.write(f"**Areas for Improvement:** {', '.join(profile['sir_notes']['areas_for_improvement'])}")
        
        with col2:
            st.write(f"**Special Considerations:** {profile['sir_notes']['special_considerations']}")
            st.write(f"**Memory Aids:** {profile['sir_notes']['memory_aids']}")
            st.write(f"**Relationship Notes:** {profile['sir_notes']['relationship_notes']}")
        
        # Current status and plans
        st.markdown("**📊 Current Status & Plans**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Status:** {profile['current_status']['status']}")
            st.write(f"**Last Contact:** {profile['current_status']['last_contact']}")
            st.write(f"**Next Scheduled:** {profile['current_status']['next_scheduled']}")
            st.write(f"**Current Goals:** {', '.join(profile['current_status']['current_goals'])}")
        
        with col2:
            st.write(f"**Recent Activities:** {', '.join(profile['current_status']['recent_activities'])}")
            st.write(f"**Upcoming Plans:** {', '.join(profile['current_status']['upcoming_plans'])}")
    
    def _show_performance_overview(self):
        """Show performance overview"""
        st.subheader("📊 Performance Overview")
        
        if self.sub_profiles:
            # Performance metrics
            performance_data = []
            for profile_id, profile in self.sub_profiles.items():
                if profile["service_profile"]["performance_metrics"]:
                    metrics = profile["service_profile"]["performance_metrics"]
                    performance_data.append({
                        "Name": profile["basic_info"]["name"],
                        "Overall Rating": metrics.get("overall_rating", 0),
                        "Service Quality": metrics.get("service_quality", 0),
                        "Communication": metrics.get("communication", 0),
                        "Reliability": metrics.get("reliability", 0),
                        "Initiative": metrics.get("initiative", 0)
                    })
            
            if performance_data:
                df = pd.DataFrame(performance_data)
                
                # Performance chart
                fig = px.bar(df, x="Name", y="Overall Rating", title="Overall Performance Ratings")
                st.plotly_chart(fig, use_container_width=True)
                
                # Performance table
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No performance data available")
        else:
            st.info("No sub profiles available")
    
    def _show_plans_and_goals(self):
        """Show plans and goals overview"""
        st.subheader("🎯 Plans & Goals Overview")
        
        if self.sub_profiles:
            # Collect all plans and goals
            all_plans = []
            all_goals = []
            
            for profile_id, profile in self.sub_profiles.items():
                name = profile["basic_info"]["name"]
                
                for plan in profile["current_status"]["upcoming_plans"]:
                    all_plans.append({"Name": name, "Plan": plan, "Type": "Upcoming Plan"})
                
                for goal in profile["current_status"]["current_goals"]:
                    all_goals.append({"Name": name, "Goal": goal, "Type": "Current Goal"})
                
                for goal in profile["service_profile"]["training_goals"]:
                    all_goals.append({"Name": name, "Goal": goal, "Type": "Training Goal"})
            
            # Display plans and goals
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📅 Upcoming Plans**")
                if all_plans:
                    for plan in all_plans:
                        st.write(f"**{plan['Name']}:** {plan['Plan']}")
                else:
                    st.info("No upcoming plans")
            
            with col2:
                st.markdown("**🎯 Current Goals**")
                if all_goals:
                    for goal in all_goals:
                        st.write(f"**{goal['Name']}:** {goal['Goal']}")
                else:
                    st.info("No current goals")
        else:
            st.info("No sub profiles available")
    
    def _show_memory_management(self):
        """Show memory management interface"""
        st.subheader("🧠 Memory Management")
        
        # Memory aids and notes
        st.markdown("### 📝 Memory Aids & Notes")
        
        if self.sub_profiles:
            for profile_id, profile in self.sub_profiles.items():
                if profile["sir_notes"]["memory_aids"]:
                    with st.expander(f"🧠 {profile['basic_info']['name']} - Memory Aids"):
                        st.write(profile["sir_notes"]["memory_aids"])
        
        # Relationship tracking
        st.markdown("### 👥 Relationship Tracking")
        
        if self.sub_profiles:
            relationship_data = []
            for profile_id, profile in self.sub_profiles.items():
                relationship_data.append({
                    "Name": profile["basic_info"]["name"],
                    "Relationship Type": profile["relationship_dynamics"]["relationship_type"],
                    "Communication Style": profile["relationship_dynamics"]["communication_style"],
                    "Last Contact": profile["current_status"]["last_contact"],
                    "Status": profile["current_status"]["status"]
                })
            
            if relationship_data:
                df = pd.DataFrame(relationship_data)
                st.dataframe(df, use_container_width=True)
        
        # Memory update tools
        st.markdown("### 🔧 Memory Update Tools")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh All Profiles"):
                st.success("✅ All profiles refreshed")
        
        with col2:
            if st.button("📊 Generate Memory Report"):
                st.info("📊 Memory report generated")
        
        with col3:
            if st.button("🧠 Memory Training"):
                st.info("🧠 Memory training session started")
    
    def _log_briefing(self, action: str, profile_id: str, details: Dict = None):
        """Log briefing action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "profile_id": profile_id,
            "details": details or {}
        }
        self.briefing_history[profile_id] = log_entry
        logger.info(f"Briefing log: {action} for {profile_id}")

# Global Sir briefing instance
sir_briefing = SirBriefingSystem()

def show_sir_briefing_system():
    """Main Sir briefing system interface"""
    sir_briefing.show_sir_briefing_dashboard()
