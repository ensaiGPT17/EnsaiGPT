DROP SCHEMA IF EXISTS ensaiGPT CASCADE;
CREATE SCHEMA ensaiGPT;

--------------------------------------------------------------
-- Utilisateur
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.users CASCADE ;
CREATE TABLE ensaiGPT.users (
    id_user serial PRIMARY KEY,
    username text UNIQUE NOT NULL,
    hashed_password text 
);

--------------------------------------------------------------
-- Conversation
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.chats CASCADE ;
CREATE TABLE ensaiGPT.chats (
    id_chat serial PRIMARY KEY,
    id_user integer REFERENCES ensaiGPT.users(id_user) ON DELETE CASCADE,
    title text,
    date_start date,
    last_date date,
    max_tokens integer,
    top_p numeric,
    temperature numeric
);

--------------------------------------------------------------
-- Message 
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.messages CASCADE ;
CREATE TABLE ensaiGPT.messages (
    id_message serial PRIMARY KEY,
    id_chat integer REFERENCES ensaiGPT.chats(id_chat) ON DELETE CASCADE,
    date_sending date,
    role_author text, 
    content text

);
