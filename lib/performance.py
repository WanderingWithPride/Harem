"""
Performance optimization utilities for Harem CRM
"""
import streamlit as st
import time
import logging
from typing import Any, Callable, Dict, List
from functools import wraps
import pandas as pd
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and optimize application performance"""
    
    def __init__(self):
        self.metrics = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
    def track_performance(self, func_name: str, execution_time: float):
        """Track function execution time"""
        try:
            if func_name not in self.metrics:
                self.metrics[func_name] = {
                    'total_time': 0,
                    'call_count': 0,
                    'avg_time': 0,
                    'max_time': 0,
                    'min_time': float('inf')
                }
            
            metrics = self.metrics[func_name]
            metrics['total_time'] += execution_time
            metrics['call_count'] += 1
            metrics['avg_time'] = metrics['total_time'] / metrics['call_count']
            metrics['max_time'] = max(metrics['max_time'], execution_time)
            metrics['min_time'] = min(metrics['min_time'], execution_time)
            
            logger.info(f"⏱️ {func_name}: {execution_time:.3f}s (avg: {metrics['avg_time']:.3f}s)")
            
        except Exception as e:
            logger.error(f"❌ Error tracking performance: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            summary = {
                'total_functions': len(self.metrics),
                'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
                'slowest_functions': [],
                'most_called_functions': []
            }
            
            # Find slowest functions
            for func_name, metrics in self.metrics.items():
                if metrics['avg_time'] > 1.0:  # Functions taking more than 1 second
                    summary['slowest_functions'].append({
                        'function': func_name,
                        'avg_time': metrics['avg_time'],
                        'max_time': metrics['max_time'],
                        'call_count': metrics['call_count']
                    })
            
            # Find most called functions
            for func_name, metrics in self.metrics.items():
                if metrics['call_count'] > 10:  # Functions called more than 10 times
                    summary['most_called_functions'].append({
                        'function': func_name,
                        'call_count': metrics['call_count'],
                        'avg_time': metrics['avg_time']
                    })
            
            # Sort by performance impact
            summary['slowest_functions'].sort(key=lambda x: x['avg_time'], reverse=True)
            summary['most_called_functions'].sort(key=lambda x: x['call_count'], reverse=True)
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error getting performance summary: {e}")
            return {}
    
    def record_cache_hit(self):
        """Record cache hit"""
        self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        self.cache_misses += 1

# Initialize performance monitor
performance_monitor = PerformanceMonitor()

def performance_timer(func_name: str = None):
    """Decorator to time function execution"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                performance_monitor.track_performance(func_name or func.__name__, execution_time)
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                performance_monitor.track_performance(func_name or func.__name__, execution_time)
                raise e
        return wrapper
    return decorator

@st.cache_data(ttl=300)  # Cache for 5 minutes
@performance_timer("get_applications_cached")
def get_applications_cached() -> List[Dict[str, Any]]:
    """Get applications with caching"""
    try:
        from .database import get_applications
        performance_monitor.record_cache_hit()
        return get_applications()
    except Exception as e:
        performance_monitor.record_cache_miss()
        logger.error(f"❌ Error getting cached applications: {e}")
        return []

@st.cache_data(ttl=300)
@performance_timer("get_users_cached")
def get_users_cached() -> List[Dict[str, Any]]:
    """Get users with caching"""
    try:
        from .database import get_users
        performance_monitor.record_cache_hit()
        return get_users()
    except Exception as e:
        performance_monitor.record_cache_miss()
        logger.error(f"❌ Error getting cached users: {e}")
        return []

@st.cache_data(ttl=300)
@performance_timer("get_analytics_cached")
def get_analytics_cached() -> Dict[str, Any]:
    """Get analytics with caching"""
    try:
        from .database import get_analytics
        performance_monitor.record_cache_hit()
        return get_analytics()
    except Exception as e:
        performance_monitor.record_cache_miss()
        logger.error(f"❌ Error getting cached analytics: {e}")
        return {}

def optimize_dataframe(df: pd.DataFrame, max_rows: int = 1000) -> pd.DataFrame:
    """Optimize DataFrame for display"""
    try:
        # Limit rows for performance
        if len(df) > max_rows:
            df = df.head(max_rows)
            logger.info(f"📊 DataFrame optimized: limited to {max_rows} rows")
        
        # Optimize data types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error optimizing DataFrame: {e}")
        return df

