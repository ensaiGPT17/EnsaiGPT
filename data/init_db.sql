DROP SCHEMA IF EXISTS ensaiGPT CASCADE;
CREATE SCHEMA ensaiGPT;

--------------------------------------------------------------
-- Utilisateur
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.user CASCADE ;
CREATE TABLE ensaiGPT.user (
    id_user serial PRIMARY KEY,
    username text UNIQUE NOT NULL,
    hashed_password text 
);

--------------------------------------------------------------
-- Conversation
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.chat CASCADE ;
CREATE TABLE ensaiGPT.chat (
    id_chat serial PRIMARY KEY,
    id_user integer REFERENCES ensaiGPT.user(id_user),
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

DROP TABLE IF EXISTS ensaiGPT.message CASCADE ;
CREATE TABLE ensaiGPT.message (
    id_message serial PRIMARY KEY,
    id_chat integer REFERENCES ensaiGPT.chat(id_chat),
    date_sending date,
    role_author text, 
    content text

);
