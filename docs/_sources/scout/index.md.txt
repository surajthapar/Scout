# Indexing

Index class is used to generate file indices to
make realtime search faster. Pre-processing of
the index can be easily achieved.
Input data format for book metadata is as follows :
```
{
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
}
```

## Usage
```python
from scout import Index
idx = Index(corpus_filepath="data.json", database="sample.db")
idx.register()
```

Voila! It's that simple. You may control file partition
slicing by using `slicing` variable. It accepts a list of
int.

For example, a slicing param of `[1, 2, 5]` will save the
term *"changlings"* to `'idx_sample_db/c/ch/chang_index.json'`.
A slicing param of `[1, 2]` will save the term *"changling"* to
`'idx_sample_db/c/ch_index.json'` and so on.

```python
idx = Index("data.json", "sample.db", slicing=[1, 2])
idx.register()
```

## Workflow
The raw `data.json` is saved to **SQLite3 database** inside
`'books'` table. Each row is computed where text from
`(title, summary, author)` is combined together. Text
processing involves *tokenization* and generation of
*n-grams*. These *n-grams* are accounted for each document
and the position of occurrance. These *n-grams* are then
carefully saved in a calculated path, also known as a
*partition*. Files from this *partition* are readily
accessible during realtime search queries.