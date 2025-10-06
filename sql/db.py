from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
import os

# Ensure the sql directory exists
os.makedirs("sql", exist_ok=True)

# SQLite DB file in the sql directory (relative path)
DB_URL = "sqlite:///./sql/runs.db"

# echo=True prints SQL statements (handy while learning)
engine = create_engine(DB_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def _fk_on(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA foreign_keys=ON")
