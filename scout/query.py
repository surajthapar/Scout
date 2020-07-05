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

    def search(self, query, k=None):
        # Convert 'query' into ngrams (term functions)
        # Get json file paths from ngrams
        # Read partitions and gather results
        # Apply BM25 (F) model to each document
        # Rank and sort the results by relevance score
        # Return a list of book(id, summary) w/ highest relevance
        pass
