from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.auth import verify_token, create_access_token
from app.utils.file_handler import allowed_file, save_file
from fastapi.security import OAuth2PasswordBearer
from app.database import db
from passlib.hash import bcrypt

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login(data: dict):
    user = await db.users.find_one({"email": data.get("email"), "role": "ops"})
    if not user or not bcrypt.verify(data.get("password"), user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token({"email": user["email"], "role": "ops"})}

@router.post("/upload")
async def upload(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user or user.get("role") != "ops":
        raise HTTPException(status_code=403, detail="Unauthorized")
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")
    await save_file(file)
    return {"message": "File uploaded successfully"}
