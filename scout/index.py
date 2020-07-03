import json
import sqlite3


# TODO
# 1. Load the file to sqlite3 database
# 2. Query DB in chunks
# 3. Apply term functions on each document
# 5. Create partitions (max 10k records per file?)

class Index:
    """Index cls"""

    def __init__(self, corpus_filepath, database):
        pass

    def connection(self, db):
        return sqlite3.connect(db)

    def load_to_db(self, corpus):
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
        # TODO : Check if database already exists
        #        ..if not empty, raise.
        self.database.execute("""CREATE TABLE books(
            id INTEGER NOT NULL PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            author TEXT NOT NULL
        );
        """)

        with open(corpus) as f:
            books = json.load(f)

            for i, title in enumerate(books['titles']):
                c = self.database.cursor()
                c.execute(
                    "INSERT INTO books VALUES (?,?,?,?)",
                    (
                        books['authors'][i]['book_id'],
                        title,
                        books['summaries'][i]['summary'],
                        books['authors'][i]['author']
                    )
                )

        self.database.commit()
