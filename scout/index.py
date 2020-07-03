# TODO
# 1. Load the file to sqlite3 database
# 2. Query DB in chunks
# 3. Apply term functions on each document
# 5. Create partitions (max 10k records per file?)

def load_corpus(filepath: str, db: str):
    """Load Corpus inserts data to SQLite3 database.

    :param filepath: Corpus data file path.
    :type filepath: str
    :param db: SQLite3 database file path.
    :type db: str
    """

    if not isinstance(filepath, str):
        raise TypeError(f"""Param 'filepath' must be of \
    type 'str', not {type(filepath).__name__}""")

    if not isinstance(db, str):
        raise TypeError(f"""Param 'db' must be of \
    type 'str', not {type(db).__name__}""")
