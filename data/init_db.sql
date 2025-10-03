DROP SCHEMA IF EXISTS ensaiGPT CASCADE;
CREATE SCHEMA ensaiGPT;

--------------------------------------------------------------
-- Utilisateur
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.utilisateur CASCADE ;
CREATE TABLE ensaiGPT.utilisateur (
    id_utilisateur serial PRIMARY KEY,
    nom_utilisateur text UNIQUE NOT NULL,
    mot_de_passe_hache text 
);

--------------------------------------------------------------
-- Conversation
--------------------------------------------------------------

DROP TABLE IF EXISTS ensaiGPT.conversation CASCADE ;
CREATE TABLE ensaiGPT.conversation (
    id_conversation serial PRIMARY KEY,
    id_utilisateur integer REFERENCES ensaiGPT.utilisateur(id_utilisateur),
    titre text,
    date_debut date,
    date_dernier_message date,
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
    date_envoi date,
    role_auteur text, 
    contenu text

);
