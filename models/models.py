# # from passlib.context import CryptContext
# # import hashlib

# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # password = "a" * 100  # definitely >72 bytes

# # digest = hashlib.sha256(password.encode()).digest()
# # hashed = pwd_context.hash(digest)

# # print("OK:", hashed)

# from passlib.context import CryptContext
# import hashlib

# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# password = "a" * 200  # way over 72 bytes

# digest = hashlib.sha256(password.encode("utf-8")).digest()

# print(type(digest), len(digest))  # MUST be bytes, 32

# hashed = pwd_context.hash(digest)

# print("SUCCESS:", hashed)