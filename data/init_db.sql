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

DROP TABLE IF EXISTS ensaiGPT.conversation CASCADE ;
CREATE TABLE ensaiGPT.conversation (
    id_conversation serial PRIMARY KEY,
    id_user integer REFERENCES ensaiGPT.user(id_user),
    title text,
    date_first_message date,
    date_last_message date,
    max_token integer,
    top_p numeric,
    temperature numeric
);

--------------------------------------------------------------
-- Message 
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.message CASCADE ;
CREATE TABLE ensaiGPT.message (
    id_message serial PRIMARY KEY,
    id_conversation integer REFERENCES ensaiGPT.conversation(id_conversation),
    date_sending date,
    role_author text, 
    content text

);
