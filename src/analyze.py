from typing import List, Dict
from collections import Counter

def compute_analytics(questions: List[Dict]) -> Dict:
    """Compute analytics: count per type, Bloom's level, and topic."""
    type_counts = Counter(q['type'] for q in questions)
    bloom_counts = Counter(q['bloom_level'] for q in questions)
    topic_counts = Counter(q['topic'] for q in questions)
    return {
        'type_counts': type_counts,
        'bloom_counts': bloom_counts,
        'topic_counts': topic_counts
    }

def compute_topic_frequency(tagged_questions):
    topic_counts = Counter(topic for _, topic in tagged_questions)
    return topic_counts 