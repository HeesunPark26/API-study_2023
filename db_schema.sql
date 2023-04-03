CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  bio TEXT,
  image TEXT,
  password TEXT NOT NULL
);

CREATE TABLE followers (
  rel_id INTEGER PRIMARY KEY AUTOINCREMENT,
  follower_id INTEGER NOT NULL,
  followed_id INTEGER NOT NULL,
  FOREIGN KEY (follower_id) REFERENCES users (id),
  FOREIGN KEY (followed_id) REFERENCES users (id)
);

CREATE TABLE posts (
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  body TEXT NOT NULL,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  favorited TEXT NOT NULL,
  favoritesCount INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  PRIMARY KEY (slug),
  FOREIGN KEY (author_id) REFERENCES users (id)
);

CREATE TABLE tags (
  tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_name TEXT NOT NULL
);

CREATE TABLE tag_rel (
  tag_rel_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_id INTEGER NOT NULL,
  slug TEXT NOT NULL,
  FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
  FOREIGN KEY (slug) REFERENCES posts (slug)
)