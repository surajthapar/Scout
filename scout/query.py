import json
import sqlite3
from scout import term


class Scout:
    # q = Scout(database="example.db")
    # results = q.search(query="Earth is flat", k=10)
    max_results = 5
    total_documents = None
    index_path = None
    slices = None

    def __init__(self, database):
        self.database = database
        self.read_meta()

    def read_meta(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute(
            "SELECT total_documents, index_path, slices FROM meta WHERE id=0;"
        )
        result = c.fetchall()
        self.total_documents = result[0][0]
        self.index_path = result[0][1]
        self.slices = json.loads(result[0][2])
        c.close()
        conn.close()

    def index_of_terms(self, path, terms):
        data = dict()
        try:
            with open(path, 'r') as f:
                js = json.load(f)
                for t in terms:
                    data[t] = js.get(t, {})
        except FileNotFoundError:
            pass
        return data

    def find_matches(self, ngrams):
        # Get json file paths from ngrams
        nparts = list(term.partitions(ngrams,
                                      path_prefix=self.index_path,
                                      indexed_at=self.slices))
        npaths = set(path for word, path in nparts)

        # Read partitions and gather results
        for pth in npaths:
            wds = list(word for word, path in nparts if path == pth)
            json_index = self.index_of_terms(pth, wds)
            for w, d in json_index.items():
                yield (w, d)

    def search(self, query, k=None):
        # results = list()

        if not isinstance(query, str):
            raise TypeError("query must be of type str.")
        elif not query:
            raise ValueError("query cannot be empty.")

        # Remove repetitive words in the query
        words = list(set(term.tokenize(query)))
        ngrams = term.ngram(words)

        index = dict(self.find_matches(ngrams))

        # Apply BM25 (F) model to each document
        # Rank and sort the results by relevance score
        # Return a list of book(id, summary) w/ highest relevance
        return index
