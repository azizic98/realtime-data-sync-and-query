-- Create Outlets Table

CREATE SCHEMA test;

CREATE TABLE test.tbl_outlets
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NULL,
    twitter VARCHAR(255) NULL,
    active BOOLEAN DEFAULT FALSE 
);

-- Create Reporters Table

CREATE TABLE test.tbl_reporters
(
    reporter_id SERIAL PRIMARY KEY,
    outlet_id int4 NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NULL,
    twitter VARCHAR(255) NULL,
    active BOOLEAN DEFAULT FALSE,
    CONSTRAINT Fkey 
        FOREIGN KEY(outlet_id)
        REFERENCES test.tbl_outlets(id)
        DEFERRABLE INITIALLY DEFERRED
);

ALTER TABLE test.tbl_outlets REPLICA IDENTITY FULL;
ALTER TABLE test.tbl_reporters REPLICA IDENTITY FULL;