def paginate_data(data: List[Dict[str, Any]], page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """Paginate data for better performance"""
    try:
        total_items = len(data)
        total_pages = (total_items + page_size - 1) // page_size
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_data = data[start_idx:end_idx]
        
        return {
            'data': paginated_data,
            'page': page,
            'page_size': page_size,
            'total_items': total_items,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
        
    except Exception as e:
        logger.error(f"❌ Error paginating data: {e}")
        return {
            'data': data,
            'page': 1,
            'page_size': len(data),
            'total_items': len(data),
            'total_pages': 1,
            'has_next': False,
            'has_prev': False
        }

def clear_cache():
    """Clear all cached data"""
    try:
        st.cache_data.clear()
        logger.info("✅ Cache cleared successfully")
    except Exception as e:
        logger.error(f"❌ Error clearing cache: {e}")

def get_cache_info() -> Dict[str, Any]:
    """Get cache information"""
    try:
        return {
            'cache_hits': performance_monitor.cache_hits,
            'cache_misses': performance_monitor.cache_misses,
            'cache_hit_rate': performance_monitor.cache_hits / (performance_monitor.cache_hits + performance_monitor.cache_misses) if (performance_monitor.cache_hits + performance_monitor.cache_misses) > 0 else 0
        }
    except Exception as e:
        logger.error(f"❌ Error getting cache info: {e}")
        return {}

def show_performance_dashboard():
    """Show performance monitoring dashboard"""
    try:
        st.subheader("📊 Performance Monitoring")
        
        # Performance summary
        summary = performance_monitor.get_performance_summary()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Functions", summary.get('total_functions', 0))
        
        with col2:
            cache_info = get_cache_info()
            st.metric("Cache Hit Rate", f"{cache_info.get('cache_hit_rate', 0):.1%}")
        
        with col3:
            st.metric("Cache Hits", cache_info.get('cache_hits', 0))
        
        # Slowest functions
        if summary.get('slowest_functions'):
            st.subheader("🐌 Slowest Functions")
            for func in summary['slowest_functions'][:5]:
                st.write(f"**{func['function']}**: {func['avg_time']:.3f}s avg ({func['call_count']} calls)")
        
        # Most called functions
        if summary.get('most_called_functions'):
            st.subheader("📞 Most Called Functions")
            for func in summary['most_called_functions'][:5]:
                st.write(f"**{func['function']}**: {func['call_count']} calls ({func['avg_time']:.3f}s avg)")
        
        # Cache management
        st.subheader("🗄️ Cache Management")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Cache"):
                clear_cache()
                st.success("Cache cleared!")
        
        with col2:
            if st.button("Refresh Data"):
                clear_cache()
                st.rerun()
        
    except Exception as e:
        logger.error(f"❌ Error showing performance dashboard: {e}")
        st.error(f"Error displaying performance dashboard: {e}")

def optimize_images(images: List[str], max_size: int = 1024) -> List[str]:
    """Optimize images for web display"""
    try:
        # In production, implement actual image optimization
        # For now, just return the original list
        logger.info(f"📸 Optimizing {len(images)} images")
        return images
        
    except Exception as e:
        logger.error(f"❌ Error optimizing images: {e}")
        return images

def lazy_load_data(data_type: str, page: int = 1, page_size: int = 20):
    """Lazy load data for better performance"""
    try:
        if data_type == 'applications':
            return get_applications_cached()
        elif data_type == 'users':
            return get_users_cached()
        elif data_type == 'analytics':
            return get_analytics_cached()
        else:
            return []
            
    except Exception as e:
        logger.error(f"❌ Error lazy loading {data_type}: {e}")
        return []

def preload_critical_data():
    """Preload critical data for better performance"""
    try:
        # Preload most important data
        get_analytics_cached()
        get_applications_cached()
        get_users_cached()
        
        logger.info("✅ Critical data preloaded successfully")
        
    except Exception as e:
        logger.error(f"❌ Error preloading critical data: {e}")

def setup_performance_monitoring():
    """Setup performance monitoring"""
    try:
        # Initialize performance tracking
        if 'performance_initialized' not in st.session_state:
            st.session_state.performance_initialized = True
            preload_critical_data()
            logger.info("✅ Performance monitoring initialized")
        
    except Exception as e:
        logger.error(f"❌ Error setting up performance monitoring: {e}")
