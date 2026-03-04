from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from motor import motor_asyncio  # MongoDB async driver
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import secrets 
import hashlib # For hashing passwords
import os
from dotenv import load_dotenv
from automated_email import send_email

load_dotenv()

# MongoDB atlas connection string
uri = "mongodb+srv://fahadhussain:<HoWEH8nXqF5WR1fl>@cluster1.yrfdqns.mongodb.net/?appName=Cluster1"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# connection_string = os.getenv("MONGO_URI")
# DB_NAME = "Cluster1"

# # Create async client and database
# client = motor_asyncio.AsyncIOMotorClient(connection_string)
# db = client[DB_NAME]

app = FastAPI()

# # Model for signup - stores username, email, phone, password
# class SignupRequest(BaseModel):
#     username: str
#     email: str
#     phone_number: str
#     password: str

# # Model for login - stores email and password
# class LoginRequest(BaseModel):
#     email: str
#     password: str

# # Model for forgot password - stores email
# class ForgotPasswordRequest(BaseModel):
#     email: str

# # Model for reset password - stores email, reset_token, new_password
# class ResetPasswordRequest(BaseModel):
#     email: str
#     reset_token: str
#     new_password: str

# #Signup api
# @app.post("/signup")
# async def signup(data: SignupRequest):
#     # Get values from request body
#     email = data.email
#     password = data.password
#     username = data.username
#     phone_number = data.phone_number
    
#     # Check if email already exists in database
#     existing_user = await db.users.find_one({"email": email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already exists")
    
#     # Check if username already exists
#     existing_username = await db.users.find_one({"username": username})
#     if existing_username:
#         raise HTTPException(status_code=400, detail="Username already exists")
    
#     # Check if phone number already exists
#     existing_phone_number = await db.users.find_one({"phone_number": phone_number})
#     if existing_phone_number:
#         raise HTTPException(status_code=400, detail="Phone number already exists")
    
#     #hash the pasword first encode and then hash

#     hash_object = hashlib.sha256(password.encode())
#     hash_password = hash_object.hexdigest()

#     # Insert new user into database
#     result = await db.users.insert_one({
#         "email": email,
#         "password": hash_password,  #hashed password stored!
#         "username": username,
#         "phone_number": phone_number
#     })

#     return {"message": "User created successfully",
#             "user_id": str(result.inserted_id)
#     }


# #Login api
# @app.post("/login")
# async def login(data: LoginRequest):
#     # Get values from request body
#     email = data.email
#     password = data.password

#     # Hash the input password to compare with stored hash
#     hash_object = hashlib.sha256(password.encode())
#     hash_password = hash_object.hexdigest()

#     # Find user by email in database
#     user = await db.users.find_one({"email": email})
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
    
#     # Check if hashed password matches stored hash
#     if user["password"] != hash_password:
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     return {"message": "Login successful", 
#             "username": user["username"]}


# # Forget password api
# @app.post("/forgotpassword")
# async def forgot_password(data: ForgotPasswordRequest):
#     # Get email from request body
#     email = data.email
    
#     # Check if user with this email exists
#     user = await db.users.find_one({"email": email})
#     if not user:
#         raise HTTPException(status_code=404, detail="User with this email does not exist")
#     print("reset token")
#     # Generate a random reset token (6 digit code)
#     reset_token = str(secrets.randbelow(900000) + 100000)

#     # Store reset token in database with expiration (store for 15 minutes)
#     await db.users.update_one(
#         {"email": email},
#         {"$set": {"reset_token": reset_token, "token_created_at": "now"}}
#     )
#     # Send email to user with reset token
#     success, message = send_email(user["email"], "Password Reset", f"Your reset token is: {reset_token}")
#     if not success:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {message}")

#     return {"message": "Reset token sent to your email",
#             "reset_token": reset_token}  # Remove this line in production!

# #Reset password api
# @app.post("/resetpassword")
# async def reset_password(data: ResetPasswordRequest):
#     # Get values from request body
#     email = data.email
#     reset_token = data.reset_token
#     new_password = data.new_password

#     # Find user by email and reset token
#     user = await db.users.find_one({"email": email, "reset_token": reset_token})
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid reset token")
    
#     # Hash the new password before storing
#     hash_object = hashlib.sha256(new_password.encode())
#     hash_new_password = hash_object.hexdigest()
    
#     # Update password in database
#     await db.users.update_one(
#         {"email": email},
#         {"$set": {"password": hash_new_password}, "$unset": {"reset_token": "", "token_created_at": ""}}
#     )
    
#     return JSONResponse(
#         status_code=200,
#         content={"message": "Password reset successfully"}
#     )

# #health check api
# @app.get("/")
# async def root():
#     return {"message": "MaxFit AI API is running"}
