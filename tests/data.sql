INSERT INTO users (username, password)
VALUES
    ('test', 'pbkdf2:sha256:50000$TCI4GzcX$...')
    ('other', 'pbkdf2:sha256:50000$kJPKsz6N$...')

INSERT INTO post (title, body, author_id, created)
VALUES
    ('test title', 'test' || x'0a' || 'body', 1, '2025-12-11 00:00:00');