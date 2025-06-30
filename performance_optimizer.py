"""
QuestVibe Performance Optimizer
Handles caching, background processing, and performance optimizations.
"""

import streamlit as st
import time
import threading
import queue
from typing import Dict, Any, List, Optional
import functools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Handles performance optimizations for QuestVibe"""
    
    def __init__(self):
        self.cache = {}
        self.background_tasks = queue.Queue()
        self.task_results = {}
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def cache_question_generation(self, subject: str, topics: List[str], 
                                num_questions: int, question_types: List[str]) -> List[Dict]:
        """Cache question generation results"""
        cache_key = f"{subject}_{hash(tuple(topics))}_{num_questions}_{hash(tuple(question_types))}"
        
        if cache_key in self.cache:
            logger.info(f"Cache hit for {cache_key}")
            return self.cache[cache_key]
        
        # This would be populated by actual generation
        return []
    
    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def cache_database_queries(self, query: str, params: tuple = ()) -> List[Dict]:
        """Cache database query results"""
        cache_key = f"{query}_{hash(params)}"
        
        if cache_key in self.cache:
            logger.info(f"Database cache hit for {cache_key}")
            return self.cache[cache_key]
        
        return []
    
    def background_question_generation(self, generation_func, *args, **kwargs):
        """Run question generation in background"""
        def task():
            try:
                start_time = time.time()
                result = generation_func(*args, **kwargs)
                end_time = time.time()
                
                self.task_results['last_generation'] = {
                    'result': result,
                    'time_taken': end_time - start_time,
                    'status': 'completed'
                }
                
                logger.info(f"Background generation completed in {end_time - start_time:.2f}s")
                
            except Exception as e:
                self.task_results['last_generation'] = {
                    'result': None,
                    'error': str(e),
                    'status': 'failed'
                }
                logger.error(f"Background generation failed: {e}")
        
        thread = threading.Thread(target=task)
        thread.daemon = True
        thread.start()
        
        return thread
    
    def optimize_database_queries(self, queries: List[str]) -> List[str]:
        """Optimize database queries for better performance"""
        optimized_queries = []
        
        for query in queries:
            # Add indexes for common queries
            if "SELECT" in query.upper() and "WHERE" in query.upper():
                # Suggest adding indexes
                if "user_id" in query:
                    optimized_queries.append("CREATE INDEX IF NOT EXISTS idx_user_id ON users(id);")
                if "subject" in query:
                    optimized_queries.append("CREATE INDEX IF NOT EXISTS idx_subject ON question_generations(subject);")
            
            optimized_queries.append(query)
        
        return optimized_queries
    
    def monitor_performance(self, func_name: str):
        """Decorator to monitor function performance"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                execution_time = end_time - start_time
                logger.info(f"{func_name} executed in {execution_time:.2f}s")
                
                # Store performance metrics
                if 'performance_metrics' not in st.session_state:
                    st.session_state.performance_metrics = {}
                
                if func_name not in st.session_state.performance_metrics:
                    st.session_state.performance_metrics[func_name] = []
                
                st.session_state.performance_metrics[func_name].append({
                    'execution_time': execution_time,
                    'timestamp': time.time(),
                    'args_count': len(args),
                    'kwargs_count': len(kwargs)
                })
                
                # Keep only last 100 metrics
                if len(st.session_state.performance_metrics[func_name]) > 100:
                    st.session_state.performance_metrics[func_name] = \
                        st.session_state.performance_metrics[func_name][-100:]
                
                return result
            return wrapper
        return decorator
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        if 'performance_metrics' not in st.session_state:
            return {"message": "No performance data available"}
        
        report = {}
        
        for func_name, metrics in st.session_state.performance_metrics.items():
            if metrics:
                execution_times = [m['execution_time'] for m in metrics]
                report[func_name] = {
                    'total_calls': len(metrics),
                    'average_time': sum(execution_times) / len(execution_times),
                    'min_time': min(execution_times),
                    'max_time': max(execution_times),
                    'last_call': metrics[-1]['timestamp']
                }
        
        return report
    
    def optimize_memory_usage(self):
        """Optimize memory usage by clearing old cache entries"""
        current_time = time.time()
        cache_ttl = 3600  # 1 hour
        
        # Clear old cache entries
        keys_to_remove = []
        for key, value in self.cache.items():
            if isinstance(value, dict) and 'timestamp' in value:
                if current_time - value['timestamp'] > cache_ttl:
                    keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.cache[key]
        
        logger.info(f"Cleared {len(keys_to_remove)} old cache entries")
    
    def batch_process_questions(self, questions: List[Dict], batch_size: int = 10) -> List[List[Dict]]:
        """Process questions in batches for better performance"""
        batches = []
        for i in range(0, len(questions), batch_size):
            batches.append(questions[i:i + batch_size])
        return batches

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

