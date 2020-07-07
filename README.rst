Scout : Search Engine
=====================

**Scout** is a search engine built on Python.
-------------------

**Power of search with Scout**::

    >>> from scout import Index, Scout

    >>> idx = Index("data_dump.json", database="scout.db")
    >>> idx.register()

    >>> q = Scout("scout.db")
    >>> q.search("autism")
      [
         {
            'id': 40,
            'summary': '...with autistic people. 
                        ...makes living with autism more difficult.'
         },
         {
            'id': 26,
            'summary': '...author, that truth was 
                        committing to the daily practice...'
         }
      ]

**Scout** allows you to pre-process data to form an index. This index
is accessible easily during realtime searches. Scout uses ngrams to
increase the chances of matching terms. Relevance is calculated using
modified version of BM25. 

Features
----------------

**Scout** is your go-to `book summary` search engine.

- Granular Indexing with Ngrams
- Tokenization Filters on Text
- Faster Retrievals
- Robust yet Simple APIs
- Automatic Database Loading

**Scout** uses SQLite3 database to store the corpus.


The API Documentation
---------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

``/docs/readme/index.rst``