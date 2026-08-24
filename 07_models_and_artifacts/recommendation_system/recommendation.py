from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_resources(user_vector, resource_vectors):
    similarities = cosine_similarity([user_vector], resource_vectors)
    return np.argsort(similarities[0])[::-1]