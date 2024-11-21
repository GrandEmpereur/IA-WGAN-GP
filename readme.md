# **Fake vs Real Image Game**

Un projet basé sur **Flask**, **PyTorch**, et **Next.js** qui permet de :
1. Générer des images à l'aide d'un modèle **WGAN-GP**.
2. Afficher ces images sur une interface web interactive.
3. Permettre aux utilisateurs de jouer à un jeu pour deviner si une image est réelle ou générée.

---

## **Fonctionnalités**

- **API Flask** :  
  Fournit un endpoint pour générer des images à partir du modèle PyTorch.

- **Interface Web** :  
  Une interface Next.js utilisant **shadcn/ui** pour afficher des images et jouer au mini-jeu.

- **Mini-Jeu** :  
  Les utilisateurs doivent identifier les images générées par rapport aux images réelles.

---

## **Prérequis**

- **Python 3.9+**
- **Node.js 20+**
- **PyTorch**
- **Flask**
- **Next.js**

---

## **Installation**

### **1. Backend Flask**

Clonez le projet et installez les dépendances Python :

```bash
git clone <URL_DU_REPO>
cd fake-vs-real-game/backend
pip install -r requirements.txt
```

#### Convertir le modèle PyTorch

Assurez-vous que votre modèle est déjà entraîné. Placez le modèle dans le dossier `saved_models/` avec le nom `wgan_gp_final.pth`.

#### Lancer l'API Flask

```bash
python app.py
```

L'API sera disponible sur `http://localhost:8000`.

---

### **2. Frontend Next.js**

Installez les dépendances Node.js :

```bash
cd ../frontend
npm install
```

Lancez le serveur Next.js :

```bash
npm run dev
```

L'interface sera disponible sur `http://localhost:3000`.

---

## **Utilisation**

1. Accédez à `http://localhost:3000/` pour accéder à l'interface du jeu.
2. Cliquez sur **Commencer** pour générer une image à partir de l'API Flask.
3. Devinez si l'image est "réelle" ou "générée" en cliquant sur les boutons **Réel** ou **Généré**.
4. Le score sera mis à jour en fonction de vos réponses.

---

## **Structure du Projet**

```plaintext
fake-vs-real-game/
├── backend/                   # Backend Flask
│   ├── app.py                 # API Flask pour la génération d'images
│   ├── saved_models/          # Modèle PyTorch
│   └── dataset/               # Datasets (réels et générés)
├── frontend/                  # Frontend Next.js
│   ├── pages/                 # Pages Next.js
│   ├── public/                # Fichiers statiques (images, etc.)
│   └── components/            # Composants React
└── README.md                  # Documentation du projet
```

---

## **Endpoints**

### **API Flask**

#### **POST /generate**
Génère une image à partir du modèle PyTorch.

- **Requête** :
  Aucun paramètre requis.

- **Réponse** :
  ```json
  {
    "image": "data:image/png;base64,encoded_image"
  }
  ```

---

## **Améliorations Futures**

- Ajouter des classements pour le mini-jeu.
- Enregistrer les statistiques des utilisateurs (nombre de bonnes réponses, temps, etc.).
- Étendre le support à d'autres types d'images générées.
- Permettre une intégration avec des modèles plus récents via ONNX.

---

## **Auteurs**

- **Votre Nom**
- Contributeurs : *Bartosik Patrick*

---

## **Licence**

Ce projet est sous licence [MIT](LICENSE).