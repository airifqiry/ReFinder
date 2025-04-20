import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity as skl_cosine_similarity
from pathlib import Path
import base64
import io

# === ЛОКАЛНА симулация на embedding генератор ===
def get_image_embedding(image_path):
    
    try:
        img = Image.open(image_path).resize((64, 64)).convert('RGB')
        img_array = np.array(img)
        mean_rgb = img_array.mean(axis=(0, 1))  # Среден цвят по всички пиксели
        return mean_rgb.tolist()  # [R, G, B] стойности
    except Exception as e:
        print(f"❌ Грешка при отваряне на изображение: {e}")
        return [0.0, 0.0, 0.0]  # fallback embedding


def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)

    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0

    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return float(np.clip(similarity, 0.0, 1.0))  
