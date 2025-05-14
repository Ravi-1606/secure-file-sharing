from fastapi import FastAPI
from app.routes import ops_user, client_user
from app.database import init_db

app = FastAPI()

app.include_router(ops_user.router, prefix="/ops", tags=["Ops User"])
app.include_router(client_user.router, prefix="/client", tags=["Client User"])

@app.get("/")
def root():
    return {"message": "Secure File Sharing System"}

@app.on_event("startup")
async def startup_db():
    await init_db()
