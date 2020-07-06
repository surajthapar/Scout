"""
**Scout** searches through course-book summaries, to provide easier
experience to pick and choose a book. It performs a search on a
given query by sifting book summaries and returns the K most
relevant documents.

Problem Statement
=================

Input
*****

- A search query 
  - type : str
  - eg. 'is your problems'
- Max results to return
  - type : int
  - eg. 3

Output
******

List of K relevant summaries sorted according to order of
relevance given a query.

Schema
******
    >>> {'summary': string, 'id': integer}

Example
*******

    >>> print(results)
        [
            {
                "summary": "The Book in Three Sentences: Practicing meditation and 
                mindfulness will make you at least 10 percent happier....",
                "id": 0
            },
            {
                "summary": "The Book in Three Sentences: Finding something important 
                and meaningful in your life is the most productive use of...",
                "id": 48
            },
            {
                "summary": "The Book in Three Sentences: Everything in life is an 
                invention. If you choose to look at your life in a new way...",
                "id": 7
            }
        ]

"""


from .query import Scout
from .index import Index
