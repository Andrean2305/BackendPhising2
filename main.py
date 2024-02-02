from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("Service.json")
try:
    default_app = firebase_admin.get_app()
except ValueError:
    default_app = firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: User):
    try:
        # Check if the user already exists
        user_ref = db.collection("User").document(user.username)
        existing_user = user_ref.get()

        if existing_user.exists:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create a new user document in the "User" collection
        user_ref.set({
            "password": user.password,
            # Add other fields as needed
        })

        return {"message": "User registered successfully", "user_id": user.username}

    except Exception as e:
        return {"error": str(e)}

@app.get("/{username}")
async def add_terkecoh_field(username: str):
    try:
        # Update the "terkecoh" field for the user in the database
        user_ref = db.collection("User").document(username)

        # Check if the document exists
        existing_user = user_ref.get()
        if existing_user.exists:
            # Get the current data in the document
            current_data = existing_user.to_dict()

            # Update the document with the new "terkecoh" field and preserve existing fields
            user_ref.update({
                **current_data,  # Preserving existing fields
                "terkecoh": "Username Ini sudah tertipu"
            })

            return {"message": f"Field 'terkecoh' added successfully for user {username}"}
        else:
            raise HTTPException(status_code=404, detail=f"User {username} not found")

    except Exception as e:
        return {"error": str(e)}
