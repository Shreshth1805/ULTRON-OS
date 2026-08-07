CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_todos_title ON todos (title);
CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos (completed);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

CREATE TABLE IF NOT EXISTS user_todos (
    user_id INTEGER NOT NULL,
    todo_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, todo_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (todo_id) REFERENCES todos (id)
);

CREATE INDEX IF NOT EXISTS idx_user_todos_user_id ON user_todos (user_id);
CREATE INDEX IF NOT EXISTS idx_user_todos_todo_id ON user_todos (todo_id);