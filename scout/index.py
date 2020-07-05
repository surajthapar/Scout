import json
import os
import sqlite3
from scout import term


class TableAlreadyExists(Exception):
    """Raised when table being created already exists."""

# TODO
# 1. Create partitions (max 10k records per file?)


class Index:
    """Index cls"""

    index_path = None

    def __init__(self, corpus_filepath, database, slices=[1, 2, 4]):
        self.database = database
        self.corpus = corpus_filepath
        self.slices = slices

        if self.table_exists("books") and self.table_exists("meta"):
            self.read_meta()
        else:
            self.define()
            self.save_corpus()
            self.read_meta()

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
            total_documents INTEGER NOT NULL,
            index_path TEXT NOT NULL,
            slices TEXT NOT NULL
        );
        """)
        c = conn.cursor()
        # Set total_documents to ZERO.
        self.index_path = "idx_"+self.database.replace(".", "_")
        c.execute(
            "INSERT INTO meta VALUES (?,?,?,?);",
            (
                0,
                0,
                self.index_path,
                json.dumps(self.slices)
            )
        )
        conn.commit()
        c.close()
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
        WHERE type='table' AND name='{name}';""")
        existence = c.fetchone()[0] == 1
        c.close()
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
                    "INSERT INTO books VALUES (?,?,?,?);",
                    (
                        books['authors'][i]['book_id'],
                        title,
                        books['summaries'][i]['summary'],
                        books['authors'][i]['author']
                    )
                )

        conn.commit()
        c.close()
        conn.close()

    def read_meta(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("SELECT index_path, slices FROM meta WHERE id=0;")
        result = c.fetchall()
        self.index_path = result[0][0]
        self.slices = json.loads(result[0][1])
        c.close()
        conn.close()

    def read_partition(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def write_partition(self, path, data):
        # Create directory if it doesn't exist.
        dir = os.path.dirname(path)
        os.makedirs(dir, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f)

    def index_doc(self, ngrams):
        nparts = term.partitions(ngrams,
                                 path_prefix=self.index_path,
                                 indexed_at=self.slices)
        for word, path in nparts:
            pos = ngrams[word]
            yield (word, path, pos)

    def register_corpus(self):
        """Register corpus calculates and writes index to json files.

        Schema of a json file `idx/c/ch.json` :
        ```
            {
                "change" : {
                    10 : [20, 45],
                    20 : [5, 17, 33]
                }
            }
        ```
        """
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute('SELECT id, title, summary, author FROM books;')
        for row in c:
            # Combining title, author & summary for wider search.
            document = f"{row[1]} - {row[3]} {row[2]}"
            words = term.tokenize(document)
            ngrams = term.ngram(words)

            # returns [(word, path, pos),]
            ng_zip = list(self.index_doc(ngrams))
            files_to_write = set(n[1] for n in ng_zip)

            # Writing to each file just once for
            # a single document (book).
            for partition_file in files_to_write:
                try:
                    json_index = self.read_partition(partition_file)
                except FileNotFoundError:
                    json_index = dict()

                # Collect all words to be written in this file.
                ngs = [(n[0], n[2]) for n in ng_zip if n[1] == partition_file]

                # Append doc_id, pos to word's list if word
                # already exists, else add the word to the
                # json file.
                doc = str(row[0])  # Make sure doc_id is str (avoid dupes)
                for word, pos in ngs:
                    pos = list(set(pos))
                    if json_index.get(word):
                        if json_index[word].get(doc):
                            json_index[word][doc] = list(set([
                                *json_index[word][doc],
                                *pos
                            ]))
                        else:
                            json_index[word][doc] = pos
                    else:
                        json_index[word] = {doc: pos}
                self.write_partition(partition_file, json_index)

        c.close()
        c = conn.cursor()
        c.execute(
            """UPDATE meta SET total_documents=
            (SELECT COUNT(1) FROM books) WHERE id =0;"""
        )
        conn.commit()
        c.close()
        conn.close()
