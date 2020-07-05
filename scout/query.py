import json
import sqlite3
import math
import functools, operator
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

    def relevance(self, index):
        # BM25 Relevance Scoring
        # https://en.wikipedia.org/wiki/Okapi_BM25
        # http://www.cs.otago.ac.nz/homepages/andrew/papers/2014-2.pdf
        # https://arxiv.org/pdf/0705.1161.pdf

        td = self.total_documents
        terms = list(index)
        documents = [list(index[term]) for term in index]
        documents = set(functools.reduce(operator.iconcat, documents, []))
        b, k = 0.75, 1.2  # Standard values for free variables
        for doc in documents:
            score_doc_query = b
            for trm in terms:
                df_t = len(index[trm])  # Document frequency of a term
                tf = len(index[trm][doc])  # Term frequency in a document (tf)

                # We're using modified IDF.
                # This minimize negative scoring for terms
                # occuring in most of the docs. (df_t > td/2)
                # For example : "The Book in Three Sentences"
                # Note : Score will be negative if term occurs
                # in all documents.

                idf = math.log((td - df_t + 0.5) / (df_t + 0.5)) / math.log(0.5 + td)
                score_doc_term = tf * (idf / (tf + k))
                score_doc_query += score_doc_term
            score = (score_doc_query + 0.001) / len(terms)
            yield (doc, score)

    def find_matches(self, ngrams):

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

        # Get json file paths from ngrams
        nparts = list(term.partitions(ngrams,
                                      path_prefix=self.index_path,
                                      indexed_at=self.slices))
        npaths = set(path for word, path in nparts)

        # Read partitions and gather results
        for pth in npaths:
            wds = list(word for word, path in nparts if path == pth)
            json_index = index_of_terms(pth, wds)
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

        query_index = dict(self.find_matches(ngrams))
        doc_by_rlv = self.relevance(query_index)
        doc_by_rlv = sorted(doc_relevance, key=lambda idx: idx[1])

        # Apply BM25 (F) model to each document
        # Rank and sort the results by relevance score
        # Return a list of book(id, summary) w/ highest relevance
        return doc_by_rlv
