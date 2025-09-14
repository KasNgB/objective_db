from db import engine
from models import Base

Base.metadata.create_all(bind=engine)
print("Database created (app.db) and tables are ready.")
