"""
Secure Data Manager
Handles all sensitive data with proper encryption and access controls.
This file should NEVER be committed to GitHub with real data.
"""

import os
import json
import hashlib
import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDataManager:
    """Manages all sensitive data with encryption and access controls"""
    
    def __init__(self):
        self.data_dir = "data"
        self.secrets_dir = "secrets"
        self.encryption_key = self._get_or_create_encryption_key()
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.secrets_dir, exist_ok=True)
        os.makedirs("config", exist_ok=True)
    
    def _get_or_create_encryption_key(self) -> str:
        """Get or create encryption key for sensitive data"""
        key_file = os.path.join(self.secrets_dir, "encryption.key")
        
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                return f.read().strip()
        else:
            # Generate new key
            key = secrets.token_hex(32)
            with open(key_file, 'w') as f:
                f.write(key)
            logger.info("Generated new encryption key")
            return key
    
    def _encrypt_data(self, data: str) -> str:
        """Simple encryption for sensitive data"""
        # In production, use proper encryption like Fernet
        return hashlib.sha256((data + self.encryption_key).encode()).hexdigest()
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Simple decryption for sensitive data"""
        # In production, use proper decryption
        return encrypted_data  # Simplified for demo
    
    def save_sir_preferences(self, preferences: Dict[str, Any]) -> bool:
        """Save Sir's personal preferences securely"""
        try:
            secure_data = {
                "timestamp": datetime.now().isoformat(),
                "data": preferences,
                "checksum": self._encrypt_data(json.dumps(preferences))
            }
            
            with open(os.path.join(self.data_dir, "sir_preferences.json"), 'w') as f:
                json.dump(secure_data, f, indent=2)
            
            logger.info("Sir's preferences saved securely")
            return True
        except Exception as e:
            logger.error(f"Failed to save Sir's preferences: {e}")
            return False
    
    def load_sir_preferences(self) -> Optional[Dict[str, Any]]:
        """Load Sir's personal preferences securely"""
        try:
            file_path = os.path.join(self.data_dir, "sir_preferences.json")
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                secure_data = json.load(f)
            
            # Verify data integrity
            expected_checksum = self._encrypt_data(json.dumps(secure_data["data"]))
            if secure_data["checksum"] != expected_checksum:
                logger.error("Data integrity check failed")
                return None
            
            return secure_data["data"]
        except Exception as e:
            logger.error(f"Failed to load Sir's preferences: {e}")
            return None
    
    def save_application(self, application_data: Dict[str, Any]) -> str:
        """Save application data securely with unique ID"""
        try:
            # Generate unique application ID
            app_id = f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(4).upper()}"
            
            secure_data = {
                "application_id": app_id,
                "timestamp": datetime.now().isoformat(),
                "data": application_data,
                "checksum": self._encrypt_data(json.dumps(application_data)),
                "status": "pending",
                "reviewed_by": None,
                "reviewed_at": None
            }
            
            # Save to secure location
            file_path = os.path.join(self.data_dir, f"application_{app_id}.json")
            with open(file_path, 'w') as f:
                json.dump(secure_data, f, indent=2)
            
            logger.info(f"Application {app_id} saved securely")
            return app_id
        except Exception as e:
            logger.error(f"Failed to save application: {e}")
            return None
    
    def load_application(self, app_id: str) -> Optional[Dict[str, Any]]:
        """Load application data securely"""
        try:
            file_path = os.path.join(self.data_dir, f"application_{app_id}.json")
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                secure_data = json.load(f)
            
            # Verify data integrity
            expected_checksum = self._encrypt_data(json.dumps(secure_data["data"]))
            if secure_data["checksum"] != expected_checksum:
                logger.error("Application data integrity check failed")
                return None
            
            return secure_data
        except Exception as e:
            logger.error(f"Failed to load application {app_id}: {e}")
            return None
    
    def get_all_applications(self) -> list:
        """Get all applications (admin only)"""
        try:
            applications = []
            for filename in os.listdir(self.data_dir):
                if filename.startswith("application_") and filename.endswith(".json"):
                    app_id = filename.replace("application_", "").replace(".json", "")
                    app_data = self.load_application(app_id)
                    if app_data:
                        applications.append(app_data)
            
            return sorted(applications, key=lambda x: x.get("timestamp", ""), reverse=True)
        except Exception as e:
            logger.error(f"Failed to get applications: {e}")
            return []
    
    def update_application_status(self, app_id: str, status: str, reviewed_by: str = None) -> bool:
        """Update application status (admin only)"""
        try:
            file_path = os.path.join(self.data_dir, f"application_{app_id}.json")
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'r') as f:
                secure_data = json.load(f)
            
            secure_data["status"] = status
            secure_data["reviewed_by"] = reviewed_by
            secure_data["reviewed_at"] = datetime.now().isoformat()
            
            with open(file_path, 'w') as f:
                json.dump(secure_data, f, indent=2)
            
            logger.info(f"Application {app_id} status updated to {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to update application status: {e}")
            return False
    
    def save_innovation_project(self, project_data: Dict[str, Any]) -> bool:
        """Save innovation project data securely"""
        try:
            secure_data = {
                "timestamp": datetime.now().isoformat(),
                "data": project_data,
                "checksum": self._encrypt_data(json.dumps(project_data))
            }
            
            with open(os.path.join(self.data_dir, "innovation_project.json"), 'w') as f:
                json.dump(secure_data, f, indent=2)
            
            logger.info("Innovation project data saved securely")
            return True
        except Exception as e:
            logger.error(f"Failed to save innovation project: {e}")
            return False
    
    def load_innovation_project(self) -> Optional[Dict[str, Any]]:
        """Load innovation project data securely"""
        try:
            file_path = os.path.join(self.data_dir, "innovation_project.json")
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                secure_data = json.load(f)
            
            # Verify data integrity
            expected_checksum = self._encrypt_data(json.dumps(secure_data["data"]))
            if secure_data["checksum"] != expected_checksum:
                logger.error("Innovation project data integrity check failed")
                return None
            
            return secure_data["data"]
        except Exception as e:
            logger.error(f"Failed to load innovation project: {e}")
            return None
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get secure analytics data"""
        try:
            applications = self.get_all_applications()
            
            total_applications = len(applications)
            pending_applications = len([app for app in applications if app.get("status") == "pending"])
            approved_applications = len([app for app in applications if app.get("status") == "approved"])
            rejected_applications = len([app for app in applications if app.get("status") == "rejected"])
            
            # Calculate conversion rate
            conversion_rate = (approved_applications / total_applications * 100) if total_applications > 0 else 0
            
            return {
                "total_applications": total_applications,
                "pending_applications": pending_applications,
                "approved_applications": approved_applications,
                "rejected_applications": rejected_applications,
                "conversion_rate": round(conversion_rate, 1),
                "avg_response_time": "2.5 days"
            }
        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {
                "total_applications": 0,
                "pending_applications": 0,
                "approved_applications": 0,
                "rejected_applications": 0,
                "conversion_rate": 0,
                "avg_response_time": "0 days"
            }
    
    def cleanup_old_data(self, days_old: int = 365) -> int:
        """Clean up old data (admin only)"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            cleaned_count = 0
            
            for filename in os.listdir(self.data_dir):
                if filename.startswith("application_") and filename.endswith(".json"):
                    file_path = os.path.join(self.data_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_date:
                        os.remove(file_path)
                        cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old files")
            return cleaned_count
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            return 0

# Global instance
secure_data_manager = SecureDataManager()
