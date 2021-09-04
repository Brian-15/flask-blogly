
DROP DATABASE IF EXISTS blogly_test;

CREATE DATABASE blogly_test;

\c blogly_test

CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    image_url TEXT
);

CREATE TABLE posts
(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users
);

CREATE TABLE tags
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE post_tag
(
    post_id INT REFERENCES posts,
    tag_id INT REFERENCES tags,
    PRIMARY KEY(post_id, tag_id)
);