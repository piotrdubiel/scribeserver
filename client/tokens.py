import time
import hashlib

def generate_token():
    base = time.time()
    return hashlib.sha256(str(base)).hexdigest()
