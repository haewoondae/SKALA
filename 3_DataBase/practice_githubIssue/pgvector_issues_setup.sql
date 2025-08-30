
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop and recreate the issues table
DROP TABLE IF EXISTS issues;
CREATE TABLE issues (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    embedding vector(384)
);

-- Example insert (without actual vector, for structure)
-- INSERT INTO issues (title, description, embedding) VALUES
-- ('Login failure on Safari', 'Users report login failing on Safari 14. Appears to be cookie-related.', '[0.1, 0.2, ...]');
