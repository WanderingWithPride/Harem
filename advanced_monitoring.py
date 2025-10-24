"""
Advanced Monitoring and Alerting System
Implements comprehensive monitoring, alerting, and performance tracking for the Harem CRM system.
"""

import streamlit as st
import time
import psutil
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedMonitoring:
    """Advanced monitoring and alerting system"""
    
    def __init__(self):
        self.metrics = {
            'performance': [],
            'errors': [],
            'alerts': [],
            'user_activity': [],
            'system_health': []
        }
        self.alert_thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'response_time': 5.0,
            'error_rate': 5.0,
            'disk_usage': 90
        }
        self.monitoring_active = False
        self.alert_queue = queue.Queue()
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            monitoring_thread = threading.Thread(target=self._monitoring_loop)
            monitoring_thread.daemon = True
            monitoring_thread.start()
            logger.info("Advanced monitoring started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        logger.info("Advanced monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                self.metrics['system_health'].append(system_metrics)
                
                # Check for alerts
                self._check_alerts(system_metrics)
                
                # Clean old metrics (keep last 1000 entries)
                for metric_type in self.metrics:
                    if len(self.metrics[metric_type]) > 1000:
                        self.metrics[metric_type] = self.metrics[metric_type][-1000:]
                
                time.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _collect_system_metrics(self) -> Dict:
        """Collect system performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available,
                'disk_usage': disk.percent,
                'disk_free': disk.free,
                'process_count': len(psutil.pids()),
                'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
            }
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': 0,
                'memory_usage': 0,
                'memory_available': 0,
                'disk_usage': 0,
                'disk_free': 0,
                'process_count': 0,
                'load_average': [0, 0, 0]
            }
    
    def _check_alerts(self, metrics: Dict):
        """Check for alert conditions"""
        alerts = []
        
        # CPU usage alert
        if metrics['cpu_usage'] > self.alert_thresholds['cpu_usage']:
            alerts.append({
                'type': 'cpu_usage',
                'severity': 'warning',
                'message': f"High CPU usage: {metrics['cpu_usage']:.1f}%",
                'timestamp': datetime.now().isoformat(),
                'value': metrics['cpu_usage'],
                'threshold': self.alert_thresholds['cpu_usage']
            })
        
        # Memory usage alert
        if metrics['memory_usage'] > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'memory_usage',
                'severity': 'warning',
                'message': f"High memory usage: {metrics['memory_usage']:.1f}%",
                'timestamp': datetime.now().isoformat(),
                'value': metrics['memory_usage'],
                'threshold': self.alert_thresholds['memory_usage']
            })
        
        # Disk usage alert
        if metrics['disk_usage'] > self.alert_thresholds['disk_usage']:
            alerts.append({
                'type': 'disk_usage',
                'severity': 'critical',
                'message': f"High disk usage: {metrics['disk_usage']:.1f}%",
                'timestamp': datetime.now().isoformat(),
                'value': metrics['disk_usage'],
                'threshold': self.alert_thresholds['disk_usage']
            })
        
        # Add alerts to queue
        for alert in alerts:
            self.metrics['alerts'].append(alert)
            self.alert_queue.put(alert)
            logger.warning(f"Alert: {alert['message']}")
    
    def track_performance(self, operation: str, duration: float, success: bool = True):
        """Track operation performance"""
        performance_data = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'duration': duration,
            'success': success
        }
        
        self.metrics['performance'].append(performance_data)
        
        # Check for performance alerts
        if duration > self.alert_thresholds['response_time']:
            alert = {
                'type': 'performance',
                'severity': 'warning',
                'message': f"Slow operation: {operation} took {duration:.2f}s",
                'timestamp': datetime.now().isoformat(),
                'operation': operation,
                'duration': duration,
                'threshold': self.alert_thresholds['response_time']
            }
            self.metrics['alerts'].append(alert)
            self.alert_queue.put(alert)
    
    def track_error(self, error_type: str, error_message: str, context: str = ""):
        """Track application errors"""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'error_message': error_message,
            'context': context
        }
        
        self.metrics['errors'].append(error_data)
        
        # Check error rate
        recent_errors = [e for e in self.metrics['errors'] 
                        if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(minutes=5)]
        
        if len(recent_errors) > 10:  # More than 10 errors in 5 minutes
            alert = {
                'type': 'error_rate',
                'severity': 'critical',
                'message': f"High error rate: {len(recent_errors)} errors in 5 minutes",
                'timestamp': datetime.now().isoformat(),
                'error_count': len(recent_errors)
            }
            self.metrics['alerts'].append(alert)
            self.alert_queue.put(alert)
    
    def track_user_activity(self, user_id: str, action: str, details: Dict = None):
        """Track user activity"""
        activity_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'action': action,
            'details': details or {}
        }
        
        self.metrics['user_activity'].append(activity_data)
        logger.info(f"User activity: {user_id} - {action}")
    
    def show_monitoring_dashboard(self):
        """Display monitoring dashboard"""
        st.markdown("# 📊 Advanced Monitoring Dashboard")
        
        # System health overview
        self._show_system_health()
        
        # Performance metrics
        self._show_performance_metrics()
        
        # Error tracking
        self._show_error_tracking()
        
        # Alerts
        self._show_alerts()
        
        # User activity
        self._show_user_activity()
    
    def _show_system_health(self):
        """Show system health metrics"""
        st.markdown("### 🖥️ System Health")
        
        if self.metrics['system_health']:
            latest_metrics = self.metrics['system_health'][-1]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                cpu_usage = latest_metrics['cpu_usage']
                st.metric("CPU Usage", f"{cpu_usage:.1f}%", 
                         delta=f"{cpu_usage - self.alert_thresholds['cpu_usage']:.1f}%" if cpu_usage > self.alert_thresholds['cpu_usage'] else None)
            
            with col2:
                memory_usage = latest_metrics['memory_usage']
                st.metric("Memory Usage", f"{memory_usage:.1f}%",
                         delta=f"{memory_usage - self.alert_thresholds['memory_usage']:.1f}%" if memory_usage > self.alert_thresholds['memory_usage'] else None)
            
            with col3:
                disk_usage = latest_metrics['disk_usage']
                st.metric("Disk Usage", f"{disk_usage:.1f}%",
                         delta=f"{disk_usage - self.alert_thresholds['disk_usage']:.1f}%" if disk_usage > self.alert_thresholds['disk_usage'] else None)
            
            with col4:
                process_count = latest_metrics['process_count']
                st.metric("Process Count", str(process_count))
            
            # System health chart
            if len(self.metrics['system_health']) > 1:
                st.markdown("**System Health Over Time**")
                chart_data = {
                    'CPU Usage': [m['cpu_usage'] for m in self.metrics['system_health'][-20:]],
                    'Memory Usage': [m['memory_usage'] for m in self.metrics['system_health'][-20:]],
                    'Disk Usage': [m['disk_usage'] for m in self.metrics['system_health'][-20:]]
                }
                st.line_chart(chart_data)
        else:
            st.info("No system health data available.")
    
    def _show_performance_metrics(self):
        """Show performance metrics"""
        st.markdown("### ⚡ Performance Metrics")
        
        if self.metrics['performance']:
            # Calculate performance statistics
            durations = [p['duration'] for p in self.metrics['performance']]
            avg_duration = sum(durations) / len(durations)
            max_duration = max(durations)
            min_duration = min(durations)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Average Response Time", f"{avg_duration:.2f}s")
            
            with col2:
                st.metric("Max Response Time", f"{max_duration:.2f}s")
            
            with col3:
                st.metric("Min Response Time", f"{min_duration:.2f}s")
            
            with col4:
                success_rate = sum(1 for p in self.metrics['performance'] if p['success']) / len(self.metrics['performance'])
                st.metric("Success Rate", f"{success_rate:.1%}")
            
            # Performance chart
            st.markdown("**Performance Over Time**")
            chart_data = {
                'Response Time': [p['duration'] for p in self.metrics['performance'][-20:]]
            }
            st.line_chart(chart_data)
        else:
            st.info("No performance data available.")
    
    def _show_error_tracking(self):
        """Show error tracking"""
        st.markdown("### 🐛 Error Tracking")
        
        if self.metrics['errors']:
            # Error statistics
            error_types = {}
            for error in self.metrics['errors']:
                error_type = error['error_type']
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Error Types**")
                for error_type, count in error_types.items():
                    st.write(f"• {error_type}: {count}")
            
            with col2:
                st.markdown("**Recent Errors**")
                for error in self.metrics['errors'][-5:]:
                    st.write(f"• {error['error_type']}: {error['error_message']}")
        else:
            st.info("No errors recorded.")
    
    def _show_alerts(self):
        """Show alerts"""
        st.markdown("### 🚨 Alerts")
        
        if self.metrics['alerts']:
            # Group alerts by severity
            critical_alerts = [a for a in self.metrics['alerts'] if a['severity'] == 'critical']
            warning_alerts = [a for a in self.metrics['alerts'] if a['severity'] == 'warning']
            
            if critical_alerts:
                st.error(f"**Critical Alerts ({len(critical_alerts)})**")
                for alert in critical_alerts[-5:]:
                    st.error(f"🔴 {alert['message']} - {alert['timestamp']}")
            
            if warning_alerts:
                st.warning(f"**Warning Alerts ({len(warning_alerts)})**")
                for alert in warning_alerts[-5:]:
                    st.warning(f"🟡 {alert['message']} - {alert['timestamp']}")
        else:
            st.success("✅ No active alerts.")
    
    def _show_user_activity(self):
        """Show user activity"""
        st.markdown("### 👥 User Activity")
        
        if self.metrics['user_activity']:
            # Recent activity
            recent_activity = self.metrics['user_activity'][-10:]
            
            for activity in recent_activity:
                st.write(f"• {activity['user_id']}: {activity['action']} - {activity['timestamp']}")
        else:
            st.info("No user activity recorded.")
    
    def show_alert_settings(self):
        """Show alert configuration"""
        st.markdown("### ⚙️ Alert Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Performance Thresholds**")
            cpu_threshold = st.slider("CPU Usage Alert (%)", 0, 100, self.alert_thresholds['cpu_usage'])
            memory_threshold = st.slider("Memory Usage Alert (%)", 0, 100, self.alert_thresholds['memory_usage'])
            response_threshold = st.slider("Response Time Alert (s)", 0.0, 10.0, self.alert_thresholds['response_time'])
        
        with col2:
            st.markdown("**System Thresholds**")
            disk_threshold = st.slider("Disk Usage Alert (%)", 0, 100, self.alert_thresholds['disk_usage'])
            error_rate_threshold = st.slider("Error Rate Alert (%)", 0.0, 20.0, self.alert_thresholds['error_rate'])
        
        if st.button("💾 Save Alert Settings"):
            self.alert_thresholds.update({
                'cpu_usage': cpu_threshold,
                'memory_usage': memory_threshold,
                'response_time': response_threshold,
                'disk_usage': disk_threshold,
                'error_rate': error_rate_threshold
            })
            st.success("✅ Alert settings saved!")

# Global monitoring instance
advanced_monitoring = AdvancedMonitoring()

def show_advanced_monitoring():
    """Main advanced monitoring interface"""
    st.markdown("# 📊 Advanced Monitoring & Alerting")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Performance", "Alerts", "Settings"])
    
    with tab1:
        advanced_monitoring.show_monitoring_dashboard()
    
    with tab2:
        advanced_monitoring._show_performance_metrics()
    
    with tab3:
        advanced_monitoring._show_alerts()
    
    with tab4:
        advanced_monitoring.show_alert_settings()
