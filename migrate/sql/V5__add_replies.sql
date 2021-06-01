CREATE TABLE replies (
    from_post   INTEGER NOT NULL,
    to_post     INTEGER NOT NULL,
    PRIMARY KEY (post_from, post_to),
    FOREIGN KEY (post_from) REFERENCES posts(id),
    FOREIGN KEY (post_to) REFERENCES posts(id)
);
