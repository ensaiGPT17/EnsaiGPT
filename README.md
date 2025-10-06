Projet 2A ENSAI

# 💬 Projet ENSAI GPT

Ce projet est une application en ligne de commande qui permet d’interagir avec une base de données PostgreSQL à l’aide d’une interface utilisateur simple basée sur **InquirerPy**.  
Il permet de gérer des utilisateurs, leurs conversations et les messages associés, le tout dans une structure claire et testable.

---

## ⚙️ Préparation avant exécution

Avant de lancer le projet, suis attentivement les étapes suivantes :

### 1. 🐍 Créer et activer un environnement virtuel

Il est recommandé d’utiliser un environnement virtuel pour isoler les dépendances du projet.

```bash
# Création de l’environnement
python -m venv venv

# Activation sous Windows
venv\Scripts\activate

# Activation sous macOS / Linux
source venv/bin/activate
```

### 2. 📦 Installer les dépendances

Installe les bibliothèques nécessaires à partir du fichier requirements.txt :

```bash
pip install -r requirements.txt
```

### 3. 🗄️ Configurer la base de données PostgreSQL
Crée un fichier .env à la racine du projet et ajoute-y les informations suivantes :

```bash
POSTGRES_HOST= 
POSTGRES_DATABASE= 
POSTGRES_USER= 
POSTGRES_PASSWORD=
POSTGRES_PORT=
```

### 4. 🧱 Initialiser le schéma de la base de données
Réuinitialiser la base de données en exécutant ceci.
```bash
python -m utils.reset_database
```


### 5. 🧪 (Optionnel) Lancer les tests unitaires

Pour vérifier que tout fonctionne correctement, exécute les tests avec pytest :

```bash
pytest
```

### 6. ▶️ Lancer l’application

Une fois toutes les étapes précédentes effectuées, lance le programme principal en étant dans */src*:
```bash
python -m main
```