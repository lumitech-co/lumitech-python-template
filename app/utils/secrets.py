import bcrypt


def verify_secret(plain_secret: str, hashed_secret: str) -> bool:
    return bcrypt.checkpw(password=plain_secret.encode("utf-8"), hashed_password=hashed_secret.encode("utf-8"))


def hash_secret(secret: str) -> str:
    return bcrypt.hashpw(password=secret.encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")
