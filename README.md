Projet 2A ENSAI

# 💬 Projet ENSAI GPT

....
---

## ⚙️ Préparation avant exécution

Placez vous à la racine du projet, puis suivez attentivement les étapes suivantes :

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

Installez les bibliothèques nécessaires à partir du fichier requirements.txt :

```bash
pip install -r requirements.txt
```

### 3. 🗄️ Configurer la base de données PostgreSQL et l'API
Créez un fichier .env à la racine du projet et ajoutez-y les informations suivantes :

```bash
POSTGRES_HOST= 
POSTGRES_DATABASE= 
POSTGRES_USER= 
POSTGRES_PASSWORD=
POSTGRES_PORT=

ENSAI_GPT_HOST=
```

Puis ajoutez .env dans les variables d'environnement :
Bash / Zsh : 
```bash
export DOTENV=".env"
```
PowerShell : 
```powershell
$ENV:DOTENV = ".env"
 ```

### 4. 🧪 (Optionnel) Lancer les tests unitaires

Pour vérifier que tout fonctionne correctement, vous pouvez exécuter les tests avec pytest :

```bash
python -m pytest
```

### 5. ▶️ Lancer l’application

**Ajoutez 'src/' aux chemins** (PYTHONPATH) : 

Bash / Zsh :
```bash
export PYTHONPATH="src"
```
PowerShell : 
```powershell
$ENV:PYTHONPATH = "src"
 ```

Une fois toutes les étapes précédentes effectuées, lance le programme principal:
```bash
python -m main
```

### 6. 🧱 (Optionnel) Réinitialiser le schéma de la base de données
**La base de données s'initialisera automatiquement au premier lancement** de l'application. Vous pouvez toutefois la réinitialiser en utilisant :
```bash
python -m utils.reset_database
```

