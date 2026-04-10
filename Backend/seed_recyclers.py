from db import SessionLocal, RecyclerID

db = SessionLocal()

ids = ["REC001", "REC002", "REC003", "REC_CLEANTECH"]

for i in ids:
    exists = db.query(RecyclerID).filter_by(valid_recycler_id=i).first()
    if not exists:
        db.add(RecyclerID(valid_recycler_id=i))

db.commit()
db.close()

print("♻️ Recycler IDs inserted")