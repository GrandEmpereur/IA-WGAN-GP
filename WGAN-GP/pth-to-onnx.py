import torch
import onnx
from model import Generator

# Paramètres du modèle
Z_DIM = 100
CHANNELS_IMG = 3
FEATURES_GEN = 16

# Charger le modèle
model_path = "./saved_models/wgan_gp_final.pth"
onnx_path = "./saved_models/generator.onnx"

checkpoint = torch.load(model_path)
gen = Generator(Z_DIM, CHANNELS_IMG, FEATURES_GEN)
gen.load_state_dict(checkpoint["generator"])
gen.eval()

# Créer un bruit d'entrée factice
dummy_input = torch.randn(1, Z_DIM, 1, 1)

# Convertir en ONNX
torch.onnx.export(
    gen,
    dummy_input,
    onnx_path,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=11,
)

print(f"Modèle exporté en ONNX : {onnx_path}")
