import json
import sqlite3


class TableAlreadyExists(Exception):
    """Raised when table being created already exists."""

# TODO
# 1. Query DB in chunks
# 2. Apply term functions on each document
# 3. Create partitions (max 10k records per file?)


class Index:
    """Index cls"""

    def __init__(self, corpus_filepath, database):
        self.database = database
        self.corpus = corpus_filepath

    def define(self):
        """Define setups the schema for required data tables.

        :raises TableAlreadyExists: Failed to create table, as
        it already exists in db.
        """
        # Table : Corpus
        conn = sqlite3.connect(self.database)
        if self.table_exists("books"):
            raise TableAlreadyExists(f"""Couldn't create table 'books'\
        in the database '{self.database}'.""")
        conn.execute("""CREATE TABLE books(
            id INTEGER NOT NULL PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            author TEXT NOT NULL
        );
        """)

        # Table : Meta-Metadata
        if self.table_exists("meta"):
            raise TableAlreadyExists(f"""Couldn't create table 'meta'\
        in the database '{self.database}'.""")
        conn.execute("""CREATE TABLE meta(
            id INTEGER NOT NULL PRIMARY KEY,
            total_documents INTEGER NOT NULL
        );
        """)
        c = conn.cursor()
        # Set total_documents to ZERO.
        c.execute("INSERT INTO meta VALUES (?,?)", (0, 0))
        conn.commit()
        conn.close()

    def table_exists(self, name="books") -> bool:
        """Table exists checks sqlite db for table's existence.

        :param name: Name of the table, defaults to "books"
        :type name: str, optional
        :return: Existence of the table in self.database
        :rtype: bool
        """
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute(f"""SELECT count(name) FROM sqlite_master \
        WHERE type='table' AND name='{name}'""")
        existence = c.fetchone()[0] == 1
        conn.close()
        return existence

    def save_corpus(self):
        """Save Corpus loads book meta data to SQLite3.

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
        """
        conn = sqlite3.connect(self.database)
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
        conn.close()

    def calibrate_count(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute(
            "UPDATE meta SET total_documents =total_documents + 1 WHERE id =0"
        )
        c.commit()
        conn.close()

    def register(self, id):
        pass
