"""
Enhanced Error Handling and User Feedback Module
Implements comprehensive error handling, user feedback, and monitoring for the Harem CRM system.
"""

import streamlit as st
import logging
import traceback
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
import functools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Enhanced error handling and user feedback system"""
    
    def __init__(self):
        self.error_logs = []
        self.user_feedback = []
        self.performance_metrics = []
    
    def handle_error(self, error: Exception, context: str = "", user_message: str = ""):
        """Handle errors with user-friendly messages and logging"""
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Log error details
        error_details = {
            'error_id': error_id,
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'traceback': traceback.format_exc(),
            'user_message': user_message
        }
        
        self.error_logs.append(error_details)
        logger.error(f"Error {error_id}: {error}")
        
        # Show user-friendly error message
        self.show_error_to_user(error_id, user_message or self._get_user_friendly_message(error))
        
        return error_id
    
    def _get_user_friendly_message(self, error: Exception) -> str:
        """Get user-friendly error message based on error type"""
        error_messages = {
            'ConnectionError': "🔌 Connection issue. Please check your internet connection and try again.",
            'TimeoutError': "⏰ Request timed out. Please try again in a moment.",
            'ValueError': "📝 Invalid input. Please check your data and try again.",
            'PermissionError': "🔒 Access denied. You don't have permission to perform this action.",
            'FileNotFoundError': "📁 File not found. Please check the file path and try again.",
            'KeyError': "🔑 Missing information. Please ensure all required fields are filled.",
            'TypeError': "⚙️ System error. Please try again or contact support if the issue persists.",
            'AttributeError': "🔧 System error. Please refresh the page and try again.",
            'ImportError': "📦 System error. Please refresh the page and try again.",
            'RuntimeError': "⚡ System error. Please try again or contact support if the issue persists."
        }
        
        error_type = type(error).__name__
        return error_messages.get(error_type, "❌ An unexpected error occurred. Please try again or contact support.")
    
    def show_error_to_user(self, error_id: str, message: str):
        """Display error message to user"""
        st.error(f"**Error {error_id}**")
        st.error(message)
        
        # Show error details in expander for debugging
        with st.expander("🔍 Error Details (for debugging)"):
            st.code(f"Error ID: {error_id}")
            st.code(f"Timestamp: {datetime.now().isoformat()}")
            st.code(f"Message: {message}")
            
            if st.button("📋 Copy Error ID", key=f"copy_{error_id}"):
                st.write("Error ID copied to clipboard!")
    
    def show_success_message(self, message: str, details: str = ""):
        """Show success message to user"""
        st.success(f"✅ {message}")
        
        if details:
            with st.expander("📋 Details"):
                st.write(details)
    
    def show_warning_message(self, message: str, details: str = ""):
        """Show warning message to user"""
        st.warning(f"⚠️ {message}")
        
        if details:
            with st.expander("📋 Details"):
                st.write(details)
    
    def show_info_message(self, message: str, details: str = ""):
        """Show info message to user"""
        st.info(f"ℹ️ {message}")
        
        if details:
            with st.expander("📋 Details"):
                st.write(details)
    
    def show_loading_state(self, message: str = "Loading..."):
        """Show loading state"""
        with st.spinner(message):
            pass
    
    def show_progress_bar(self, progress: float, message: str = "Processing..."):
        """Show progress bar"""
        st.progress(progress)
        st.write(f"{message} ({progress:.0%})")
    
    def collect_user_feedback(self, feedback_type: str, rating: int, comment: str = ""):
        """Collect user feedback"""
        feedback = {
            'timestamp': datetime.now().isoformat(),
            'type': feedback_type,
            'rating': rating,
            'comment': comment,
            'user_agent': st.session_state.get('user_agent', 'unknown')
        }
        
        self.user_feedback.append(feedback)
        logger.info(f"User feedback collected: {feedback}")
        
        return feedback
    
    def show_feedback_form(self, feedback_type: str = "general"):
        """Show feedback collection form"""
        st.markdown("### 📝 Feedback Form")
        
        with st.form("feedback_form"):
            st.markdown(f"**{feedback_type.title()} Feedback**")
            
            # Rating
            rating = st.slider("Rating", 1, 5, 3, help="Rate your experience (1 = Poor, 5 = Excellent)")
            
            # Comment
            comment = st.text_area("Comments", placeholder="Share your thoughts, suggestions, or issues...")
            
            # Submit feedback
            if st.form_submit_button("📤 Submit Feedback"):
                feedback = self.collect_user_feedback(feedback_type, rating, comment)
                
                if rating >= 4:
                    st.success("✅ Thank you for your positive feedback!")
                elif rating >= 3:
                    st.info("👍 Thank you for your feedback!")
                else:
                    st.warning("⚠️ We're sorry for the poor experience. We'll work to improve.")
    
    def show_error_reporting(self):
        """Show error reporting interface"""
        st.markdown("### 🐛 Error Reporting")
        
        if self.error_logs:
            st.markdown(f"**Recent Errors ({len(self.error_logs)})**")
            
            for error in self.error_logs[-5:]:  # Show last 5 errors
                with st.expander(f"Error {error['error_id']} - {error['error_type']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Timestamp:** {error['timestamp']}")
                        st.write(f"**Context:** {error['context']}")
                        st.write(f"**Message:** {error['user_message']}")
                    
                    with col2:
                        st.code(f"Error Type: {error['error_type']}")
                        st.code(f"Error Message: {error['error_message']}")
                        
                        if st.button("📋 Copy Error Details", key=f"copy_error_{error['error_id']}"):
                            st.write("Error details copied to clipboard!")
        else:
            st.info("No errors recorded.")
    
    def show_performance_metrics(self):
        """Show performance metrics"""
        st.markdown("### 📊 Performance Metrics")
        
        if self.performance_metrics:
            # Calculate average performance
            avg_response_time = sum(m['response_time'] for m in self.performance_metrics) / len(self.performance_metrics)
            avg_memory_usage = sum(m['memory_usage'] for m in self.performance_metrics) / len(self.performance_metrics)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Average Response Time", f"{avg_response_time:.2f}s")
            
            with col2:
                st.metric("Average Memory Usage", f"{avg_memory_usage:.2f}MB")
            
            with col3:
                st.metric("Total Requests", len(self.performance_metrics))
            
            # Performance chart
            st.markdown("**Performance Over Time**")
            st.line_chart([m['response_time'] for m in self.performance_metrics])
        else:
            st.info("No performance data available.")
    
    def track_performance(self, operation: str, start_time: float, end_time: float, memory_usage: float = 0):
        """Track performance metrics"""
        performance_data = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'response_time': end_time - start_time,
            'memory_usage': memory_usage
        }
        
        self.performance_metrics.append(performance_data)
        logger.info(f"Performance tracked: {performance_data}")

# Global error handler instance
error_handler = ErrorHandler()

def error_boundary(func: Callable) -> Callable:
    """Decorator for error boundary functionality"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_error(e, f"Function: {func.__name__}")
            return None
    return wrapper

