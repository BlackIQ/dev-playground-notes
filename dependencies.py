# Session
from db import session


# Get DB
def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()
