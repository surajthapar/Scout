# Problem Statement

**Search Engine Challenge : Search Utility**

A service that allows students to search through coursebooks summaries which would make picking and buying a coursebook, a much better experience for students.

## Data

```
{
"titles": [
    "Anything You Want",
    "The Richest Man in Babylon"
],
"queries": [
    "is your problems",
    "achieve take book"
],
"summaries": [
    {
    "id": 0,
    "summary": "The Book in Three Sentences: Practicing meditation and mindfulness ..."
    },
    {
    "id": 1,
    "summary": "The Book in Three Sentences: The 10X Rule says that 1) you should set ..."
    }
],
"authors": [
    {
    "book_id": 0,
    "author": "Dan Harris"
    },
    {
    "book_id": 1,
    "author": "Grant Cardone"
    }
]
}
```

## User Inputs

Search utility should be developer friendly. Here's the requirement :
##### Search Query : *str*
> eg. 'is your problems'
##### Max results to return : *int*
> eg. 3


## Utility Output


List of K relevant summaries sorted according to order of
relevance given a query.

### Schema

```javascript
{'summary': string, 'id': integer}
```
### Example

```
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
```