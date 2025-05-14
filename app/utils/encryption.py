from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

def encrypt(data: str) -> str:
    return f.encrypt(data.encode()).decode()

def decrypt(token: str) -> str:
    return f.decrypt(token.encode()).decode()
