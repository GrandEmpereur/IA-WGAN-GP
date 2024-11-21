from PIL import Image
import os

# Dossiers
input_folder = "./celeb_dataset/images"  # Dossier contenant vos images
output_folder = "./images"  # Dossier où sauvegarder les images redimensionnées
target_size = (64, 64)  # Taille cible (par exemple, 78x78)

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Parcourir toutes les images du dossier
for filename in os.listdir(input_folder):
    if filename.endswith((".png", ".jpg", ".jpeg")):  # Filtrer les fichiers images
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Ouvrir l'image et la redimensionner
        with Image.open(input_path) as img:
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)  # Redimensionner
            resized_img.save(output_path)  # Sauvegarder l'image redimensionnée
            print(f"Image {filename} redimensionnée et sauvegardée sous {output_path}")

print("Toutes les images ont été redimensionnées.")
