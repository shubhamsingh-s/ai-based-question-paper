import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class AdvancedExamAnalyzer:
    def __init__(self):
        self.question_database = []
        self.topic_weights = {}
        self.trend_analysis = {}
        self.prediction_model = None
        
    def add_question_paper(self, questions: List[Dict], paper_metadata: Dict = None):
        """Add a question paper to the analysis database"""
        paper_data = {
            'questions': questions,
            'metadata': paper_metadata or {},
            'timestamp': datetime.now()
        }
        self.question_database.append(paper_data)
        
    def analyze_topic_distribution(self) -> Dict:
        """Analyze topic distribution across all papers"""
        all_topics = []
        topic_marks = defaultdict(int)
        topic_frequency = Counter()
        
        for paper in self.question_database:
            for q in paper['questions']:
                topic = q.get('topic', 'Unknown')
                marks = q.get('marks', 1)
                all_topics.append(topic)
                topic_marks[topic] += marks
                topic_frequency[topic] += 1
                
        total_marks = sum(topic_marks.values())
        topic_weightage = {topic: (marks/total_marks)*100 for topic, marks in topic_marks.items()}
        
        return {
            'topic_frequency': dict(topic_frequency),
            'topic_weightage': topic_weightage,
            'total_questions': len(all_topics),
            'unique_topics': len(set(all_topics))
        }
    
    def analyze_question_types(self) -> Dict:
        """Analyze distribution of question types"""
        type_counts = Counter()
        type_marks = defaultdict(int)
        
        for paper in self.question_database:
            for q in paper['questions']:
                qtype = q.get('type', 'Unknown')
                marks = q.get('marks', 1)
                type_counts[qtype] += 1
                type_marks[qtype] += marks
                
        return {
            'type_distribution': dict(type_counts),
            'type_marks_distribution': dict(type_marks)
        }
    
    def analyze_bloom_levels(self) -> Dict:
        """Analyze cognitive levels distribution"""
        bloom_counts = Counter()
        bloom_marks = defaultdict(int)
        
        for paper in self.question_database:
            for q in paper['questions']:
                bloom = q.get('bloom_level', 'Unknown')
                marks = q.get('marks', 1)
                bloom_counts[bloom] += 1
                bloom_marks[bloom] += marks
                
        return {
            'bloom_distribution': dict(bloom_counts),
            'bloom_marks_distribution': dict(bloom_marks)
        }
    
    def analyze_temporal_trends(self, years_back: int = 5) -> Dict:
        """Analyze trends over time"""
        current_year = datetime.now().year
        year_data = defaultdict(lambda: {'questions': 0, 'topics': Counter(), 'types': Counter()})
        
        for paper in self.question_database:
            # Extract year from metadata or use current year
            paper_year = paper['metadata'].get('year', current_year)
            if current_year - paper_year <= years_back:
                for q in paper['questions']:
                    year_data[paper_year]['questions'] += 1
                    year_data[paper_year]['topics'][q.get('topic', 'Unknown')] += 1
                    year_data[paper_year]['types'][q.get('type', 'Unknown')] += 1
                    
        return dict(year_data)
    
    def predict_likely_questions(self, syllabus_topics: List[str], num_predictions: int = 10) -> List[Dict]:
        """Predict likely questions based on historical patterns"""
        topic_analysis = self.analyze_topic_distribution()
        type_analysis = self.analyze_question_types()
        
        predictions = []
        
        for topic in syllabus_topics:
            # Calculate topic probability
            topic_freq = topic_analysis['topic_frequency'].get(topic, 0)
            total_questions = topic_analysis['total_questions']
            topic_probability = (topic_freq / total_questions) * 100 if total_questions > 0 else 0
            
            # Get most common question types for this topic
            topic_questions = []
            for paper in self.question_database:
                for q in paper['questions']:
                    if q.get('topic', '').lower() == topic.lower():
                        topic_questions.append(q)
            
            if topic_questions:
                type_counts = Counter(q.get('type', 'Unknown') for q in topic_questions)
                most_common_type = type_counts.most_common(1)[0][0] if type_counts else 'Short Answer'
                
                # Calculate confidence based on frequency and recency
                confidence = min(95, topic_probability + 20)  # Base confidence
                
                predictions.append({
                    'topic': topic,
                    'question_type': most_common_type,
                    'probability': topic_probability,
                    'confidence': confidence,
                    'historical_frequency': topic_freq,
                    'recommended_marks': self._get_recommended_marks(most_common_type)
                })
        
        # Sort by probability and return top predictions
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        return predictions[:num_predictions]
    
    def _get_recommended_marks(self, question_type: str) -> int:
        """Get recommended marks for a question type based on historical data"""
        type_marks = []
        for paper in self.question_database:
            for q in paper['questions']:
                if q.get('type') == question_type:
                    type_marks.append(q.get('marks', 1))
        
        if type_marks:
            return int(np.mean(type_marks))
        else:
            # Default marks
            defaults = {'MCQ': 1, 'Short Answer': 3, 'Long Answer': 8, 'Case Study': 10}
            return defaults.get(question_type, 2)
    
    def identify_hot_topics(self, threshold_percentage: float = 10.0) -> List[Dict]:
        """Identify topics that appear frequently (hot topics)"""
        topic_analysis = self.analyze_topic_distribution()
        hot_topics = []
        
        for topic, weightage in topic_analysis['topic_weightage'].items():
            if weightage >= threshold_percentage:
                hot_topics.append({
                    'topic': topic,
                    'weightage': weightage,
                    'frequency': topic_analysis['topic_frequency'].get(topic, 0),
                    'status': 'Hot Topic'
                })
        
        return sorted(hot_topics, key=lambda x: x['weightage'], reverse=True)
    
    def identify_declining_topics(self, years_back: int = 3) -> List[Dict]:
        """Identify topics that are declining in frequency"""
        temporal_data = self.analyze_temporal_trends(years_back)
        current_year = datetime.now().year
        
        # Get recent years data
        recent_years = [year for year in temporal_data.keys() if current_year - year <= years_back]
        if len(recent_years) < 2:
            return []
        
        declining_topics = []
        
        # Compare recent years
        for year in sorted(recent_years)[:-1]:
            next_year = year + 1
            if next_year in temporal_data:
                current_topics = temporal_data[year]['topics']
                next_topics = temporal_data[next_year]['topics']
                
                for topic in current_topics:
                    if topic in next_topics:
                        current_freq = current_topics[topic]
                        next_freq = next_topics[topic]
                        if next_freq < current_freq:
                            decline_percentage = ((current_freq - next_freq) / current_freq) * 100
                            declining_topics.append({
                                'topic': topic,
                                'year': year,
                                'decline_percentage': decline_percentage,
                                'previous_frequency': current_freq,
                                'current_frequency': next_freq
                            })
        
        return sorted(declining_topics, key=lambda x: x['decline_percentage'], reverse=True)
    
    def generate_analytics_report(self) -> Dict:
        """Generate comprehensive analytics report"""
        return {
            'topic_analysis': self.analyze_topic_distribution(),
            'type_analysis': self.analyze_question_types(),
            'bloom_analysis': self.analyze_bloom_levels(),
            'temporal_trends': self.analyze_temporal_trends(),
            'hot_topics': self.identify_hot_topics(),
            'declining_topics': self.identify_declining_topics(),
            'total_papers_analyzed': len(self.question_database)
        }
    
    def create_visualizations(self) -> Dict:
        """Create various visualizations for the analysis"""
        topic_analysis = self.analyze_topic_distribution()
        type_analysis = self.analyze_question_types()
        bloom_analysis = self.analyze_bloom_levels()
        
        # Topic distribution pie chart
        fig1 = px.pie(
            values=list(topic_analysis['topic_weightage'].values()),
            names=list(topic_analysis['topic_weightage'].keys()),
            title='Topic Weightage Distribution'
        )
        
        # Question type distribution bar chart
        fig2 = px.bar(
            x=list(type_analysis['type_distribution'].keys()),
            y=list(type_analysis['type_distribution'].values()),
            title='Question Type Distribution'
        )
        
        # Bloom's taxonomy distribution
        fig3 = px.bar(
            x=list(bloom_analysis['bloom_distribution'].keys()),
            y=list(bloom_analysis['bloom_distribution'].values()),
            title='Cognitive Levels Distribution'
        )
        
        # Temporal trends
        temporal_data = self.analyze_temporal_trends()
        if temporal_data:
            years = sorted(temporal_data.keys())
            question_counts = [temporal_data[year]['questions'] for year in years]
            fig4 = px.line(
                x=years,
                y=question_counts,
                title='Question Count Trends Over Time'
            )
        else:
            fig4 = None
        
        return {
            'topic_distribution': fig1,
            'type_distribution': fig2,
            'bloom_distribution': fig3,
            'temporal_trends': fig4
        } 