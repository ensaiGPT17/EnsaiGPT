DROP SCHEMA IF EXISTS ensaiGPTTEST CASCADE;
CREATE SCHEMA ensaiGPTTEST;

--------------------------------------------------------------
-- Utilisateur
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPTTEST.users CASCADE ;
CREATE TABLE ensaiGPTTEST.users (
    id_user serial PRIMARY KEY,
    username text UNIQUE NOT NULL,
    hashed_password text 
);

--------------------------------------------------------------
-- Conversation
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPTTEST.chats CASCADE ;
CREATE TABLE ensaiGPTTEST.chats (
    id_chat serial PRIMARY KEY,
    id_user integer REFERENCES ensaiGPTTEST.users(id_user) ON DELETE CASCADE,
    title text,
    date_start timestamp,
    last_date timestamp,
    max_tokens integer,
    top_p numeric,
    temperature numeric
);

--------------------------------------------------------------
-- Message 
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPTTEST.messages CASCADE ;
CREATE TABLE ensaiGPTTEST.messages (
    id_message serial PRIMARY KEY,
    id_chat integer REFERENCES ensaiGPTTEST.chats(id_chat) ON DELETE CASCADE,
    date_sending timestamp,
    role_author text, 
    content text

);