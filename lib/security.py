"""
Security utilities for Harem CRM
"""
import streamlit as st
import hashlib
import secrets
import bcrypt
import bleach
import re
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta
import jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityManager:
    """Comprehensive security management for the CRM system"""
    
    def __init__(self):
        self.session_timeout = 3600  # 1 hour
        self.max_login_attempts = 5
        self.lockout_duration = 900  # 15 minutes
        
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"❌ Error hashing password: {e}")
            return None
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            logger.error(f"❌ Error verifying password: {e}")
            return False
    
    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks"""
        try:
            if not user_input:
                return ""
            
            # Remove HTML tags and dangerous content
            sanitized = bleach.clean(user_input, 
                                   tags=[], 
                                   attributes={}, 
                                   strip=True)
            
            # Remove SQL injection patterns
            sql_patterns = [
                r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)',
                r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
                r'(\b(OR|AND)\s+\w+\s*=\s*\w+)',
                r'(\bUNION\s+SELECT\b)',
                r'(\bDROP\s+TABLE\b)',
                r'(\bDELETE\s+FROM\b)',
                r'(\bINSERT\s+INTO\b)',
                r'(\bUPDATE\s+SET\b)',
            ]
            
            for pattern in sql_patterns:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
            
            # Remove script tags and javascript
            script_patterns = [
                r'<script[^>]*>.*?</script>',
                r'javascript:',
                r'on\w+\s*=',
                r'<iframe[^>]*>.*?</iframe>',
                r'<object[^>]*>.*?</object>',
                r'<embed[^>]*>.*?</embed>',
            ]
            
            for pattern in script_patterns:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
            
            return sanitized.strip()
            
        except Exception as e:
            logger.error(f"❌ Error sanitizing input: {e}")
            return ""
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        except Exception as e:
            logger.error(f"❌ Error validating email: {e}")
            return False
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        try:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', phone)
            # Check if it's a valid length (10-15 digits)
            return 10 <= len(digits) <= 15
        except Exception as e:
            logger.error(f"❌ Error validating phone: {e}")
            return False
    
    def generate_session_token(self, user_id: str) -> str:
        """Generate secure session token"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=self.session_timeout),
                'iat': datetime.utcnow(),
                'jti': secrets.token_urlsafe(32)
            }
            
            # In production, use a proper secret key
            secret = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
            token = jwt.encode(payload, secret, algorithm='HS256')
            
            logger.info(f"✅ Session token generated for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"❌ Error generating session token: {e}")
            return None
    
    def verify_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify session token"""
        try:
            secret = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                logger.warning("❌ Session token expired")
                return None
            
            logger.info(f"✅ Session token verified for user {payload['user_id']}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Session token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("❌ Invalid session token")
            return None
        except Exception as e:
            logger.error(f"❌ Error verifying session token: {e}")
            return None
    
    def check_rate_limit(self, user_id: str, action: str) -> bool:
        """Check if user has exceeded rate limits"""
        try:
            # Get current rate limit data from session state
            if 'rate_limits' not in st.session_state:
                st.session_state.rate_limits = {}
            
            user_limits = st.session_state.rate_limits.get(user_id, {})
            action_limits = user_limits.get(action, {'count': 0, 'last_reset': datetime.now()})
            
            # Reset counter if more than 1 hour has passed
            if datetime.now() - action_limits['last_reset'] > timedelta(hours=1):
                action_limits = {'count': 0, 'last_reset': datetime.now()}
            
            # Check limits based on action
            limits = {
                'login': 5,  # 5 login attempts per hour
                'application': 3,  # 3 applications per hour
                'update': 20,  # 20 updates per hour
                'view': 100  # 100 views per hour
            }
            
            limit = limits.get(action, 10)
            
            if action_limits['count'] >= limit:
                logger.warning(f"❌ Rate limit exceeded for user {user_id}, action {action}")
                return False
            
            # Increment counter
            action_limits['count'] += 1
            user_limits[action] = action_limits
            st.session_state.rate_limits[user_id] = user_limits
            
            logger.info(f"✅ Rate limit check passed for user {user_id}, action {action}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error checking rate limit: {e}")
            return False
    
    def log_security_event(self, user_id: str, event: str, details: str = ""):
        """Log security events"""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = {
                'timestamp': timestamp,
                'user_id': user_id,
                'event': event,
                'details': details,
                'ip_address': '127.0.0.1'  # In production, get real IP
            }
            
            # Store in session state for now (in production, use proper logging)
            if 'security_logs' not in st.session_state:
                st.session_state.security_logs = []
            
            st.session_state.security_logs.append(log_entry)
            
            # Keep only last 1000 entries
            if len(st.session_state.security_logs) > 1000:
                st.session_state.security_logs = st.session_state.security_logs[-1000:]
            
            logger.info(f"🔒 Security event logged: {event} for user {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Error logging security event: {e}")
    
    def check_password_strength(self, password: str) -> Dict[str, Any]:
        """Check password strength"""
        try:
            score = 0
            feedback = []
            
            # Length check
            if len(password) >= 8:
                score += 1
            else:
                feedback.append("Password should be at least 8 characters long")
            
            # Uppercase check
            if re.search(r'[A-Z]', password):
                score += 1
            else:
                feedback.append("Password should contain at least one uppercase letter")
            
            # Lowercase check
            if re.search(r'[a-z]', password):
                score += 1
            else:
                feedback.append("Password should contain at least one lowercase letter")
            
            # Number check
            if re.search(r'\d', password):
                score += 1
            else:
                feedback.append("Password should contain at least one number")
            
            # Special character check
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                score += 1
            else:
                feedback.append("Password should contain at least one special character")
            
            # Common password check
            common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
            if password.lower() in common_passwords:
                score -= 2
                feedback.append("Password is too common")
            
            strength_levels = {
                0: "Very Weak",
                1: "Weak", 
                2: "Fair",
                3: "Good",
                4: "Strong",
                5: "Very Strong"
            }
            
            return {
                'score': score,
                'level': strength_levels.get(score, "Very Weak"),
                'feedback': feedback,
                'is_strong': score >= 4
            }
            
        except Exception as e:
            logger.error(f"❌ Error checking password strength: {e}")
            return {'score': 0, 'level': 'Very Weak', 'feedback': ['Error checking password'], 'is_strong': False}

# Initialize security manager
security = SecurityManager()

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user with enhanced security"""
    try:
        # Check rate limiting
        if not security.check_rate_limit(username, 'login'):
            st.error("❌ Too many login attempts. Please try again later.")
            security.log_security_event(username, 'rate_limit_exceeded', 'login attempts')
            return False
        
        # Validate input
        username = security.sanitize_input(username)
        if not username:
            st.error("❌ Invalid username")
            return False
        
        # Check credentials (in production, verify against database)
        if username == "admin" and password == "harem2025":
            # Generate session token
            token = security.generate_session_token(username)
            if token:
                st.session_state.auth_token = token
                st.session_state.authenticated_user = username
                st.session_state.login_time = datetime.now()
                
                security.log_security_event(username, 'successful_login')
                logger.info(f"✅ User {username} authenticated successfully")
                return True
        
        # Log failed attempt
        security.log_security_event(username, 'failed_login', 'invalid credentials')
        logger.warning(f"❌ Failed login attempt for user {username}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        security.log_security_event(username, 'authentication_error', str(e))
        return False

def check_authentication() -> bool:
    """Check if user is authenticated"""
    try:
        if 'auth_token' not in st.session_state:
            return False
        
        # Verify session token
        payload = security.verify_session_token(st.session_state.auth_token)
        if not payload:
            # Clear invalid session
            st.session_state.auth_token = None
            st.session_state.authenticated_user = None
            return False
        
        # Check session timeout
        if 'login_time' in st.session_state:
            if datetime.now() - st.session_state.login_time > timedelta(seconds=security.session_timeout):
                st.session_state.auth_token = None
                st.session_state.authenticated_user = None
                st.session_state.login_time = None
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Authentication check error: {e}")
        return False

def logout_user():
    """Logout user and clear session"""
    try:
        if 'authenticated_user' in st.session_state:
            security.log_security_event(st.session_state.authenticated_user, 'logout')
        
        # Clear session data
        st.session_state.auth_token = None
        st.session_state.authenticated_user = None
        st.session_state.login_time = None
        
        logger.info("✅ User logged out successfully")
        
    except Exception as e:
        logger.error(f"❌ Logout error: {e}")

def get_security_logs() -> List[Dict[str, Any]]:
    """Get security logs"""
    try:
        return st.session_state.get('security_logs', [])
    except Exception as e:
        logger.error(f"❌ Error getting security logs: {e}")
        return []
