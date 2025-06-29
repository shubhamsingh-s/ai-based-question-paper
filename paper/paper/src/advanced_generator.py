import random
import json
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import numpy as np
from datetime import datetime

class AdvancedQuestionGenerator:
    def __init__(self):
        self.question_templates = self._load_question_templates()
        self.bloom_verbs = self._load_bloom_verbs()
        self.difficulty_markers = self._load_difficulty_markers()
        
    def _load_question_templates(self) -> Dict:
        """Load question templates for different types and cognitive levels"""
        return {
            'MCQ': {
                'Remember': [
                    'Which of the following best defines {topic}?',
                    'What is the primary purpose of {topic}?',
                    'Identify the correct definition of {topic}.',
                    'Which statement accurately describes {topic}?'
                ],
                'Understand': [
                    'Which of the following explains {topic} correctly?',
                    'How does {topic} relate to {related_concept}?',
                    'Which scenario best demonstrates {topic}?',
                    'What is the significance of {topic} in {context}?'
                ],
                'Apply': [
                    'Given {scenario}, which {topic} principle would you apply?',
                    'How would you use {topic} to solve {problem}?',
                    'Which {topic} method is most appropriate for {situation}?',
                    'In {context}, which {topic} approach would be best?'
                ],
                'Analyze': [
                    'Compare and contrast {topic} with {related_topic}.',
                    'What are the key components of {topic}?',
                    'Analyze the relationship between {topic} and {factor}.',
                    'Which factors influence {topic}?'
                ],
                'Evaluate': [
                    'Which {topic} approach is most effective for {objective}?',
                    'Evaluate the strengths and weaknesses of {topic}.',
                    'Which {topic} solution would be most suitable for {scenario}?',
                    'Assess the impact of {topic} on {outcome}.'
                ],
                'Create': [
                    'Design a {topic} solution for {challenge}.',
                    'Propose a new approach to {topic}.',
                    'Create a {topic} framework for {purpose}.',
                    'Develop a {topic} strategy for {goal}.'
                ]
            },
            'Short Answer': {
                'Remember': [
                    'Define {topic} and list its key characteristics.',
                    'What are the main components of {topic}?',
                    'State the fundamental principles of {topic}.',
                    'List the essential features of {topic}.'
                ],
                'Understand': [
                    'Explain the concept of {topic} in your own words.',
                    'Describe how {topic} works in practice.',
                    'Summarize the importance of {topic}.',
                    'Clarify the relationship between {topic} and {related_concept}.'
                ],
                'Apply': [
                    'Demonstrate how {topic} can be applied to {scenario}.',
                    'Show how {topic} principles work in {context}.',
                    'Illustrate the use of {topic} in {situation}.',
                    'Apply {topic} concepts to solve {problem}.'
                ],
                'Analyze': [
                    'Break down {topic} into its constituent parts.',
                    'Analyze the factors that affect {topic}.',
                    'Examine the relationship between {topic} and {factor}.',
                    'Investigate the causes and effects of {topic}.'
                ],
                'Evaluate': [
                    'Assess the effectiveness of {topic} in {context}.',
                    'Evaluate the pros and cons of {topic}.',
                    'Judge the reliability of {topic} methods.',
                    'Critique the implementation of {topic}.'
                ],
                'Create': [
                    'Propose a new application of {topic}.',
                    'Design a {topic} solution for {challenge}.',
                    'Develop a {topic} framework for {purpose}.',
                    'Create an innovative approach to {topic}.'
                ]
            },
            'Long Answer': {
                'Remember': [
                    'Provide a comprehensive definition of {topic} and discuss its historical development.',
                    'Detail the complete framework of {topic} including all its components.',
                    'Present a thorough overview of {topic} principles and their evolution.',
                    'Describe the complete structure and organization of {topic}.'
                ],
                'Understand': [
                    'Explain {topic} in detail, including its underlying mechanisms and relationships.',
                    'Provide a comprehensive analysis of how {topic} functions in various contexts.',
                    'Discuss the theoretical foundations and practical implications of {topic}.',
                    'Elaborate on the significance and impact of {topic} in the field.'
                ],
                'Apply': [
                    'Demonstrate comprehensive application of {topic} principles to complex scenarios.',
                    'Show detailed implementation of {topic} in real-world situations.',
                    'Provide extensive examples of {topic} applications across different domains.',
                    'Illustrate advanced usage of {topic} in solving complex problems.'
                ],
                'Analyze': [
                    'Conduct a thorough analysis of {topic}, examining all its aspects and relationships.',
                    'Perform detailed investigation of {topic} components and their interactions.',
                    'Analyze the complex dynamics and interdependencies within {topic}.',
                    'Examine the multifaceted nature of {topic} and its various dimensions.'
                ],
                'Evaluate': [
                    'Provide comprehensive evaluation of {topic} effectiveness and limitations.',
                    'Conduct thorough assessment of {topic} methodologies and outcomes.',
                    'Evaluate the overall impact and value of {topic} in practice.',
                    'Critically analyze the strengths, weaknesses, and future prospects of {topic}.'
                ],
                'Create': [
                    'Design and develop a comprehensive {topic} solution for complex challenges.',
                    'Create an innovative and detailed {topic} framework for advanced applications.',
                    'Propose and elaborate on novel approaches to {topic} implementation.',
                    'Develop a complete and original {topic} strategy for future development.'
                ]
            },
            'Case Study': {
                'Remember': [
                    'Case Study: A company is implementing {topic}. Identify all the key components and requirements involved.',
                    'Scenario: An organization is adopting {topic}. List all the essential elements and considerations.',
                    'Case: A project team is working with {topic}. Describe all the fundamental aspects they need to understand.',
                    'Situation: A business is integrating {topic}. Outline all the critical factors and prerequisites.'
                ],
                'Understand': [
                    'Case Study: Analyze how {topic} functions in the given scenario and explain its role.',
                    'Scenario: Examine the relationship between {topic} and the organizational context provided.',
                    'Case: Investigate how {topic} principles apply to the described situation.',
                    'Situation: Understand the implications of {topic} in the given business context.'
                ],
                'Apply': [
                    'Case Study: Apply {topic} principles to solve the challenges presented in the scenario.',
                    'Scenario: Use {topic} methodologies to address the issues described in the case.',
                    'Case: Implement {topic} solutions to resolve the problems outlined.',
                    'Situation: Utilize {topic} approaches to handle the circumstances described.'
                ],
                'Analyze': [
                    'Case Study: Conduct a detailed analysis of how {topic} factors influence the given situation.',
                    'Scenario: Analyze the complex interactions between {topic} and other organizational elements.',
                    'Case: Examine the underlying causes and effects of {topic} in the described context.',
                    'Situation: Investigate the various dimensions and implications of {topic} in the scenario.'
                ],
                'Evaluate': [
                    'Case Study: Evaluate the effectiveness of {topic} implementation in the given context.',
                    'Scenario: Assess the success and limitations of {topic} approaches in the described situation.',
                    'Case: Judge the appropriateness and outcomes of {topic} strategies in the scenario.',
                    'Situation: Critique the implementation and results of {topic} in the given context.'
                ],
                'Create': [
                    'Case Study: Design a comprehensive {topic} solution for the challenges presented.',
                    'Scenario: Create an innovative {topic} framework to address the described situation.',
                    'Case: Develop a novel {topic} approach to solve the problems outlined.',
                    'Situation: Propose a creative {topic} strategy for the given circumstances.'
                ]
            }
        }
    
    def _load_bloom_verbs(self) -> Dict:
        """Load Bloom's taxonomy verbs for each cognitive level"""
        return {
            'Remember': ['define', 'list', 'state', 'identify', 'recall', 'recognize'],
            'Understand': ['explain', 'describe', 'summarize', 'interpret', 'clarify', 'illustrate'],
            'Apply': ['demonstrate', 'show', 'use', 'apply', 'implement', 'execute'],
            'Analyze': ['analyze', 'examine', 'investigate', 'compare', 'contrast', 'break down'],
            'Evaluate': ['assess', 'evaluate', 'judge', 'critique', 'appraise', 'examine'],
            'Create': ['design', 'create', 'develop', 'propose', 'construct', 'formulate']
        }
    
    def _load_difficulty_markers(self) -> Dict:
        """Load difficulty markers for different levels"""
        return {
            'Easy': ['basic', 'simple', 'fundamental', 'elementary', 'straightforward'],
            'Medium': ['intermediate', 'moderate', 'standard', 'typical', 'common'],
            'Hard': ['advanced', 'complex', 'sophisticated', 'challenging', 'difficult']
        }
    
    def generate_question_paper(self, 
                               syllabus_topics: List[str],
                               exam_config: Dict,
                               difficulty_distribution: Dict = None,
                               topic_weightage: Dict = None) -> Dict:
        """
        Generate a comprehensive question paper based on syllabus and configuration
        
        Args:
            syllabus_topics: List of topics from syllabus
            exam_config: Dictionary with exam parameters
            difficulty_distribution: Distribution of difficulty levels
            topic_weightage: Weightage for each topic
        """
        
        # Default configurations
        if difficulty_distribution is None:
            difficulty_distribution = {'Easy': 0.3, 'Medium': 0.5, 'Hard': 0.2}
        
        if topic_weightage is None:
            # Equal weightage for all topics
            topic_weightage = {topic: 1.0 for topic in syllabus_topics}
        
        # Calculate questions per topic based on weightage
        total_weight = sum(topic_weightage.values())
        topic_questions = {}
        
        for topic, weight in topic_weightage.items():
            topic_questions[topic] = int((weight / total_weight) * exam_config['total_questions'])
        
        # Adjust for rounding errors
        while sum(topic_questions.values()) < exam_config['total_questions']:
            # Add remaining questions to topics with highest weightage
            max_topic = max(topic_weightage.items(), key=lambda x: x[1])[0]
            topic_questions[max_topic] += 1
        
        # Generate questions
        all_questions = []
        question_id = 1
        
        for topic, num_questions in topic_questions.items():
            topic_questions_list = self._generate_topic_questions(
                topic, num_questions, exam_config, difficulty_distribution
            )
            
            for q in topic_questions_list:
                q['id'] = question_id
                q['topic'] = topic
                all_questions.append(q)
                question_id += 1
        
        # Calculate total marks
        total_marks = sum(q['marks'] for q in all_questions)
        
        return {
            'paper_info': {
                'title': exam_config.get('title', 'Generated Question Paper'),
                'total_questions': len(all_questions),
                'total_marks': total_marks,
                'duration': exam_config.get('duration', 180),
                'instructions': exam_config.get('instructions', ''),
                'generated_at': datetime.now().isoformat()
            },
            'questions': all_questions,
            'analysis': self._analyze_generated_paper(all_questions, syllabus_topics)
        }
    
    def _generate_topic_questions(self, 
                                 topic: str, 
                                 num_questions: int, 
                                 exam_config: Dict,
                                 difficulty_distribution: Dict) -> List[Dict]:
        """Generate questions for a specific topic"""
        questions = []
        question_types = exam_config.get('question_types', ['MCQ', 'Short Answer', 'Long Answer'])
        
        # Distribute questions across types
        type_distribution = self._calculate_type_distribution(num_questions, question_types)
        
        for qtype, count in type_distribution.items():
            for _ in range(count):
                # Select difficulty level based on distribution
                difficulty = self._select_difficulty(difficulty_distribution)
                
                # Select cognitive level
                bloom_level = self._select_bloom_level(qtype, difficulty)
                
                # Generate question
                question_text = self._generate_question_text(topic, qtype, bloom_level, difficulty)
                
                # Assign marks
                marks = self._assign_marks(qtype, difficulty, bloom_level)
                
                questions.append({
                    'question': question_text,
                    'type': qtype,
                    'bloom_level': bloom_level,
                    'difficulty': difficulty,
                    'marks': marks,
                    'topic': topic
                })
        
        return questions
    
    def _calculate_type_distribution(self, num_questions: int, question_types: List[str]) -> Dict:
        """Calculate how many questions of each type to generate"""
        # Default distribution weights
        type_weights = {
            'MCQ': 0.4,
            'Short Answer': 0.3,
            'Long Answer': 0.2,
            'Case Study': 0.1
        }
        
        distribution = {}
        total_weight = sum(type_weights.get(qtype, 0.1) for qtype in question_types)
        
        for qtype in question_types:
            weight = type_weights.get(qtype, 0.1)
            distribution[qtype] = int((weight / total_weight) * num_questions)
        
        # Adjust for rounding
        while sum(distribution.values()) < num_questions:
            # Add to type with highest weight
            max_type = max(type_weights.items(), key=lambda x: x[1])[0]
            if max_type in distribution:
                distribution[max_type] += 1
        
        return distribution
    
    def _select_difficulty(self, difficulty_distribution: Dict) -> str:
        """Select difficulty level based on distribution"""
        difficulties = list(difficulty_distribution.keys())
        probabilities = list(difficulty_distribution.values())
        return random.choices(difficulties, weights=probabilities)[0]
    
    def _select_bloom_level(self, question_type: str, difficulty: str) -> str:
        """Select appropriate Bloom's level based on question type and difficulty"""
        if difficulty == 'Easy':
            levels = ['Remember', 'Understand']
        elif difficulty == 'Medium':
            levels = ['Understand', 'Apply', 'Analyze']
        else:  # Hard
            levels = ['Analyze', 'Evaluate', 'Create']
        
        return random.choice(levels)
    
    def _generate_question_text(self, topic: str, qtype: str, bloom_level: str, difficulty: str) -> str:
        """Generate question text using templates"""
        templates = self.question_templates.get(qtype, {}).get(bloom_level, [])
        
        if not templates:
            # Fallback template
            templates = [f'Discuss {topic} in detail.']
        
        template = random.choice(templates)
        
        # Replace placeholders
        question_text = template.format(
            topic=topic,
            related_concept=self._get_related_concept(topic),
            context=self._get_context(topic),
            scenario=self._get_scenario(topic),
            problem=self._get_problem(topic),
            situation=self._get_situation(topic),
            related_topic=self._get_related_topic(topic),
            factor=self._get_factor(topic),
            objective=self._get_objective(topic),
            outcome=self._get_outcome(topic),
            challenge=self._get_challenge(topic),
            purpose=self._get_purpose(topic),
            goal=self._get_goal(topic)
        )
        
        return question_text
    
    def _assign_marks(self, question_type: str, difficulty: str, bloom_level: str) -> int:
        """Assign marks based on question type, difficulty, and cognitive level"""
        base_marks = {
            'MCQ': 1,
            'Short Answer': 3,
            'Long Answer': 8,
            'Case Study': 10
        }
        
        base = base_marks.get(question_type, 2)
        
        # Adjust for difficulty
        difficulty_multiplier = {
            'Easy': 0.8,
            'Medium': 1.0,
            'Hard': 1.2
        }
        
        # Adjust for cognitive level
        bloom_multiplier = {
            'Remember': 0.8,
            'Understand': 0.9,
            'Apply': 1.0,
            'Analyze': 1.1,
            'Evaluate': 1.2,
            'Create': 1.3
        }
        
        adjusted_marks = base * difficulty_multiplier.get(difficulty, 1.0) * bloom_multiplier.get(bloom_level, 1.0)
        return max(1, int(round(adjusted_marks)))
    
    def _analyze_generated_paper(self, questions: List[Dict], syllabus_topics: List[str]) -> Dict:
        """Analyze the generated question paper"""
        topic_coverage = Counter(q['topic'] for q in questions)
        type_distribution = Counter(q['type'] for q in questions)
        bloom_distribution = Counter(q['bloom_level'] for q in questions)
        difficulty_distribution = Counter(q['difficulty'] for q in questions)
        
        # Calculate coverage percentage
        covered_topics = len(topic_coverage)
        coverage_percentage = (covered_topics / len(syllabus_topics)) * 100 if syllabus_topics else 0
        
        return {
            'topic_coverage': dict(topic_coverage),
            'type_distribution': dict(type_distribution),
            'bloom_distribution': dict(bloom_distribution),
            'difficulty_distribution': dict(difficulty_distribution),
            'coverage_percentage': coverage_percentage,
            'total_marks': sum(q['marks'] for q in questions),
            'average_marks_per_question': np.mean([q['marks'] for q in questions])
        }
    
    # Helper methods for placeholder replacement
    def _get_related_concept(self, topic: str) -> str:
        related_concepts = ['data management', 'system design', 'analysis', 'implementation']
        return random.choice(related_concepts)
    
    def _get_context(self, topic: str) -> str:
        contexts = ['business environment', 'technical system', 'organizational setting', 'academic research']
        return random.choice(contexts)
    
    def _get_scenario(self, topic: str) -> str:
        scenarios = ['a company implementing new technology', 'an organization undergoing digital transformation', 
                    'a project team working on system development', 'a business facing operational challenges']
        return random.choice(scenarios)
    
    def _get_problem(self, topic: str) -> str:
        problems = ['data management issues', 'system performance problems', 'operational inefficiencies', 
                   'technical challenges', 'organizational bottlenecks']
        return random.choice(problems)
    
    def _get_situation(self, topic: str) -> str:
        situations = ['high-volume data processing', 'real-time system requirements', 'multi-user environment', 
                     'distributed system architecture', 'mission-critical applications']
        return random.choice(situations)
    
    def _get_related_topic(self, topic: str) -> str:
        related_topics = ['data structures', 'algorithms', 'system architecture', 'performance optimization']
        return random.choice(related_topics)
    
    def _get_factor(self, topic: str) -> str:
        factors = ['performance', 'scalability', 'reliability', 'security', 'cost-effectiveness']
        return random.choice(factors)
    
    def _get_objective(self, topic: str) -> str:
        objectives = ['improving efficiency', 'reducing costs', 'enhancing performance', 'increasing reliability']
        return random.choice(objectives)
    
    def _get_outcome(self, topic: str) -> str:
        outcomes = ['system performance', 'user satisfaction', 'operational efficiency', 'business success']
        return random.choice(outcomes)
    
    def _get_challenge(self, topic: str) -> str:
        challenges = ['scaling operations', 'managing complexity', 'ensuring reliability', 'optimizing performance']
        return random.choice(challenges)
    
    def _get_purpose(self, topic: str) -> str:
        purposes = ['data analysis', 'system optimization', 'process improvement', 'decision support']
        return random.choice(purposes)
    
    def _get_goal(self, topic: str) -> str:
        goals = ['improving efficiency', 'reducing costs', 'enhancing performance', 'achieving scalability']
        return random.choice(goals) 