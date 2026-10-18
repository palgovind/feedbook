CREATE TABLE IF NOT EXISTS drawings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    aps_urn VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS drawing_comments (
    id SERIAL PRIMARY KEY,
    drawing_id INT REFERENCES drawings(id) ON DELETE CASCADE,
    username VARCHAR(100) NOT NULL,
    comment_text TEXT NOT NULL,
    camera_state TEXT NOT NULL,
    db_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);