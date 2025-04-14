CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    type VARCHAR(256) NOT NULL
);

CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    subtype VARCHAR(256) NOT NULL,
    category_id INT REFERENCES categories(id) 
);

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL
);

CREATE TABLE experience_levels (
    id SERIAL PRIMARY KEY,
    level VARCHAR(64) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    level_id INT REFERENCES experience_levels(id),
    subcategory_id INT REFERENCES subcategories(id),
    title VARCHAR(256) NOT NULL,
    description TEXT,
    publication_date DATE,
    limit_date DATE,
    extraction_date DATE
);

CREATE TABLE jobs_skills (
    id SERIAL PRIMARY KEY,
    skill_id INT REFERENCES skills(id),
    job_id INT REFERENCES jobs(id)
);

