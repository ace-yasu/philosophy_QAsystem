
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    book TEXT NOT NULL,
    text TEXT NOT NULL,
    embedding vector(1536)
)