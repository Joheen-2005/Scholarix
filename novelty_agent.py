from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Common research topics (baseline corpus)
COMMON_RESEARCH_TOPICS = [
    "Deep Learning for Image Classification",
    "Natural Language Processing using Transformers",
    "Blockchain for Secure Transactions",
    "Internet of Things in Smart Cities",
    "Cloud Computing Architecture",
    "Federated Learning for Privacy",
    "Cybersecurity Threat Detection",
    "Reinforcement Learning Algorithms",
    "Data Mining Techniques",
    "Computer Vision Object Detection"
]

def compute_novelty(user_topic):

    corpus = COMMON_RESEARCH_TOPICS + [user_topic]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Compare user topic (last index) with all others
    similarities = similarity_matrix[-1][:-1]

    max_similarity = max(similarities)

    # Novelty score
    novelty_score = (1 - max_similarity) * 100

    return round(novelty_score, 2)