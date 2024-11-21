# **Fake vs Real Image Game**

Un projet basé sur **Flask**, **ONNX**, et **Next.js** qui permet de :
1. Générer des images à l'aide d'un modèle **WGAN-GP** converti en **ONNX**.
2. Afficher ces images sur une interface web interactive.
3. Permettre aux utilisateurs de jouer à un jeu pour deviner si une image est réelle ou générée.

---

## **Fonctionnalités**

- **API Flask** :  
  Fournit un endpoint pour générer des images à partir du modèle ONNX.

- **Interface Web** :  
  Une interface Next.js utilisant **shadcn/ui** pour afficher des images et jouer au mini-jeu.

- **Support ONNX** :  
  Les prédictions sont effectuées via **ONNX Runtime**.

- **Mini-Jeu** :  
  Les utilisateurs doivent identifier les images générées par rapport aux images réelles.

---

## **Prérequis**

- **Python 3.8+**
- **Node.js 16+**
- **PyTorch**
- **ONNX Runtime**
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

#### Convertir le modèle PyTorch en ONNX

Assurez-vous que votre modèle est déjà entraîné. Puis, exécutez le script suivant pour convertir votre modèle en ONNX :

```bash
python convert_to_onnx.py
```

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

1. Accédez à `http://localhost:3000/generate` pour générer des images à partir de l'API Flask.
2. Jouez au mini-jeu pour deviner si une image est "réelle" ou "générée".
3. Les résultats sont affichés en temps réel.

---

## **Structure du Projet**

```plaintext
fake-vs-real-game/
├── backend/                   # Backend Flask
│   ├── app.py                 # API Flask pour la génération d'images
│   ├── convert_to_onnx.py     # Script pour convertir le modèle PyTorch en ONNX
│   ├── saved_models/          # Modèles PyTorch et ONNX
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
Génère une image à partir du modèle ONNX.

- **Requête** :
  Aucun paramètre requis.

- **Réponse** :
  ```json
  {
    "image": "base64_encoded_image"
  }
  ```

---

## **Améliorations Futures**

- Ajouter des classements pour le mini-jeu.
- Enregistrer les statistiques des utilisateurs (nombre de bonnes réponses, temps, etc.).
- Étendre le support à d'autres types d'images générées.

---

## **Auteurs**

- **Votre Nom**
- Contributeurs : *Bartosik Patrick*

---

## **Licence**

Ce projet est sous licence [MIT](LICENSE).

---