import json
import sqlite3
import math
import functools
import operator
from typing import List, Dict, Tuple, Iterator
from scout import term
from scout.exceptions import (
    IndexMissingInDatabase,
    UnsupportedQueryType,
    EmptyQuery
)


class Scout:
    """Scout Search

    :raises IndexMissingInDatabase: Raised when SQLite3 fails to
     find index tables.
    :raises UnsupportedQueryType: Raised when the search query is not a str.
    :raises EmptyQuery: Raised when the search query is empty.
    :raises LookupError: Raised when no results are found.**.
    """
    max_results = 5
    total_documents = None
    index_path = None
    slices = None

    def __init__(self, database: str):
        """Scout.__init__

        Example :
        ```
        q = Scout(database="example.db")
        results = q.search(query="Earth is flat", k=10)
        ```

        :param database: Location of the SQLite3 database file.
        :type database: str
        """
        self.database = database
        self._meta()

    def _meta(self):
        """Meta function fetches metadata from index db.

        Following fields are pulled from the db :
        1. total_documents
        2. index_path
        3. slices

        :raises IndexMissingInDatabase: Raised when meta table doesn't exist.
        """
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        try:
            c.execute(
                """SELECT total_documents, index_path, slices\
                   FROM meta WHERE id=0;"""
            )
        except sqlite3.OperationalError as e:
            raise IndexMissingInDatabase(e)
        result = c.fetchall()
        self.total_documents = result[0][0]
        self.index_path = result[0][1]
        self.slices = json.loads(result[0][2])
        c.close()
        conn.close()

    def relevance(self,
                  index: Dict[str, Dict[str, List[int]]]
                  ) -> Iterator[Tuple[int, float]]:
        """Relevance returns matching docs with BM25 score.

        :param index: The query index contains (word, data),
                      where data is dict of doc and pos list. 
                      Passed from dict of match function.
        :type index: Dict[str, Dict[str, List[int]]]
        :yield: Yields (Document ID, Relevance Score)
        :rtype: Iterator[Tuple[int, float]]

        """

        td = self.total_documents
        terms = list(index)

        # Get all unique matching documents
        documents = [list(index[term]) for term in index]
        documents = set(functools.reduce(operator.iconcat, documents, []))
        b, k = 0.75, 1.2  # Standard values for free variables
        for doc in documents:
            score_doc_query = b
            for trm in terms:
                # Document frequency of a term
                df_t = len(index.get(trm, []))

                # Term frequency in a document (tf)
                tf = len(index.get(trm, {}).get(doc, []))

                # We're using modified IDF.
                # This minimize negative scoring for terms
                # occuring in most of the docs. (df_t > td/2)
                # For example : "The Book in Three Sentences"
                # Note : Score will be negative if term occurs
                # in all documents.

                idf = math.log((td - df_t + 0.5) / (df_t + 0.5))
                idf = idf / math.log(0.5 + td)
                score_doc_term = tf * (idf / (tf + k))
                score_doc_query += score_doc_term
            score = (score_doc_query + 0.001) / len(terms)
            yield (doc, score)

    def match(self,
              ngrams: Dict[str, List[int]]
              ) -> Iterator[Tuple[str, Dict[str, List[int]]]]:
        """Match function finds all indices of each ngram.

        An iterator is returned for (word, data). The data is a dict
        combination of document id and term position list.

        :param ngrams: Ngram is a dictionary of words, position.
        :type ngrams: Dict[str, List[int]]
        :yield: An index containing (word, data), where data is dict
                of doc and pos list. Passed from dict of match function.
        :rtype: Iterator[Tuple[str, Dict[str, List[int]]]]

        """

        def index_of_terms(path: str,
                           terms: List[str]
                           ) -> Dict[str, Dict[int, List[int]]]:
            """Index of terms gets term relevant json from index files.

            If, a term is matched, below json is returned
            ```
            {
                "change" : {
                    10 : [20, 45],
                    20 : [5, 17, 33]
                },
            }
            ```
            Else, empty dict, if term is unmatched.
            ```
            {
                "changling" : {}
            }
            ```

            :param path: Location of the index file.
            :type path: str
            :param terms: List of ngram to be matched.
            :type terms: List[str]
            :return: Json of index for terms matched.
            :rtype: Dict[str, Dict[int, List[int]]]
            """
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
                # Yielding, (word, data)
                # Here, data is dict(doc_id,list(pos))
                yield (w, d)

    def search(self,
               query: str,
               k: int = None
               ) -> List[Dict[str, str]]:
        """Search returns a list of matching book summaries in order of relevance.

        Usage :
        Instantiate Scout class, and simply search.
        ```
        q = Scout("dbname")
        q.search("The jumping $$ fox changes color.")
        ```
        The above snippet returns upto 5 results. To control
        the number of results, 'k' int.
        ```
        q.search("The jumping $$ fox changes color.", k=10)
        ```

        :param query: A search query to find documents.
        :type query: str
        :param k: Maximum number of results, defaults to self.max_results
        :type k: int, optional
        :raises UnsupportedQueryType: Raised when the search query is not str.
        :raises EmptyQuery: Raised when the search query is empty.
        :raises LookupError: Raised when no results are found.
        :return: List of book {id, summary} in order of relevance.
        :rtype: List[Dict[str, str]]
        """
        if not k:
            k = self.max_results

        if not isinstance(query, str):
            raise UnsupportedQueryType("query must be of type str.")
        elif not query:
            raise EmptyQuery("query cannot be empty.")

        # Remove repetitive words in the query
        words = list(set(term.tokenize(query)))
        ngrams = term.ngram(words)

        query_index = dict(self.match(ngrams))
        doc_by_rlv = self.relevance(query_index)
        doc_by_rlv = sorted(doc_by_rlv, key=lambda idx: idx[1], reverse=True)
        doc_by_rlv = doc_by_rlv[:k]  # Get first 'k' results.
        k = min(len(doc_by_rlv), k)  # If results are less than 'k'
        if not k:
            raise LookupError("No results found.")
        result_doc_ids = [x[0] for x in doc_by_rlv]
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute(
            f"select id, summary from books where id IN ({','.join(['?']*k)})",
            result_doc_ids
        )
        results = c.fetchall()
        c.close()
        conn.close()

        return [dict(id=r[0], summary=r[1]) for r in results]
