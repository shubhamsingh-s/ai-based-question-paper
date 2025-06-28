import random
from typing import Dict, List, Tuple
import re

class ModelAnswerGenerator:
    def __init__(self):
        self.answer_templates = self._load_answer_templates()
        self.marking_schemes = self._load_marking_schemes()
        self.alternative_approaches = self._load_alternative_approaches()
        
    def _load_answer_templates(self) -> Dict:
        """Load answer templates for different question types and cognitive levels"""
        return {
            'MCQ': {
                'Remember': 'The correct answer is {correct_option}. {topic} is defined as {definition}.',
                'Understand': 'The correct answer is {correct_option}. This is because {explanation}.',
                'Apply': 'The correct answer is {correct_option}. In this scenario, {application_logic}.',
                'Analyze': 'The correct answer is {correct_option}. Analysis shows that {analysis_reasoning}.',
                'Evaluate': 'The correct answer is {correct_option}. Evaluation indicates {evaluation_criteria}.',
                'Create': 'The correct answer is {correct_option}. This represents {creative_solution}.'
            },
            'Short Answer': {
                'Remember': '{topic} refers to {definition}. Key characteristics include: {key_points}.',
                'Understand': '{topic} can be understood as {explanation}. This concept is important because {significance}.',
                'Apply': 'To apply {topic} in this context: {application_steps}. The expected outcome is {expected_result}.',
                'Analyze': 'Analysis of {topic} reveals: {analysis_points}. The relationship with {related_factor} shows {relationship_insight}.',
                'Evaluate': 'Evaluation of {topic} shows: {evaluation_points}. The effectiveness is {effectiveness_assessment}.',
                'Create': 'A creative approach to {topic} involves: {creative_elements}. This solution addresses {addressed_challenges}.'
            },
            'Long Answer': {
                'Remember': self._get_long_answer_template('Remember'),
                'Understand': self._get_long_answer_template('Understand'),
                'Apply': self._get_long_answer_template('Apply'),
                'Analyze': self._get_long_answer_template('Analyze'),
                'Evaluate': self._get_long_answer_template('Evaluate'),
                'Create': self._get_long_answer_template('Create')
            },
            'Case Study': {
                'Remember': self._get_case_study_template('Remember'),
                'Understand': self._get_case_study_template('Understand'),
                'Apply': self._get_case_study_template('Apply'),
                'Analyze': self._get_case_study_template('Analyze'),
                'Evaluate': self._get_case_study_template('Evaluate'),
                'Create': self._get_case_study_template('Create')
            }
        }
    
    def _get_long_answer_template(self, bloom_level: str) -> str:
        """Get comprehensive long answer template"""
        templates = {
            'Remember': """
{topic} is a fundamental concept that encompasses several key aspects:

1. Definition and Scope:
{topic} is defined as {definition}. This concept covers {scope_description}.

2. Historical Development:
The development of {topic} has evolved through {historical_phases}.

3. Key Components:
The main components of {topic} include:
- {component_1}
- {component_2}
- {component_3}

4. Fundamental Principles:
The core principles underlying {topic} are:
- {principle_1}
- {principle_2}
- {principle_3}

5. Current Applications:
{topic} is currently applied in {current_applications}.

This comprehensive understanding of {topic} provides the foundation for further analysis and application.
""",
            'Understand': """
Understanding {topic} requires a deep comprehension of its underlying mechanisms and relationships:

1. Conceptual Framework:
{topic} operates within a framework where {conceptual_elements} interact to create {outcome}.

2. Mechanisms and Processes:
The key mechanisms involved in {topic} include:
- {mechanism_1}: {explanation_1}
- {mechanism_2}: {explanation_2}
- {mechanism_3}: {explanation_3}

3. Relationships and Dependencies:
{topic} is closely related to {related_concepts} and depends on {dependencies}.

4. Contextual Factors:
The effectiveness of {topic} is influenced by {contextual_factors}.

5. Practical Implications:
Understanding {topic} has important implications for {practical_applications}.

This understanding enables effective application and analysis of {topic} in various contexts.
""",
            'Apply': """
Applying {topic} effectively requires systematic implementation and practical execution:

1. Application Strategy:
The application of {topic} involves {strategy_description} to achieve {desired_outcome}.

2. Implementation Steps:
Step-by-step implementation includes:
- Step 1: {step_1_description}
- Step 2: {step_2_description}
- Step 3: {step_3_description}
- Step 4: {step_4_description}

3. Practical Considerations:
Key considerations when applying {topic} include:
- {consideration_1}
- {consideration_2}
- {consideration_3}

4. Expected Outcomes:
The application of {topic} should result in {expected_outcomes}.

5. Monitoring and Evaluation:
Success metrics include {success_metrics} to ensure effective implementation.

This systematic approach ensures successful application of {topic} principles.
""",
            'Analyze': """
A comprehensive analysis of {topic} reveals complex interactions and underlying patterns:

1. Structural Analysis:
{topic} consists of {structural_elements} that interact in {interaction_patterns}.

2. Functional Analysis:
The functions of {topic} include:
- {function_1}: {function_description_1}
- {function_2}: {function_description_2}
- {function_3}: {function_description_3}

3. Causal Relationships:
Analysis reveals that {causal_relationships} influence {outcomes}.

4. Comparative Analysis:
When compared to {comparison_basis}, {topic} shows {comparative_insights}.

5. Impact Assessment:
The impact of {topic} on {impact_areas} demonstrates {impact_analysis}.

6. Trend Analysis:
Current trends in {topic} indicate {trend_insights}.

This analysis provides deep insights into the complexity and significance of {topic}.
""",
            'Evaluate': """
Evaluation of {topic} requires systematic assessment of its effectiveness and value:

1. Evaluation Criteria:
The evaluation of {topic} is based on {evaluation_criteria}:
- {criterion_1}: {criterion_description_1}
- {criterion_2}: {criterion_description_2}
- {criterion_3}: {criterion_description_3}

2. Strengths Assessment:
The strengths of {topic} include:
- {strength_1}
- {strength_2}
- {strength_3}

3. Limitations Analysis:
Limitations of {topic} include:
- {limitation_1}
- {limitation_2}
- {limitation_3}

4. Effectiveness Measurement:
Effectiveness is measured through {effectiveness_metrics} showing {effectiveness_results}.

5. Value Proposition:
The value of {topic} lies in {value_proposition}.

6. Recommendations:
Based on evaluation, recommendations include {recommendations}.

This evaluation provides a balanced assessment of {topic}'s effectiveness and value.
""",
            'Create': """
Creating innovative solutions using {topic} requires creative thinking and systematic design:

1. Design Framework:
The creative design framework for {topic} involves {design_elements} to achieve {design_objectives}.

2. Innovative Approaches:
Creative approaches to {topic} include:
- {approach_1}: {approach_description_1}
- {approach_2}: {approach_description_2}
- {approach_3}: {approach_description_3}

3. Solution Development:
The developed solution incorporates {solution_elements} to address {addressed_challenges}.

4. Implementation Strategy:
Implementation involves {implementation_strategy} with {implementation_timeline}.

5. Innovation Features:
Key innovative features include {innovation_features}.

6. Future Potential:
The created solution has potential for {future_applications}.

This creative approach demonstrates the innovative potential of {topic} applications.
"""
        }
        return templates.get(bloom_level, templates['Understand'])
    
    def _get_case_study_template(self, bloom_level: str) -> str:
        """Get case study answer template"""
        base_template = self._get_long_answer_template(bloom_level)
        case_study_prefix = """
Case Study Analysis:

Background:
The case presents {case_background} involving {topic}.

Key Issues:
The main issues identified are:
- {issue_1}
- {issue_2}
- {issue_3}

Analysis Approach:
"""
        return case_study_prefix + base_template
    
    def _load_marking_schemes(self) -> Dict:
        """Load marking schemes for different question types"""
        return {
            'MCQ': {
                'correct_answer': 1.0,
                'explanation': 0.2
            },
            'Short Answer': {
                'key_points': 0.6,
                'explanation': 0.3,
                'clarity': 0.1
            },
            'Long Answer': {
                'comprehensive_coverage': 0.4,
                'logical_structure': 0.2,
                'examples_evidence': 0.2,
                'critical_analysis': 0.15,
                'clarity_expression': 0.05
            },
            'Case Study': {
                'problem_identification': 0.2,
                'analysis_depth': 0.3,
                'solution_proposal': 0.3,
                'justification': 0.15,
                'practical_feasibility': 0.05
            }
        }
    
    def _load_alternative_approaches(self) -> Dict:
        """Load alternative approaches for different topics"""
        return {
            'database': ['relational approach', 'NoSQL approach', 'hybrid approach', 'distributed approach'],
            'algorithm': ['iterative approach', 'recursive approach', 'dynamic programming', 'greedy approach'],
            'system': ['modular approach', 'integrated approach', 'distributed approach', 'centralized approach'],
            'analysis': ['qualitative approach', 'quantitative approach', 'mixed-method approach', 'comparative approach'],
            'design': ['user-centered approach', 'system-centered approach', 'data-driven approach', 'agile approach']
        }
    
    def generate_model_answer(self, question: Dict) -> Dict:
        """Generate comprehensive model answer for a question"""
        qtype = question.get('type', 'Short Answer')
        bloom_level = question.get('bloom_level', 'Understand')
        topic = question.get('topic', 'general topic')
        difficulty = question.get('difficulty', 'Medium')
        
        # Generate main answer
        main_answer = self._generate_main_answer(topic, qtype, bloom_level, difficulty)
        
        # Generate marking scheme
        marking_scheme = self._generate_marking_scheme(qtype, question.get('marks', 5))
        
        # Generate alternative approaches
        alternative_approaches = self._generate_alternative_approaches(topic, qtype, bloom_level)
        
        # Generate key points
        key_points = self._generate_key_points(topic, qtype, bloom_level)
        
        return {
            'main_answer': main_answer,
            'marking_scheme': marking_scheme,
            'alternative_approaches': alternative_approaches,
            'key_points': key_points,
            'expected_length': self._get_expected_length(qtype, bloom_level),
            'common_mistakes': self._get_common_mistakes(topic, qtype),
            'examiner_notes': self._get_examiner_notes(topic, qtype, bloom_level)
        }
    
    def _generate_main_answer(self, topic: str, qtype: str, bloom_level: str, difficulty: str) -> str:
        """Generate the main model answer"""
        template = self.answer_templates.get(qtype, {}).get(bloom_level, '')
        
        if not template:
            template = f"Provide a comprehensive answer about {topic}."
        
        # Replace placeholders
        answer = template.format(
            topic=topic,
            correct_option=self._get_correct_option(topic),
            definition=self._get_definition(topic),
            explanation=self._get_explanation(topic),
            application_logic=self._get_application_logic(topic),
            analysis_reasoning=self._get_analysis_reasoning(topic),
            evaluation_criteria=self._get_evaluation_criteria(topic),
            creative_solution=self._get_creative_solution(topic),
            key_points=self._get_key_points_text(topic),
            significance=self._get_significance(topic),
            application_steps=self._get_application_steps(topic),
            expected_result=self._get_expected_result(topic),
            analysis_points=self._get_analysis_points(topic),
            related_factor=self._get_related_factor(topic),
            relationship_insight=self._get_relationship_insight(topic),
            evaluation_points=self._get_evaluation_points(topic),
            effectiveness_assessment=self._get_effectiveness_assessment(topic),
            creative_elements=self._get_creative_elements(topic),
            addressed_challenges=self._get_addressed_challenges(topic),
            # Additional placeholders for long answers
            scope_description=self._get_scope_description(topic),
            historical_phases=self._get_historical_phases(topic),
            component_1=self._get_component(topic, 1),
            component_2=self._get_component(topic, 2),
            component_3=self._get_component(topic, 3),
            principle_1=self._get_principle(topic, 1),
            principle_2=self._get_principle(topic, 2),
            principle_3=self._get_principle(topic, 3),
            current_applications=self._get_current_applications(topic),
            case_background=self._get_case_background(topic),
            issue_1=self._get_issue(topic, 1),
            issue_2=self._get_issue(topic, 2),
            issue_3=self._get_issue(topic, 3)
        )
        
        return answer
    
    def _generate_marking_scheme(self, qtype: str, total_marks: int) -> Dict:
        """Generate detailed marking scheme"""
        scheme = self.marking_schemes.get(qtype, {})
        marking_details = {}
        
        for criterion, weight in scheme.items():
            marks = int(total_marks * weight)
            marking_details[criterion] = {
                'marks': marks,
                'description': self._get_criterion_description(criterion),
                'indicators': self._get_criterion_indicators(criterion)
            }
        
        return marking_details
    
    def _generate_alternative_approaches(self, topic: str, qtype: str, bloom_level: str) -> List[str]:
        """Generate alternative approaches to the same concept"""
        approaches = []
        
        # Get topic-specific approaches
        topic_key = self._get_topic_key(topic)
        topic_approaches = self.alternative_approaches.get(topic_key, [])
        approaches.extend(topic_approaches)
        
        # Add cognitive level specific approaches
        if bloom_level == 'Apply':
            approaches.extend(['practical implementation', 'hands-on approach', 'experimental method'])
        elif bloom_level == 'Analyze':
            approaches.extend(['systematic analysis', 'comparative study', 'investigative approach'])
        elif bloom_level == 'Evaluate':
            approaches.extend(['critical assessment', 'systematic evaluation', 'comprehensive review'])
        elif bloom_level == 'Create':
            approaches.extend(['innovative design', 'creative solution', 'novel approach'])
        
        return approaches[:5]  # Return top 5 approaches
    
    def _generate_key_points(self, topic: str, qtype: str, bloom_level: str) -> List[str]:
        """Generate key points that should be covered in the answer"""
        key_points = []
        
        # Topic-specific key points
        key_points.extend([
            f"Definition and scope of {topic}",
            f"Key principles of {topic}",
            f"Applications of {topic}",
            f"Benefits and limitations of {topic}"
        ])
        
        # Add cognitive level specific points
        if bloom_level == 'Remember':
            key_points.extend([f"Historical development of {topic}", f"Core components of {topic}"])
        elif bloom_level == 'Understand':
            key_points.extend([f"Mechanisms of {topic}", f"Relationships with other concepts"])
        elif bloom_level == 'Apply':
            key_points.extend([f"Implementation steps for {topic}", f"Practical considerations"])
        elif bloom_level == 'Analyze':
            key_points.extend([f"Structural analysis of {topic}", f"Causal relationships"])
        elif bloom_level == 'Evaluate':
            key_points.extend([f"Strengths and weaknesses of {topic}", f"Effectiveness criteria"])
        elif bloom_level == 'Create':
            key_points.extend([f"Innovative applications of {topic}", f"Future potential"])
        
        return key_points
    
    def _get_expected_length(self, qtype: str, bloom_level: str) -> str:
        """Get expected answer length"""
        if qtype == 'MCQ':
            return "1-2 sentences"
        elif qtype == 'Short Answer':
            return "2-3 paragraphs (100-150 words)"
        elif qtype == 'Long Answer':
            return "4-6 paragraphs (300-500 words)"
        elif qtype == 'Case Study':
            return "6-8 paragraphs (500-800 words)"
        else:
            return "2-3 paragraphs"
    
    def _get_common_mistakes(self, topic: str, qtype: str) -> List[str]:
        """Get common mistakes students make"""
        common_mistakes = [
            f"Confusing {topic} with related concepts",
            "Providing vague or incomplete definitions",
            "Lacking specific examples or evidence",
            "Poor organization and structure"
        ]
        
        if qtype == 'MCQ':
            common_mistakes.extend(["Not reading all options carefully", "Selecting based on keywords only"])
        elif qtype in ['Long Answer', 'Case Study']:
            common_mistakes.extend(["Insufficient depth of analysis", "Missing critical evaluation"])
        
        return common_mistakes
    
    def _get_examiner_notes(self, topic: str, qtype: str, bloom_level: str) -> str:
        """Get examiner notes for grading"""
        notes = f"Look for comprehensive understanding of {topic}. "
        
        if bloom_level == 'Remember':
            notes += "Focus on accurate recall and basic understanding."
        elif bloom_level == 'Understand':
            notes += "Emphasize clear explanation and conceptual grasp."
        elif bloom_level == 'Apply':
            notes += "Check for practical application and implementation."
        elif bloom_level == 'Analyze':
            notes += "Evaluate depth of analysis and critical thinking."
        elif bloom_level == 'Evaluate':
            notes += "Assess quality of evaluation and judgment."
        elif bloom_level == 'Create':
            notes += "Look for creativity and innovative thinking."
        
        return notes
    
    # Helper methods for placeholder replacement
    def _get_correct_option(self, topic: str) -> str:
        return f"the option that best describes {topic}"
    
    def _get_definition(self, topic: str) -> str:
        return f"the systematic approach to {topic} that involves structured methodology"
    
    def _get_explanation(self, topic: str) -> str:
        return f"{topic} operates through established principles and mechanisms"
    
    def _get_application_logic(self, topic: str) -> str:
        return f"the principles of {topic} directly apply to the given scenario"
    
    def _get_analysis_reasoning(self, topic: str) -> str:
        return f"detailed analysis reveals the underlying patterns in {topic}"
    
    def _get_evaluation_criteria(self, topic: str) -> str:
        return f"effectiveness, efficiency, and applicability of {topic}"
    
    def _get_creative_solution(self, topic: str) -> str:
        return f"an innovative approach to {topic} that addresses current challenges"
    
    def _get_key_points_text(self, topic: str) -> str:
        return f"understanding, application, and evaluation of {topic}"
    
    def _get_significance(self, topic: str) -> str:
        return f"it provides essential framework for understanding complex systems"
    
    def _get_application_steps(self, topic: str) -> str:
        return f"identify requirements, design solution, implement, and evaluate"
    
    def _get_expected_result(self, topic: str) -> str:
        return f"improved understanding and practical application of {topic}"
    
    def _get_analysis_points(self, topic: str) -> str:
        return f"structural components, functional relationships, and operational dynamics"
    
    def _get_related_factor(self, topic: str) -> str:
        return f"system performance and organizational efficiency"
    
    def _get_relationship_insight(self, topic: str) -> str:
        return f"interdependencies and mutual influences between components"
    
    def _get_evaluation_points(self, topic: str) -> str:
        return f"effectiveness, efficiency, scalability, and maintainability"
    
    def _get_effectiveness_assessment(self, topic: str) -> str:
        return f"high effectiveness in achieving intended objectives"
    
    def _get_creative_elements(self, topic: str) -> str:
        return f"innovative design, novel approaches, and creative problem-solving"
    
    def _get_addressed_challenges(self, topic: str) -> str:
        return f"current limitations and future requirements"
    
    def _get_scope_description(self, topic: str) -> str:
        return f"various aspects and applications across different domains"
    
    def _get_historical_phases(self, topic: str) -> str:
        return f"several developmental stages from basic concepts to advanced applications"
    
    def _get_component(self, topic: str, num: int) -> str:
        components = [f"core {topic} elements", f"supporting {topic} mechanisms", f"advanced {topic} features"]
        return components[num - 1] if num <= len(components) else f"{topic} component {num}"
    
    def _get_principle(self, topic: str, num: int) -> str:
        principles = [f"fundamental {topic} principles", f"operational {topic} guidelines", f"advanced {topic} concepts"]
        return principles[num - 1] if num <= len(principles) else f"{topic} principle {num}"
    
    def _get_current_applications(self, topic: str) -> str:
        return f"various industries and organizational contexts"
    
    def _get_case_background(self, topic: str) -> str:
        return f"a complex organizational scenario involving {topic}"
    
    def _get_issue(self, topic: str, num: int) -> str:
        issues = [f"implementation challenges with {topic}", f"performance issues related to {topic}", f"integration problems with {topic}"]
        return issues[num - 1] if num <= len(issues) else f"{topic} issue {num}"
    
    def _get_topic_key(self, topic: str) -> str:
        """Extract key topic for approach matching"""
        topic_lower = topic.lower()
        if 'database' in topic_lower or 'dbms' in topic_lower:
            return 'database'
        elif 'algorithm' in topic_lower:
            return 'algorithm'
        elif 'system' in topic_lower:
            return 'system'
        elif 'analysis' in topic_lower:
            return 'analysis'
        elif 'design' in topic_lower:
            return 'design'
        else:
            return 'general'
    
    def _get_criterion_description(self, criterion: str) -> str:
        """Get description for marking criterion"""
        descriptions = {
            'correct_answer': 'Accurate selection of the correct option',
            'explanation': 'Clear and logical explanation of the answer',
            'key_points': 'Coverage of essential points and concepts',
            'comprehensive_coverage': 'Thorough coverage of all relevant aspects',
            'logical_structure': 'Well-organized and coherent structure',
            'examples_evidence': 'Use of relevant examples and evidence',
            'critical_analysis': 'Depth of critical thinking and analysis',
            'clarity_expression': 'Clear and effective communication',
            'problem_identification': 'Accurate identification of key problems',
            'analysis_depth': 'Depth and breadth of analysis',
            'solution_proposal': 'Quality and feasibility of proposed solutions',
            'justification': 'Logical justification of recommendations',
            'practical_feasibility': 'Practicality and implementability of solutions'
        }
        return descriptions.get(criterion, f'Assessment of {criterion}')
    
    def _get_criterion_indicators(self, criterion: str) -> List[str]:
        """Get indicators for marking criterion"""
        indicators = {
            'correct_answer': ['Accurate selection', 'Understanding of concept'],
            'explanation': ['Clear reasoning', 'Logical flow', 'Appropriate detail'],
            'key_points': ['Essential concepts covered', 'Important aspects included'],
            'comprehensive_coverage': ['All relevant topics addressed', 'Depth of coverage'],
            'logical_structure': ['Clear organization', 'Coherent flow', 'Logical progression'],
            'examples_evidence': ['Relevant examples', 'Supporting evidence', 'Practical applications'],
            'critical_analysis': ['Deep analysis', 'Critical evaluation', 'Insightful observations'],
            'clarity_expression': ['Clear writing', 'Effective communication', 'Appropriate terminology']
        }
        return indicators.get(criterion, ['Quality of response', 'Understanding demonstrated']) 