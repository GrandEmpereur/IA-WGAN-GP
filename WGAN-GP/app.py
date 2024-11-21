import os
import numpy as np
from flask import Flask, request, jsonify
import onnxruntime as ort
from PIL import Image
import io

# Initialisation de l'application Flask
app = Flask(__name__)

# Charger le modèle ONNX
ONNX_MODEL_PATH = "./saved_models/generator.onnx"
if not os.path.exists(ONNX_MODEL_PATH):
    raise FileNotFoundError(f"Le modèle ONNX est introuvable : {ONNX_MODEL_PATH}")

print(f"Chargement du modèle ONNX depuis {ONNX_MODEL_PATH}...")
onnx_session = ort.InferenceSession(ONNX_MODEL_PATH)
print("Modèle ONNX chargé avec succès.")

# Endpoint pour générer des images
@app.route("/generate", methods=["POST"])
def generate_image():
    """
    Génère une image à partir d'un bruit aléatoire.
    """
    try:
        # Créer un bruit aléatoire pour l'entrée
        z_dim = 100
        noise = np.random.randn(1, z_dim, 1, 1).astype(np.float32)

        # Faire la prédiction
        output = onnx_session.run(None, {"input": noise})[0]

        # Convertir la sortie en image
        output_image = (output.squeeze(0).transpose(1, 2, 0) + 1) / 2 * 255
        output_image = Image.fromarray(output_image.astype(np.uint8))

        # Retourner l'image au format PNG
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return jsonify({"image": img_byte_arr.getvalue().decode("latin1")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
