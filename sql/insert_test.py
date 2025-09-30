from .db import SessionLocal
from .models import Runs

def insert_run(start_time, end_time, detected=0):
    session = SessionLocal()
    try:
        # INSERT
        run = Runs(detected=detected, start_time=str(start_time), end_time=str(end_time))
        session.add(run)
        session.commit()
        session.refresh(run)
        print("Inserted run id:", run.id)
        print("Inserted detected humans:", run.detected)
        print("Inserted run start time", run.start_time)
        print("Inserted run end time:", run.end_time)

        # QUERY
        rows = session.query(Runs).all()
        for r in rows:
            print(r.id, r.detected, r.start_time, r.end_time)
    finally:
        session.close()
