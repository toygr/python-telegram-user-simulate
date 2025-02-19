import hashlib


def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash
