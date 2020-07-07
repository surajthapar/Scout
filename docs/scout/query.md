# Searching

**Scout** searches through pre-processed index.

## Usage

Instantiate Scout class, and simply search. Make sure the index is already processed. For more check, scout.index.Index class.

```python
from scout import Scout
q = Scout(database="dbname")
q.search("The jumping $$ fox changes color.")
```
The above snippet returns upto 5 results. To control
the number of results, 'k' int.
```python
q.search("The jumping $$ fox changes color.", k=10)
```

## Class Variables
### `Scout.max_results`
`Scout.max_results` is used when user doesn't provide value 'k' during search, (type : `int`), defaults to `5`.

```python
q = Scout("dbname")
Scout.max_results = 10
results = q.search("hello world")
```

## Workflow

For a search query, `"The Un-Worthy jumping $$ fox changes color."`

```python
# Input Query
"The Un-Worthy jumping $$ fox changes color."

# Hyphenated words are merged.
"The UnWorthy jumping $$ fox changes color."

# Punctuations and non-ascii (beyond A-Z, 0-9) chars are stripped.
"The UnWorthy jumping fox changes color"

# Text is lowercased.
"the unworthy jumping fox changes color"

# Stop words like - "a", "the", "but" are removed.
"unworthy jumping fox changes color"

# Text is converted into a list of words.
["unworthy", "jumping", "fox", "changes", "color"]

# Each word is sliced and repeated to form n-grams.
# Say, for "unworthy"
["unw", "unwo", "unwor", "unwort", "unworth", "unworthy"]
```
Each n-gram term is looked in the index. All matching documents are
calculated for BM25 relevance score. Top 'k' results with highest
scores are returned.

```
[
{​'id​':​0​,  'summary​':'Practicing meditation will make you
                        ​at​ least ​10​ percent happier....'},
{'id​':​48, ​'summary​':'Finding something meaningful ​in​ your
                        life ​is​...'​​},
{​​'id​':​7​,  'summary​':'Everything ​in life ​is​ an invention.
         ​                If​ you...'}
]
```

#### BM25 Relevance Scoring (Refer below docs)
---
https://en.wikipedia.org/wiki/Okapi_BM25,
http://www.cs.otago.ac.nz/homepages/andrew/papers/2014-2.pdf,
https://arxiv.org/pdf/0705.1161.pdf
