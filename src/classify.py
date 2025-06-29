from typing import List, Tuple

def tag_questions_by_topic(questions: List[str], topics: List[str]) -> List[Tuple[str, str]]:
    tagged = []
    for q in questions:
        found = False
        for topic in topics:
            if topic.lower() in q.lower():
                tagged.append((q, topic))
                found = True
                break
        if not found:
            tagged.append((q, 'Unknown'))
    return tagged 