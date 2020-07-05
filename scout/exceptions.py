class IndexMissingInDatabase(Exception):
    """Raised when SQLite3 fails to find index tables."""


class UnsupportedQueryType(Exception):
    """Raised when the search query is not a str."""


class EmptyQuery(Exception):
    """Raised when the search query is empty."""
