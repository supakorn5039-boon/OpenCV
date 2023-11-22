import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/smart.json")
firebase_admin.initialize_app(cred)
from firebase_admin import firestore

# Get a reference to the Firestore database
db = firestore.client()

# Example: Add a document to a 'users' collection
doc_ref = db.collection('users').document('user1')
doc_ref.set({
    'name': 'John Doe',
    'age': 30,
    'email': 'john@example.com'
})
