from app.rag import query_rag


def is_vague(query):
    words = query.lower().split()

    # if query is too short → vague
    if len(words) < 4:
        return True

    # check if meaningful keywords exist
    meaningful_keywords = ["data", "analyst", "developer", "skills", "numerical", "coding"]

    if any(word in words for word in meaningful_keywords):
        return False

    return False

def is_comparison(query):
    keywords = ["compare", "difference", "vs"]
    return any(k in query.lower() for k in keywords)


def generate_response(user_query):
    # 1. Vague → ask questions
    if is_vague(user_query):
        return {
            "type": "clarification",
            "message": "Can you specify the role, skills, or experience level you're hiring for?"
        }

    # 2. Comparison
    if is_comparison(user_query):
        return {
            "type": "comparison",
            "message": "Comparison feature coming soon (basic version built)."
        }

    # 3. Recommendation (main logic)
    results = query_rag(user_query)

    recommendations = []
    for r in results:
        metadata = r.metadata
        recommendations.append({
            "name": metadata["title"],
            "description": metadata["description"]
        })

    return {
        "type": "recommendation",
        "recommendations": recommendations
    }