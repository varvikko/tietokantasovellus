DROP TABLE replies;

CREATE TABLE replies (
    from_post   INTEGER NOT NULL,
    to_post     INTEGER NOT NULL,
    PRIMARY KEY (from_post, to_post),
    FOREIGN KEY (from_post) REFERENCES posts(id)
);
