import firebase_admin
from firebase_admin import credentials, firestore

try:
    # Initialize Firebase
   cred = credentials.Certificate("/smart-parking-e0f33-firebase-" "adminsdk-g8j23-ba95d55480.json")

    firebase_admin.initialize_app(cred)

    # Get a reference to the Firestore database
    db = firestore.client()

    # Example: Add a document to a 'users' collection
    doc_ref = db.collection('users').document('user1')
    doc_ref.set({
        'name': 'John Doe',
        'age': 30,
        'email': 'john@example.com'
    })

    print("Document added successfully.")
except Exception as e:
    print("Error:", str(e))
