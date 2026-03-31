"""Security utilities for password hashing and verification."""
import hashlib
import secrets
import base64


def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2 algorithm with salt.
    
    Args:
        password: Plain text password to hash
    
    Returns:
        Hashed password with salt as base64 encoded string
    """
    # Generate random salt
    salt = secrets.token_bytes(32)
    
    # Hash password with salt using PBKDF2
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # iterations
    )
    
    # Combine salt and hash, then encode as base64
    combined = salt + hashed
    return base64.b64encode(combined).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Hashed password to check against
    
    Returns:
        True if password matches hash, False otherwise
    """
    try:
        # Decode base64 hash
        combined = base64.b64decode(hashed_password.encode('utf-8'))
        
        # Extract salt (first 32 bytes)
        salt = combined[:32]
        stored_hash = combined[32:]
        
        # Hash the provided password with stored salt
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # iterations
        )
        
        # Compare hashes
        return hashed == stored_hash
    except Exception:
        return False
