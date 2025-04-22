import numpy as np
from django.conf import settings
from clarifai.client.model import Model

# Задаваме публичния Clarifai модел за embedding
model = Model(
    model_id="general-image-embedding",
    user_id="clarifai",
    app_id="main",
    pat=settings.CLARIFAI_PAT
)

def get_image_embedding(image_path):
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = model.predict_by_bytes(image_bytes, input_type="image")

        embedding = response.outputs[0].data.embeddings[0].vector
        return list(embedding)

    except Exception as e:
        print(f"❌ Clarifai embedding error: {e}")
        return [0.0] * 1024


def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0

    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return float(np.clip(similarity, 0.0, 1.0))
