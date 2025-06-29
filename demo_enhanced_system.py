#!/usr/bin/env python3
"""
Enhanced Question Paper Maker & Exam Pattern Analyzer Demo
==========================================================

This demo showcases the comprehensive features of the AI-powered system for:
1. Exam Pattern Analysis
2. Question Paper Generation
3. Advanced Analytics
4. Report Generation

Author: AI Assistant
Date: 2024
"""

import os
import sys
import json
from datetime import datetime
from collections import Counter, defaultdict
import pandas as pd
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our modules
from ingest import DocumentIngestor
from generate import generate_questions, generate_model_answer, assign_marks
from analyze import compute_analytics, compute_topic_frequency
from classify import tag_questions_by_topic

class EnhancedQuestionPaperSystem:
    """
    Enhanced Question Paper Maker & Exam Pattern Analyzer
    
    This class provides comprehensive functionality for:
    - Analyzing exam patterns from previous papers
    - Generating balanced question papers
    - Creating detailed reports and analytics
    - Predicting likely questions for future exams
    """
    
    def __init__(self):
        self.question_database = []
        self.syllabus_topics = []
        self.analysis_results = {}
        self.predictions = []
        
    def analyze_exam_patterns(self, file_paths):
        """
        Analyze exam patterns from multiple question papers
        
        Args:
            file_paths (list): List of file paths to analyze
            
        Returns:
            dict: Analysis results including topic distribution, trends, and predictions
        """
        print("🔍 Starting Exam Pattern Analysis...")
        
        all_questions = []
        paper_metadata = []
        
        for i, file_path in enumerate(file_paths):
            print(f"Processing file {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
            
            try:
                # Extract text from file
                ingestor = DocumentIngestor(file_path)
                ext = os.path.splitext(file_path)[-1].lower()
                
                if ext == '.pdf':
                    text_list = ingestor.parse_pdf()
                elif ext in ['.docx', '.doc']:
                    text_list = ingestor.parse_word()
                elif ext in ['.txt', '.text']:
                    text_list = ingestor.parse_text()
                else:
                    print(f"Unsupported file type: {ext}")
                    continue
                
                # Extract questions
                questions = ingestor.extract_questions(text_list)
                all_questions.extend(questions)
                
                # Store metadata
                paper_metadata.append({
                    'filename': os.path.basename(file_path),
                    'questions_extracted': len(questions),
                    'file_type': ext
                })
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        # Analyze extracted questions
        analysis_results = self._perform_comprehensive_analysis(all_questions, paper_metadata)
        
        print(f"✅ Analysis completed! Extracted {len(all_questions)} questions from {len(file_paths)} files")
        return analysis_results
    
    def _perform_comprehensive_analysis(self, questions, paper_metadata):
        """Perform comprehensive analysis of extracted questions"""
        
        # Basic statistics
        total_questions = len(questions)
        unique_questions = len(set(questions))
        
        # Topic analysis (if topics are provided)
        topic_analysis = {}
        if self.syllabus_topics:
            tagged_questions = tag_questions_by_topic(questions, self.syllabus_topics)
            topic_frequency = compute_topic_frequency(tagged_questions)
            topic_analysis = {
                'tagged_questions': len(tagged_questions),
                'topic_frequency': dict(topic_frequency),
                'coverage_percentage': (len(set(topic for _, topic in tagged_questions)) / len(self.syllabus_topics)) * 100
            }
        
        # Question pattern analysis
        question_patterns = self._analyze_question_patterns(questions)
        
        # Trend analysis
        trends = self._analyze_trends(questions)
        
        # Generate predictions
        predictions = self._generate_predictions(questions)
        
        return {
            'basic_stats': {
                'total_questions': total_questions,
                'unique_questions': unique_questions,
                'papers_analyzed': len(paper_metadata)
            },
            'topic_analysis': topic_analysis,
            'question_patterns': question_patterns,
            'trends': trends,
            'predictions': predictions,
            'paper_metadata': paper_metadata
        }
    
    def _analyze_question_patterns(self, questions):
        """Analyze patterns in question structure and content"""
        
        patterns = {
            'question_lengths': [],
            'common_keywords': Counter(),
            'question_starters': Counter(),
            'question_types': Counter()
        }
        
        for question in questions:
            # Analyze question length
            patterns['question_lengths'].append(len(question))
            
            # Extract common keywords
            words = question.lower().split()
            patterns['common_keywords'].update(words)
            
            # Analyze question starters
            if question.strip():
                first_word = question.strip().split()[0].lower()
                patterns['question_starters'][first_word] += 1
            
            # Classify question types based on keywords
            question_lower = question.lower()
            if any(word in question_lower for word in ['what', 'which', 'who', 'where', 'when']):
                patterns['question_types']['Wh-Question'] += 1
            elif any(word in question_lower for word in ['explain', 'describe', 'discuss']):
                patterns['question_types']['Explanation'] += 1
            elif any(word in question_lower for word in ['compare', 'contrast', 'analyze']):
                patterns['question_types']['Analysis'] += 1
            elif any(word in question_lower for word in ['evaluate', 'assess', 'criticize']):
                patterns['question_types']['Evaluation'] += 1
            else:
                patterns['question_types']['Other'] += 1
        
        # Calculate statistics
        patterns['avg_question_length'] = np.mean(patterns['question_lengths'])
        patterns['top_keywords'] = dict(patterns['common_keywords'].most_common(10))
        patterns['top_starters'] = dict(patterns['question_starters'].most_common(5))
        
        return patterns
    
    def _analyze_trends(self, questions):
        """Analyze trends in question content and style"""
        
        trends = {
            'complexity_trend': [],
            'topic_evolution': {},
            'style_changes': {}
        }
        
        # Analyze complexity trend (simplified)
        for question in questions:
            # Simple complexity measure based on sentence length and vocabulary
            words = question.split()
            avg_word_length = np.mean([len(word) for word in words])
            complexity_score = len(words) * avg_word_length / 100
            trends['complexity_trend'].append(complexity_score)
        
        trends['avg_complexity'] = np.mean(trends['complexity_trend'])
        trends['complexity_variance'] = np.var(trends['complexity_trend'])
        
        return trends
    
    def _generate_predictions(self, questions):
        """Generate predictions for future questions"""
        
        predictions = []
        
        # Analyze question patterns to predict future questions
        question_patterns = self._analyze_question_patterns(questions)
        
        # Predict based on common patterns
        top_keywords = question_patterns['top_keywords']
        top_starters = question_patterns['top_starters']
        question_types = question_patterns['question_types']
        
        # Generate prediction scenarios
        for keyword, frequency in list(top_keywords.items())[:5]:
            if len(keyword) > 3:  # Filter out short words
                predictions.append({
                    'type': 'keyword_based',
                    'prediction': f"Questions containing '{keyword}' are likely to appear",
                    'confidence': min(90, frequency * 10),
                    'evidence': f"Appeared {frequency} times in analyzed papers"
                })
        
        # Predict question types
        most_common_type = max(question_types.items(), key=lambda x: x[1])
        predictions.append({
            'type': 'question_type',
            'prediction': f"{most_common_type[0]} type questions are most likely",
            'confidence': min(85, most_common_type[1] * 5),
            'evidence': f"{most_common_type[1]} questions found in analyzed papers"
        })
        
        return predictions
    
    def generate_question_paper(self, syllabus_topics, exam_config):
        """
        Generate a comprehensive question paper based on syllabus and configuration
        
        Args:
            syllabus_topics (list): List of topics from syllabus
            exam_config (dict): Exam configuration parameters
            
        Returns:
            dict: Generated question paper with analysis
        """
        print("📝 Generating Question Paper...")
        
        self.syllabus_topics = syllabus_topics
        
        # Extract configuration parameters
        total_questions = exam_config.get('total_questions', 20)
        question_types = exam_config.get('question_types', ['MCQ', 'Short Answer', 'Long Answer'])
        difficulty = exam_config.get('difficulty', 'Mixed')
        total_marks = exam_config.get('total_marks', 100)
        
        # Generate questions
        questions = generate_questions(syllabus_topics, question_types, total_questions)
        
        # Calculate total marks
        total_assigned_marks = sum(assign_marks(q) for q in questions)
        
        # Generate model answers
        model_answers = []
        for question in questions:
            answer = generate_model_answer(question)
            model_answers.append({
                'question': question,
                'model_answer': answer,
                'marks': assign_marks(question)
            })
        
        # Analyze generated paper
        paper_analysis = self._analyze_generated_paper(questions, syllabus_topics)
        
        # Create comprehensive paper
        question_paper = {
            'paper_info': {
                'title': exam_config.get('title', 'Generated Question Paper'),
                'total_questions': len(questions),
                'total_marks': total_assigned_marks,
                'duration': exam_config.get('duration', 180),
                'difficulty': difficulty,
                'generated_at': datetime.now().isoformat()
            },
            'questions': questions,
            'model_answers': model_answers,
            'analysis': paper_analysis,
            'recommendations': self._generate_paper_recommendations(questions, syllabus_topics)
        }
        
        print(f"✅ Question paper generated successfully!")
        print(f"   - Total Questions: {len(questions)}")
        print(f"   - Total Marks: {total_assigned_marks}")
        print(f"   - Topics Covered: {len(set(q['topic'] for q in questions))}/{len(syllabus_topics)}")
        
        return question_paper
    
    def _analyze_generated_paper(self, questions, syllabus_topics):
        """Analyze the generated question paper"""
        
        # Basic analytics
        analytics = compute_analytics(questions)
        
        # Topic coverage analysis
        covered_topics = set(q['topic'] for q in questions)
        coverage_percentage = (len(covered_topics) / len(syllabus_topics)) * 100 if syllabus_topics else 0
        
        # Balance analysis
        topic_distribution = Counter(q['topic'] for q in questions)
        type_distribution = Counter(q['type'] for q in questions)
        bloom_distribution = Counter(q['bloom_level'] for q in questions)
        
        # Calculate balance score
        balance_score = self._calculate_balance_score(topic_distribution, type_distribution)
        
        return {
            'basic_analytics': analytics,
            'coverage_analysis': {
                'covered_topics': len(covered_topics),
                'total_topics': len(syllabus_topics),
                'coverage_percentage': coverage_percentage,
                'missing_topics': list(set(syllabus_topics) - covered_topics)
            },
            'distribution_analysis': {
                'topic_distribution': dict(topic_distribution),
                'type_distribution': dict(type_distribution),
                'bloom_distribution': dict(bloom_distribution)
            },
            'quality_metrics': {
                'balance_score': balance_score,
                'avg_marks_per_question': np.mean([assign_marks(q) for q in questions]),
                'cognitive_complexity': self._calculate_cognitive_complexity(bloom_distribution)
            }
        }
    
    def _calculate_balance_score(self, topic_dist, type_dist):
        """Calculate balance score for the question paper"""
        
        # Topic balance
        topic_counts = list(topic_dist.values())
        topic_balance = 1 - (np.std(topic_counts) / np.mean(topic_counts)) if topic_counts else 0
        
        # Type balance
        type_counts = list(type_dist.values())
        type_balance = 1 - (np.std(type_counts) / np.mean(type_counts)) if type_counts else 0
        
        # Overall balance score
        balance_score = (topic_balance + type_balance) / 2
        return max(0, min(1, balance_score))
    
    def _calculate_cognitive_complexity(self, bloom_dist):
        """Calculate cognitive complexity based on Bloom's taxonomy"""
        
        complexity_weights = {
            'Remember': 1,
            'Understand': 2,
            'Apply': 3,
            'Analyze': 4,
            'Evaluate': 5,
            'Create': 6
        }
        
        total_questions = sum(bloom_dist.values())
        if total_questions == 0:
            return 0
        
        weighted_sum = sum(bloom_dist.get(level, 0) * complexity_weights.get(level, 1) 
                          for level in bloom_dist)
        avg_complexity = weighted_sum / total_questions
        
        return avg_complexity
    
    def _generate_paper_recommendations(self, questions, syllabus_topics):
        """Generate recommendations for improving the question paper"""
        
        recommendations = []
        
        # Analyze topic coverage
        covered_topics = set(q['topic'] for q in questions)
        missing_topics = set(syllabus_topics) - covered_topics
        
        if missing_topics:
            recommendations.append({
                'type': 'coverage',
                'priority': 'high',
                'issue': f"Missing topics: {', '.join(missing_topics)}",
                'recommendation': "Add questions covering the missing topics"
            })
        
        # Analyze topic balance
        topic_distribution = Counter(q['topic'] for q in questions)
        for topic, count in topic_distribution.items():
            percentage = (count / len(questions)) * 100
            if percentage > 25:
                recommendations.append({
                    'type': 'balance',
                    'priority': 'medium',
                    'issue': f"Topic '{topic}' has high coverage ({percentage:.1f}%)",
                    'recommendation': f"Consider reducing questions on {topic}"
                })
        
        # Analyze cognitive levels
        bloom_distribution = Counter(q['bloom_level'] for q in questions)
        higher_order_skills = ['Analyze', 'Evaluate', 'Create']
        higher_order_count = sum(bloom_distribution.get(level, 0) for level in higher_order_skills)
        higher_order_percentage = (higher_order_count / len(questions)) * 100
        
        if higher_order_percentage < 30:
            recommendations.append({
                'type': 'cognitive',
                'priority': 'high',
                'issue': f"Low coverage of higher-order thinking skills ({higher_order_percentage:.1f}%)",
                'recommendation': "Increase questions requiring analysis, evaluation, and creation"
            })
        
        return recommendations
    
    def generate_comprehensive_report(self, analysis_results, question_paper=None):
        """
        Generate a comprehensive report combining analysis and generation results
        
        Args:
            analysis_results (dict): Results from pattern analysis
            question_paper (dict): Generated question paper (optional)
            
        Returns:
            dict: Comprehensive report
        """
        print("📋 Generating Comprehensive Report...")
        
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'report_type': 'comprehensive_analysis',
                'version': '2.0'
            },
            'pattern_analysis': analysis_results,
            'question_paper': question_paper,
            'summary_statistics': self._generate_summary_statistics(analysis_results, question_paper),
            'insights_and_recommendations': self._generate_insights(analysis_results, question_paper)
        }
        
        print("✅ Comprehensive report generated successfully!")
        return report
    
    def _generate_summary_statistics(self, analysis_results, question_paper):
        """Generate summary statistics for the report"""
        
        stats = {
            'papers_analyzed': analysis_results.get('basic_stats', {}).get('papers_analyzed', 0),
            'questions_analyzed': analysis_results.get('basic_stats', {}).get('total_questions', 0),
            'unique_questions': analysis_results.get('basic_stats', {}).get('unique_questions', 0)
        }
        
        if question_paper:
            stats.update({
                'questions_generated': len(question_paper.get('questions', [])),
                'marks_assigned': question_paper.get('paper_info', {}).get('total_marks', 0),
                'topics_covered': len(set(q['topic'] for q in question_paper.get('questions', [])))
            })
        
        return stats
    
    def _generate_insights(self, analysis_results, question_paper):
        """Generate insights and recommendations"""
        
        insights = {
            'key_findings': [],
            'trends_identified': [],
            'recommendations': []
        }
        
        # Key findings from pattern analysis
        basic_stats = analysis_results.get('basic_stats', {})
        if basic_stats.get('total_questions', 0) > 0:
            insights['key_findings'].append(
                f"Analyzed {basic_stats['total_questions']} questions from {basic_stats['papers_analyzed']} papers"
            )
        
        # Trends from analysis
        trends = analysis_results.get('trends', {})
        if trends.get('avg_complexity'):
            insights['trends_identified'].append(
                f"Average question complexity: {trends['avg_complexity']:.2f}"
            )
        
        # Predictions
        predictions = analysis_results.get('predictions', [])
        if predictions:
            top_prediction = max(predictions, key=lambda x: x.get('confidence', 0))
            insights['key_findings'].append(
                f"Top prediction: {top_prediction['prediction']} (Confidence: {top_prediction['confidence']}%)"
            )
        
        # Recommendations from question paper
        if question_paper:
            recommendations = question_paper.get('recommendations', [])
            insights['recommendations'].extend(recommendations)
        
        return insights
    
    def export_report(self, report, format='json', filename=None):
        """
        Export the report in specified format
        
        Args:
            report (dict): Report to export
            format (str): Export format ('json', 'txt')
            filename (str): Output filename
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"question_paper_report_{timestamp}.{format}"
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
        elif format == 'txt':
            with open(filename, 'w') as f:
                f.write(self._format_report_as_text(report))
        
        print(f"📤 Report exported to: {filename}")
        return filename
    
    def _format_report_as_text(self, report):
        """Format report as readable text"""
        
        text = []
        text.append("=" * 60)
        text.append("AI QUESTION PAPER MAKER & EXAM PATTERN ANALYZER")
        text.append("COMPREHENSIVE REPORT")
        text.append("=" * 60)
        text.append("")
        
        # Summary Statistics
        text.append("SUMMARY STATISTICS")
        text.append("-" * 20)
        stats = report.get('summary_statistics', {})
        for key, value in stats.items():
            text.append(f"{key.replace('_', ' ').title()}: {value}")
        text.append("")
        
        # Key Findings
        insights = report.get('insights_and_recommendations', {})
        if insights.get('key_findings'):
            text.append("KEY FINDINGS")
            text.append("-" * 15)
            for finding in insights['key_findings']:
                text.append(f"• {finding}")
            text.append("")
        
        # Recommendations
        if insights.get('recommendations'):
            text.append("RECOMMENDATIONS")
            text.append("-" * 15)
            for rec in insights['recommendations']:
                text.append(f"• {rec['issue']}")
                text.append(f"  Recommendation: {rec['recommendation']}")
                text.append(f"  Priority: {rec['priority']}")
                text.append("")
        
        return "\n".join(text)

def demo_enhanced_system():
    """Demo function showcasing the enhanced system capabilities"""
    
    print("🚀 Enhanced Question Paper Maker & Exam Pattern Analyzer Demo")
    print("=" * 70)
    print()
    
    # Initialize the system
    system = EnhancedQuestionPaperSystem()
    
    # Demo 1: Pattern Analysis
    print("📊 DEMO 1: Exam Pattern Analysis")
    print("-" * 40)
    
    # Simulate analyzing some files (using existing files in the directory)
    demo_files = []
    for file in os.listdir('.'):
        if file.endswith(('.pdf', '.docx', '.txt')) and 'question' in file.lower():
            demo_files.append(file)
    
    if demo_files:
        print(f"Found {len(demo_files)} question paper files for analysis")
        analysis_results = system.analyze_exam_patterns(demo_files)
        
        # Display key results
        basic_stats = analysis_results.get('basic_stats', {})
        print(f"📈 Analysis Results:")
        print(f"   - Papers analyzed: {basic_stats.get('papers_analyzed', 0)}")
        print(f"   - Questions extracted: {basic_stats.get('total_questions', 0)}")
        print(f"   - Unique questions: {basic_stats.get('unique_questions', 0)}")
        
        # Show predictions
        predictions = analysis_results.get('predictions', [])
        if predictions:
            print(f"🔮 Top Predictions:")
            for pred in predictions[:3]:
                print(f"   - {pred['prediction']} (Confidence: {pred['confidence']}%)")
    else:
        print("No question paper files found for analysis")
        # Create mock analysis results for demo
        analysis_results = {
            'basic_stats': {'papers_analyzed': 5, 'total_questions': 150, 'unique_questions': 120},
            'predictions': [
                {'prediction': 'Database concepts likely to appear', 'confidence': 85},
                {'prediction': 'SQL queries will be tested', 'confidence': 78}
            ]
        }
    
    print()
    
    # Demo 2: Question Paper Generation
    print("📝 DEMO 2: Question Paper Generation")
    print("-" * 40)
    
    # Sample syllabus topics
    syllabus_topics = [
        "Database Management Systems",
        "SQL Queries",
        "Normalization",
        "Transaction Management",
        "Indexing and Performance",
        "Data Modeling",
        "Database Security",
        "Distributed Databases"
    ]
    
    # Exam configuration
    exam_config = {
        'title': 'Database Management Systems - Final Exam',
        'total_questions': 15,
        'total_marks': 100,
        'duration': 180,
        'question_types': ['MCQ', 'Short Answer', 'Long Answer'],
        'difficulty': 'Mixed'
    }
    
    print(f"Generating question paper for {len(syllabus_topics)} topics...")
    question_paper = system.generate_question_paper(syllabus_topics, exam_config)
    
    # Display paper summary
    paper_info = question_paper.get('paper_info', {})
    analysis = question_paper.get('analysis', {})
    
    print(f"📄 Generated Paper Summary:")
    print(f"   - Title: {paper_info.get('title', 'N/A')}")
    print(f"   - Questions: {paper_info.get('total_questions', 0)}")
    print(f"   - Total Marks: {paper_info.get('total_marks', 0)}")
    print(f"   - Duration: {paper_info.get('duration', 0)} minutes")
    
    coverage = analysis.get('coverage_analysis', {})
    print(f"   - Topics Covered: {coverage.get('covered_topics', 0)}/{coverage.get('total_topics', 0)}")
    print(f"   - Coverage: {coverage.get('coverage_percentage', 0):.1f}%")
    
    quality = analysis.get('quality_metrics', {})
    print(f"   - Balance Score: {quality.get('balance_score', 0):.2f}")
    print(f"   - Cognitive Complexity: {quality.get('cognitive_complexity', 0):.2f}")
    
    print()
    
    # Demo 3: Comprehensive Report Generation
    print("📋 DEMO 3: Comprehensive Report Generation")
    print("-" * 40)
    
    print("Generating comprehensive report...")
    comprehensive_report = system.generate_comprehensive_report(analysis_results, question_paper)
    
    # Export report
    report_filename = system.export_report(comprehensive_report, format='json')
    print(f"Report exported to: {report_filename}")
    
    # Display report summary
    summary = comprehensive_report.get('summary_statistics', {})
    print(f"📊 Report Summary:")
    print(f"   - Papers Analyzed: {summary.get('papers_analyzed', 0)}")
    print(f"   - Questions Analyzed: {summary.get('questions_analyzed', 0)}")
    print(f"   - Questions Generated: {summary.get('questions_generated', 0)}")
    print(f"   - Topics Covered: {summary.get('topics_covered', 0)}")
    
    print()
    print("🎉 Demo completed successfully!")
    print("=" * 70)
    
    return comprehensive_report

if __name__ == "__main__":
    # Run the demo
    demo_enhanced_system() 