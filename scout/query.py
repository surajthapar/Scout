from scout import term


class Scout:
    # q = Scout(database="example.db")
    # results = q.search(query="Earth is flat", k=10)
    max_results = 5

    def __init__(self, database):
        self.database = database

    def search(self, query, k=None):
        # Convert 'query' into ngrams (term functions)
        # Get json file paths from ngrams
        # Read partitions and gather results
        # Apply BM25 (F) model to each document
        # Rank and sort the results by relevance score
        # Return a list of book(id, summary) w/ highest relevance
        pass
