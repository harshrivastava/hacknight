from utils import db

print('Initializing DB...')
db.init_db()
print('DB initialized at', db.get_db_path())
print('Importing complaints.json -> complaints table...')
count_c = db.import_complaints_from_json()
print('Imported complaints:', count_c)
print('Importing services_listings.json -> providers/vendors...')
count_s = db.import_services_from_json()
print('Imported services/vendors:', count_s)
