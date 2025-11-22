# ENSAI GPT

## Presentation of the Application

**ensaiGPT** is a conversational AI application designed to provide an interactive experience for all users. Built around a language model accessible via an API, the application allows users to engage in conversations with an AI assistant, manage their conversation history, and customize the assistant's behavior.

### Key Features

- **User Account Management**
  - Users can create an account with a username and password to access their personal space.
  - Secure authentication ensures that user data is protected, with passwords stored in hashed form.

- **Conversation Management**
  - Start new conversations with default or custom settings.
  - Send and receive messages with the AI assistant.
  - Continue past conversations from the user's history.

- **Search and Retrieval**
  - Search for previous conversations by keywords in titles or by creation date.
  - The search algorithm tolerates minor spelling errors for improved usability.

- **Customization**
  - You can configure the AI assistant’s behavior using parameters:
    - `max_tokens`: maximum length of responses
    - `top_p`: controls diversity of word choices
    - `temperature`: controls creativity and variability
    - Context instruction: guides the assistant’s overall behavior

- **Statistics**
  - View personalized statistics, including:
    - Number of conversations
    - Total and average messages per conversation
    - Dates of first and last conversation

- **Export and Backup**
  - Export conversations to TXT or PDF formats for offline use.
  - All exported files are organized in an `exports` folder.

- **Deletion**
  - Delete individual conversations or all conversations at once to manage storage and privacy.
  - Users can also delete their account.

---

## Preparation before execution

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

### 5. Run the application

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

### 6. (Optional) Reset the database schema
**The database will initialize automatically on the first launch** of the application. However, you can reset it using:

```bash
python -m utils.reset_database
```

