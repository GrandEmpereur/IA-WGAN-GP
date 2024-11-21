import base64
import os
import torch
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importer Flask-CORS
from model import Generator  # Importer le modèle
from PIL import Image
import io

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Charger le modèle PyTorch
MODEL_PATH = "./saved_models/wgan_gp_final.pth"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Le modèle PyTorch est introuvable : {MODEL_PATH}")

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

# Endpoint pour générer des images
@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        # Générer une image à partir du modèle
        noise = torch.randn(1, Z_DIM, 1, 1)
        with torch.no_grad():
            output = gen(noise).squeeze(0)
        output_image = (output.permute(1, 2, 0).numpy() + 1) / 2 * 255
        output_image = Image.fromarray(output_image.astype(np.uint8))

        # Convertir l'image en base64
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        base64_image = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

        # Retourner une URL Base64 complète
        return jsonify({"image": f"data:image/png;base64,{base64_image}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
