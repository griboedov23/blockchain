DROP TABLE if EXISTS blockchain;

CREATE TABLE IF NOT EXISTS blockchain (
                id INTEGER PRIMARY KEY,
                data TEXT,
                timestamp REAL,
                hash TEXT
            );