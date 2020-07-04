import json
import sqlite3


class TableAlreadyExists(Exception):
    """Raised when table being created already exists."""
    pass

# TODO
# 1. Query DB in chunks
# 2. Apply term functions on each document
# 3. Create partitions (max 10k records per file?)


class Index:
    """Index cls"""

    def __init__(self, corpus_filepath, database):
        self.database = database
        self.corpus = corpus_filepath

    def connection(self, db):
        return sqlite3.connect(db)

    def table_exists(self, name="books"):
        conn = self.connection(self.database)
        c = conn.cursor()
        c.execute(f"""SELECT count(name) FROM sqlite_master \
        WHERE type='table' AND name='{name}'""")
        existence = c.fetchone()[0] == 1
        conn.close()
        return existence

    def load_to_db(self):
        """Load To DB inserts corpus data to SQLite3.

        Corpus is a JSON file with book metadata. It follows
        the below schema :

        ```{
            "titles": [
                "Anything You Want",
            ],
            "summaries": [
                {
                "id": 0,
                "summary": "Practicing meditation ... in your life"
                },
            ],
            "authors": [
                {
                "book_id": 0,
                "author": "Dan Harris"
                },
            ]
        }```

        :param corpus: Corpus data filepath.
        :type corpus: str
        """
        conn = self.connection(self.database)
        if self.table_exists("books"):
            raise TableAlreadyExists(f"""Couldn't create \
table 'books' in the database '{self.database}'.""")
        conn.execute("""CREATE TABLE books(
            id INTEGER NOT NULL PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            author TEXT NOT NULL
        );
        """)

        with open(self.corpus) as f:
            books = json.load(f)

            for i, title in enumerate(books['titles']):
                c = conn.cursor()
                c.execute(
                    "INSERT INTO books VALUES (?,?,?,?)",
                    (
                        books['authors'][i]['book_id'],
                        title,
                        books['summaries'][i]['summary'],
                        books['authors'][i]['author']
                    )
                )

        conn.commit()
