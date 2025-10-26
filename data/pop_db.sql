--------------------------------------------------------------
-- Peuplement de la base ensaiGPT
--------------------------------------------------------------

-- On insère d’abord quelques utilisateurs
INSERT INTO ensaiGPT.users (username, hashed_password)
VALUES
    ('bruno', '1234'),
    ('sarah_dev', 'hashed_pwd_456'),
    ('marc_ai', 'hashed_pwd_789');

--------------------------------------------------------------
-- Conversations
--------------------------------------------------------------

INSERT INTO ensaiGPT.chats (id_user, title, date_start, last_date, max_tokens, top_p, temperature)
VALUES
    (1, 'Data Analysis Project', '2025-09-28', '2025-09-30', 4096, 0.9, 0.7),
    (1, 'Operations Research Help', '2025-10-01', '2025-10-02', 4096, 1.0, 0.8),
    (2, 'Python Debugging', '2025-10-03', '2025-10-03', 2048, 0.8, 0.6),
    (3, 'Machine Learning Basics', '2025-09-29', '2025-09-30', 4096, 0.95, 0.75);

--------------------------------------------------------------
-- Messages
--------------------------------------------------------------

INSERT INTO ensaiGPT.messages (id_chat, date_sending, role_author, content)
VALUES
    -- Conversation 1 (Bruno)
    (1, '2025-09-28', 'user', 'Hi, can you help me analyze sales data using Python?'),
    (1, '2025-09-28', 'assistant', 'Of course, Bruno! Do you already have the dataset ready?'),
    (1, '2025-09-29', 'user', 'Yes, it contains sales from January to June. I want to visualize trends.'),
    (1, '2025-09-30', 'assistant', 'You can use Matplotlib and Seaborn for that. Let me show you an example code.'),

    -- Conversation 2 (Bruno)
    (2, '2025-10-01', 'user', 'Can you explain the difference between linear and integer programming?'),
    (2, '2025-10-01', 'assistant', 'Sure! Linear programming allows continuous variables, while integer programming restricts them to integers.'),
    (2, '2025-10-02', 'user', 'Got it. So integer programming is used for discrete decisions, right?'),
    (2, '2025-10-02', 'assistant', 'Exactly, for example, when you must assign tasks to workers or select locations.'),

    -- Conversation 3 (Sarah)
    (3, '2025-10-03', 'user', 'My Python script keeps throwing a KeyError.'),
    (3, '2025-10-03', 'assistant', 'That usually means the key doesn’t exist in your dictionary. Can you share the code?'),

    -- Conversation 4 (Marc)
    (4, '2025-09-29', 'user', 'What’s the simplest way to start learning machine learning?'),
    (4, '2025-09-29', 'assistant', 'Begin with linear regression, it’s intuitive and widely used.'),
    (4, '2025-09-30', 'user', 'Should I learn NumPy and Pandas first?'),
    (4, '2025-09-30', 'assistant', 'Yes, definitely. They’re essential for data manipulation and analysis.');
