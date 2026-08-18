from pwdlib import PasswordHash
import secrets

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def generate_random_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"