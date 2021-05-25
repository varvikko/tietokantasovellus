CREATE TYPE user_role AS enum ('anon', 'registered', 'admin');

CREATE TABLE boards (
    name        VARCHAR(64) UNIQUE NOT NULL,
    path        VARCHAR(16) UNIQUE NOT NULL,
    description TEXT,
    PRIMARY KEY (path)
);

CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(64) UNIQUE,
    passwd      VARCHAR(128),
    role        user_role DEFAULT 'anon' NOT NULL
);

CREATE TABLE images (
    id          SERIAL PRIMARY KEY,
    filename    VARCHAR(32) UNIQUE NOT NULL,
    data        BYTEA NOT NULL
);

CREATE TABLE posts (
    id          SERIAL PRIMARY KEY,
    board       VARCHAR(16),
    thread      INTEGER,
    author      INTEGER,
    body        TEXT NOT NULL,
    image       INTEGER,
    created_at  TIMESTAMP NOT NULL,
    edited      BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (author) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (image) REFERENCES images(id) ON DELETE SET NULL,
    FOREIGN KEY (thread) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (board) REFERENCES boards(path) ON DELETE CASCADE
);

CREATE TABLE reports (
    id          SERIAL PRIMARY KEY,
    post        INTEGER NOT NULL,
    reasn       TEXT NOT NULL,
    FOREIGN KEY (post) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TABLE bans (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL,
    reason      TEXT NOT NULL,
    started_at  TIMESTAMP NOT NULL,
    ends_at     TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE hides (
    user_id     INTEGER NOT NULL,
    thread      INTEGER NOT NULL,
    PRIMARY KEY (user_id, thread),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