def with_loading_state(message: str = "Loading..."):
    """Decorator for loading state"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def with_error_handling(context: str = ""):
    """Decorator for error handling"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_error(e, context or f"Function: {func.__name__}")
                return None
        return wrapper
    return decorator

def show_enhanced_error_handling():
    """Main enhanced error handling interface"""
    st.markdown("# 🛠️ Enhanced Error Handling & User Feedback")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Error Reporting", "User Feedback", "Performance", "Settings"])
    
    with tab1:
        error_handler.show_error_reporting()
    
    with tab2:
        error_handler.show_feedback_form("system")
    
    with tab3:
        error_handler.show_performance_metrics()
    
    with tab4:
        st.markdown("### ⚙️ Error Handling Settings")
        
        # Error reporting settings
        st.checkbox("Enable Error Reporting", value=True, help="Automatically report errors for debugging")
        st.checkbox("Show Error Details", value=False, help="Show technical error details to users")
        st.checkbox("Log Performance Metrics", value=True, help="Track performance metrics")
        
        # Notification settings
        st.checkbox("Email Error Notifications", value=False, help="Send email notifications for critical errors")
        st.checkbox("Slack Notifications", value=False, help="Send Slack notifications for errors")
        
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved!")

# Example usage functions
@error_boundary
def example_function_with_error_handling():
    """Example function with error handling"""
    # This function will automatically handle errors
    result = 1 / 0  # This will cause an error
    return result

@with_loading_state("Processing data...")
def example_function_with_loading():
    """Example function with loading state"""
    import time
    time.sleep(2)  # Simulate processing
    return "Processing complete!"

@with_error_handling("Data processing")
def example_function_with_context():
    """Example function with error context"""
    # This function will show context-specific error messages
    data = {"key": "value"}
    return data["missing_key"]  # This will cause an error
