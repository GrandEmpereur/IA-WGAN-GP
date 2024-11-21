"""
Training of WGAN-GP with model and generated images saving, including saving final epoch images.
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
from utils import gradient_penalty, save_checkpoint, load_checkpoint
from model import Discriminator, Generator, initialize_weights

# Hyperparameters etc.
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
LEARNING_RATE = 1e-4
BATCH_SIZE = 64
IMAGE_SIZE = 64
CHANNELS_IMG = 3
Z_DIM = 100
NUM_EPOCHS = 10
FEATURES_CRITIC = 16
FEATURES_GEN = 16
CRITIC_ITERATIONS = 5
LAMBDA_GP = 10
git commit -m "first commit"
# Dossier pour sauvegarder les images générées
GENERATED_IMAGES_DIR = "./dataset/generated/images"
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

# Dossier pour sauvegarder les modèles
SAVED_MODELS_DIR = "./saved_models"
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

# Logs pour TensorBoard
LEARNING_CURVES_DIR = "./logs/learns"
os.makedirs(LEARNING_CURVES_DIR, exist_ok=True)

# Transformation des données
transforms = transforms.Compose(
    [
        transforms.Resize(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.5 for _ in range(CHANNELS_IMG)], [0.5 for _ in range(CHANNELS_IMG)]
        ),
    ]
)

# Charger le dataset
dataset = datasets.ImageFolder(root="celeb_dataset", transform=transforms)
loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
)

# Initialisation des modèles
gen = Generator(Z_DIM, CHANNELS_IMG, FEATURES_GEN).to(device)
critic = Discriminator(CHANNELS_IMG, FEATURES_CRITIC).to(device)
initialize_weights(gen)
initialize_weights(critic)

# Optimiseurs
opt_gen = optim.Adam(gen.parameters(), lr=LEARNING_RATE, betas=(0.0, 0.9))
opt_critic = optim.Adam(critic.parameters(), lr=LEARNING_RATE, betas=(0.0, 0.9))

# TensorBoard Writers
writer_real = SummaryWriter(f"logs/GAN_MNIST/real")
writer_fake = SummaryWriter(f"logs/GAN_MNIST/fake")
writer_learns = SummaryWriter(LEARNING_CURVES_DIR)
step = 0

# Bruit fixe pour générer des images constantes
fixed_noise = torch.randn(32, Z_DIM, 1, 1).to(device)

gen.train()
critic.train()

# Entraînement
for epoch in range(NUM_EPOCHS):
    for batch_idx, (real, _) in enumerate(tqdm(loader)):
        real = real.to(device)
        cur_batch_size = real.shape[0]

        # Entraîner le Critic
        for _ in range(CRITIC_ITERATIONS):
            noise = torch.randn(cur_batch_size, Z_DIM, 1, 1).to(device)
            fake = gen(noise)
            critic_real = critic(real).reshape(-1)
            critic_fake = critic(fake).reshape(-1)
            gp = gradient_penalty(critic, real, fake, device=device)
            loss_critic = (
                -(torch.mean(critic_real) - torch.mean(critic_fake)) + LAMBDA_GP * gp
            )
            critic.zero_grad()
            loss_critic.backward(retain_graph=True)
            opt_critic.step()

        # Entraîner le Generator
        gen_fake = critic(fake).reshape(-1)
        loss_gen = -torch.mean(gen_fake)
        gen.zero_grad()
        loss_gen.backward()
        opt_gen.step()

        # Afficher les pertes périodiquement
        if batch_idx % 100 == 0 and batch_idx > 0:
            print(
                f"Epoch [{epoch}/{NUM_EPOCHS}] Batch {batch_idx}/{len(loader)} \
                  Loss Critic: {loss_critic:.4f}, Loss Generator: {loss_gen:.4f}"
            )

            # Ajouter les pertes dans TensorBoard
            writer_learns.add_scalar("Loss/Critic", loss_critic.item(), global_step=step)
            writer_learns.add_scalar("Loss/Generator", loss_gen.item(), global_step=step)

            # Générer des images et les sauvegarder dans TensorBoard
            with torch.no_grad():
                fake = gen(fixed_noise)
                img_grid_real = torchvision.utils.make_grid(real[:32], normalize=True)
                img_grid_fake = torchvision.utils.make_grid(fake[:32], normalize=True)

                writer_real.add_image("Real", img_grid_real, global_step=step)
                writer_fake.add_image("Fake", img_grid_fake, global_step=step)

            step += 1

    # Sauvegarder les modèles après chaque epoch
    torch.save(gen.state_dict(), os.path.join(SAVED_MODELS_DIR, f"generator_epoch_{epoch}.pth"))
    torch.save(critic.state_dict(), os.path.join(SAVED_MODELS_DIR, f"critic_epoch_{epoch}.pth"))
    print(f"Modèles sauvegardés pour l'epoch {epoch}")

    # Sauvegarder les images générées uniquement pour la dernière époque
    if epoch == NUM_EPOCHS - 1:
        print("Sauvegarde des images générées pour la dernière époque...")
        with torch.no_grad():
            final_fake_images = gen(fixed_noise)
            for i in range(final_fake_images.size(0)):
                save_image_path = os.path.join(GENERATED_IMAGES_DIR, f"final_epoch_img_{i}.png")
                torchvision.utils.save_image(final_fake_images[i], save_image_path, normalize=True)

# Fin de l'entraînement
print("Entraînement terminé.")
