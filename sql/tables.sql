
CREATE TABLE books (
	id INTEGER NOT NULL, 
	title VARCHAR(255), 
	PRIMARY KEY (id)
);



CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR(255), 
	password VARCHAR(60), 
	PRIMARY KEY (id)
);


CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE authors (
	id INTEGER NOT NULL, 
	name VARCHAR(100), 
	PRIMARY KEY (id)
);


CREATE UNIQUE INDEX ix_authors_name ON authors (name);

CREATE TABLE authorship (
	author_id INTEGER, 
	book_id INTEGER, 
	FOREIGN KEY(author_id) REFERENCES authors (id), 
	FOREIGN KEY(book_id) REFERENCES books (id)
);


