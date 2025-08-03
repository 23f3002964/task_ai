from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database URL. For this phase, we use a local SQLite file.
# This makes it easy to get started without a separate database server.
# The 'check_same_thread' argument is specific to SQLite.
SQLALCHEMY_DATABASE_URL = "sqlite:///./pathcraft.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This dependency will be used in API endpoints to get a database session.
# It ensures that the database session is always closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
