# 💬 Projet ENSAI GPT

....
---

## ⚙️ Preparation before execution

Place yourself at the root of the project, then carefully follow the steps below:

### 1. (Recommended) Create and activate a virtual environment

It is recommended to use a virtual environment to isolate the project dependencies.

Creating the environment:
```
python -m venv venv
```
Activate: 

Bash / Zsh
```bash
source venv/bin/activate
```
PowerShell
```powershell
.\venv\Scripts\activate
```


### 2. Install the dependencies

Install the required libraries from the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 3. Configure the PostgreSQL database and the API
Create a .env file at the root of the project and add the following information:

```bash
POSTGRES_HOST= 
POSTGRES_DATABASE= 
POSTGRES_USER= 
POSTGRES_PASSWORD=
POSTGRES_PORT=

ENSAI_GPT_HOST=
```

Then add .env to the environment variables:

Bash / Zsh
```bash
export DOTENV=".env"
```
PowerShell
```powershell
$ENV:DOTENV = ".env"
 ```

### 4. (Optional) Run the tests

To check that everything is working correctly, you can run the tests with pytest:

```bash
python -m pytest
```

### 5. ▶️ Lancer l’application

**Add 'src/' to the paths** (PYTHONPATH) : 

Bash / Zsh
```bash
export PYTHONPATH="src"
```
PowerShell
```powershell
$ENV:PYTHONPATH = "src"
 ```

Once all the previous steps are completed, you can run the main program:
```bash
python -m main
```

### 6. 🧱 (Optional) Reset the database schema
**The database will initialize automatically on the first launch** of the application. However, you can reset it using:

```bash
python -m utils.reset_database
```

