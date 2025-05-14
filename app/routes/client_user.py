from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserSignup, UserLogin
from app.auth import create_access_token, verify_token
from app.database import db
from passlib.hash import bcrypt
from app.utils.email_service import send_verification_email
from app.utils.encryption import encrypt, decrypt
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup")
async def signup(user: UserSignup):
    hashed_password = bcrypt.hash(user.password)
    user_data = {"email": user.email, "hashed_password": hashed_password, "role": "client", "is_verified": False}
    try:
        await db.users.insert_one(user_data)
        token = encrypt(user.email)
        send_verification_email(user.email, token)
        return {"encrypted_url": token}
    except:
        raise HTTPException(status_code=400, detail="User already exists")

@router.get("/verify-email")
async def verify_email(token: str):
    try:
        email = decrypt(token)
        await db.users.update_one({"email": email}, {"$set": {"is_verified": True}})
        return {"message": "Verified"}
    except:
        raise HTTPException(status_code=400, detail="Invalid token")

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    if db_user and bcrypt.verify(user.password, db_user["hashed_password"]):
        token = create_access_token({"email": user.email, "role": db_user["role"]})
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/list-files")
async def list_files(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user or user.get("role") != "client":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"files": os.listdir("app/uploads")}

@router.get("/download-file/{filename}")
async def get_link(filename: str, token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user or user.get("role") != "client":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"download-link": f"/client/secure-download/{encrypt(filename)}"}

@router.get("/secure-download/{token}")
async def download(token: str, user_token: str = Depends(oauth2_scheme)):
    user = verify_token(user_token)
    if not user or user.get("role") != "client":
        raise HTTPException(status_code=403, detail="Unauthorized")
    filename = decrypt(token)
    filepath = os.path.join("app/uploads", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, filename=filename)
