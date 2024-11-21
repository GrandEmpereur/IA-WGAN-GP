import base64
import os
import random
import torch
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS
from model import Generator
from PIL import Image
import io

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Chemins des modèles et datasets
MODEL_PATH = "./saved_models/wgan_gp_final.pth"
IMAGE_FOLDER = "./celeb_dataset/images"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Le modèle PyTorch est introuvable : {MODEL_PATH}")
if not os.path.exists(IMAGE_FOLDER):
    raise FileNotFoundError(f"Le dossier des images réelles est introuvable : {IMAGE_FOLDER}")

print(f"Chargement du modèle PyTorch depuis {MODEL_PATH}...")

# Paramètres du modèle
Z_DIM = 100
CHANNELS_IMG = 3
FEATURES_GEN = 16

# Charger le générateur
gen = Generator(Z_DIM, CHANNELS_IMG, FEATURES_GEN)
checkpoint = torch.load(MODEL_PATH, map_location="cpu")
gen.load_state_dict(checkpoint["generator"])
gen.eval()
print("Modèle PyTorch chargé avec succès.")

# Charger les images réelles
real_images = [
    os.path.join(IMAGE_FOLDER, img) for img in os.listdir(IMAGE_FOLDER) if img.endswith((".png", ".jpg", ".jpeg"))
]
if not real_images:
    raise ValueError("Aucune image trouvée dans le dossier des images réelles.")

print(f"{len(real_images)} images réelles chargées.")

def load_real_image(image_path):
    """Charge une image réelle depuis le dossier et la convertit en base64."""
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{base64_image}"

def generate_fake_image():
    """Génère une image avec le modèle et la convertit en base64."""
    noise = torch.randn(1, Z_DIM, 1, 1)
    with torch.no_grad():
        output = gen(noise).squeeze(0)
    output_image = (output.permute(1, 2, 0).numpy() + 1) / 2 * 255
    output_image = Image.fromarray(output_image.astype(np.uint8))

    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return f"data:image/png;base64,{base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')}"

@app.route("/get-images", methods=["GET"])
def get_images():
    """Sélectionne aléatoirement 20 images entre réelles et générées."""
    try:
        # Mélanger des images réelles et générées
        num_real = random.randint(5, 15)  # Par exemple, entre 5 et 15 images réelles
        num_fake = 20 - num_real

        selected_real_images = random.sample(real_images, num_real)
        selected_fake_images = [generate_fake_image() for _ in range(num_fake)]

        # Associer chaque image à son type
        images = [{"image": load_real_image(img), "is_real": True} for img in selected_real_images]
        images += [{"image": img, "is_real": False} for img in selected_fake_images]

        # Mélanger toutes les images
        random.shuffle(images)

        return jsonify({"images": images})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