# Performance monitoring decorators
def monitor_performance(func_name: str):
    """Decorator to monitor function performance"""
    return performance_optimizer.monitor_performance(func_name)

def cache_result(ttl: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{hash(str(args))}_{hash(str(kwargs))}"
            
            if cache_key in performance_optimizer.cache:
                cached_result = performance_optimizer.cache[cache_key]
                if time.time() - cached_result.get('timestamp', 0) < ttl:
                    return cached_result['data']
            
            result = func(*args, **kwargs)
            performance_optimizer.cache[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            
            return result
        return wrapper
    return decorator

# Background task management
class BackgroundTaskManager:
    """Manages background tasks for better user experience"""
    
    def __init__(self):
        self.tasks = {}
        self.results = {}
    
    def start_task(self, task_id: str, task_func, *args, **kwargs):
        """Start a background task"""
        def task_wrapper():
            try:
                start_time = time.time()
                result = task_func(*args, **kwargs)
                end_time = time.time()
                
                self.results[task_id] = {
                    'status': 'completed',
                    'result': result,
                    'execution_time': end_time - start_time,
                    'completed_at': time.time()
                }
                
            except Exception as e:
                self.results[task_id] = {
                    'status': 'failed',
                    'error': str(e),
                    'completed_at': time.time()
                }
        
        thread = threading.Thread(target=task_wrapper)
        thread.daemon = True
        thread.start()
        
        self.tasks[task_id] = {
            'thread': thread,
            'started_at': time.time(),
            'status': 'running'
        }
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a background task"""
        if task_id not in self.tasks:
            return {'status': 'not_found'}
        
        task = self.tasks[task_id]
        if task_id in self.results:
            return self.results[task_id]
        
        return {
            'status': 'running',
            'started_at': task['started_at'],
            'elapsed_time': time.time() - task['started_at']
        }
    
    def cleanup_completed_tasks(self, max_age: int = 3600):
        """Clean up old completed tasks"""
        current_time = time.time()
        
        # Clean up old results
        keys_to_remove = []
        for task_id, result in self.results.items():
            if current_time - result.get('completed_at', 0) > max_age:
                keys_to_remove.append(task_id)
        
        for task_id in keys_to_remove:
            del self.results[task_id]
            if task_id in self.tasks:
                del self.tasks[task_id]

# Global background task manager
background_task_manager = BackgroundTaskManager()

# Streamlit-specific optimizations
def optimize_streamlit_performance():
    """Apply Streamlit-specific performance optimizations"""
    
    # Configure Streamlit for better performance
    st.set_page_config(
        page_title="QuestVibe",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add custom CSS for performance
    st.markdown("""
    <style>
    /* Optimize rendering performance */
    .stApp {
        background-attachment: fixed;
    }
    
    /* Reduce animation complexity */
    .stButton > button {
        transition: all 0.2s ease;
    }
    
    /* Optimize text rendering */
    * {
        text-rendering: optimizeSpeed;
    }
    </style>
    """, unsafe_allow_html=True)

def lazy_load_components():
    """Lazy load heavy components for better initial load time"""
    
    # Only load heavy components when needed
    if st.session_state.get('show_manual_creation'):
        from streamlit_app import manual_creation_page
        manual_creation_page()
    
    if st.session_state.get('show_pattern_analysis'):
        from streamlit_app import pattern_analysis_page
        pattern_analysis_page()

# Database optimization
def optimize_database_connection():
    """Optimize database connections for better performance"""
    import sqlite3
    
    # Enable WAL mode for better concurrency
    conn = sqlite3.connect('user_data.db')
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    conn.execute('PRAGMA cache_size=10000')
    conn.execute('PRAGMA temp_store=MEMORY')
    conn.close()
    
    logger.info("Database optimized for better performance")

# Memory management
def cleanup_memory():
    """Clean up memory usage"""
    import gc
    
    # Force garbage collection
    gc.collect()
    
    # Clear old cache entries
    performance_optimizer.optimize_memory_usage()
    
    # Clean up background tasks
    background_task_manager.cleanup_completed_tasks()
    
    logger.info("Memory cleanup completed") 