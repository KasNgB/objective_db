from db import SessionLocal
from models import Image

session = SessionLocal()
try:
    # INSERT
    img = Image(filename="example.jpg", width=640, height=480)
    session.add(img)
    session.commit()
    session.refresh(img)
    print("Inserted image id:", img.image_ID)

    # QUERY
    rows = session.query(Image).all()
    for r in rows:
        print(r.image_ID, r.filename, r.width, r.height, r.created_at)
finally:
    session.close()
