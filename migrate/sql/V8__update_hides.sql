DROP TABLE hides;


CREATE TABLE hides (
    user_id     INTEGER NOT NULL,
    thread      INTEGER NOT NULL,
    PRIMARY KEY (user_id, thread),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
