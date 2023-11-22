import firebase_admin
from firebase_admin import credentials

# Replace 'path/to/your/credentials.json' with the path to the JSON file you downloaded
cred = credentials.Certificate('path/to/your/credentials.json')
firebase_admin.initialize_app(cred)
