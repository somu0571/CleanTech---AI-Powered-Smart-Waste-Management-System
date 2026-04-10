from db import SessionLocal, AdminID

db = SessionLocal()

ids = ["ADMIN001", "ADMIN002", "ADMIN003", "CLEANTECH_DEMO"]

for i in ids:
    exists = db.query(AdminID).filter_by(valid_admin_id=i).first()
    if not exists:
        db.add(AdminID(valid_admin_id=i))

db.commit()
db.close()

print("✅ Admin IDs inserted")