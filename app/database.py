from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.secure_file_sharing

async def init_db():
    await db.users.create_index("email", unique=True)
