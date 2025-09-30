import hashlib
import secrets
import binascii
from typing import Optional

class PasswordManager:
    """
    Secure password hashing and verification using PBKDF2 with SHA-256
    """
    
    @staticmethod
    def hash_password(password: str) -> tuple[str, str]:
        """
        Hash a password with a random salt
        
        Args:
            password: Plain text password
            
        Returns:
            tuple: (password_hash, salt) both as hex strings
        """
        # Generate a random salt
        salt = secrets.token_bytes(32)
        
        # Hash the password with PBKDF2
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt,
                                      100000)  # 100,000 iterations
        
        return binascii.hexlify(pwdhash).decode('ascii'), binascii.hexlify(salt).decode('ascii')
    
    @staticmethod
    def verify_password(stored_password_hash: str, stored_salt: str, provided_password: str) -> bool:
        """
        Verify a provided password against the stored hash and salt
        
        Args:
            stored_password_hash: Hex string of stored password hash
            stored_salt: Hex string of stored salt
            provided_password: Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Convert hex strings back to bytes
        salt = binascii.unhexlify(stored_salt)
        stored_hash = binascii.unhexlify(stored_password_hash)
        
        # Hash the provided password with the stored salt
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      provided_password.encode('utf-8'),
                                      salt,
                                      100000)
        
        # Compare the hashes
        return pwdhash == stored_hash

# Example usage functions for your Flask app
def create_user(db_connection, username: str, password: str, email: Optional[str] = None) -> bool:
    """
    Create a new user with hashed password
    
    Args:
        db_connection: Your database connection object
        username: User's username
        password: Plain text password
        email: Optional email address
        
    Returns:
        bool: True if user created successfully, False if username already exists
    """
    try:
        # Check if username already exists
        existing_user = db_connection.query("SELECT id FROM users WHERE username = %s", (username,))
        if existing_user:
            return False  # Username already exists
        
        # Hash the password
        password_hash, salt = PasswordManager.hash_password(password)
        
        # Insert the new user
        db_connection.execute(
            "INSERT INTO users (username, password_hash, salt, email) VALUES (%s, %s, %s, %s)",
            (username, password_hash, salt, email)
        )
        
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def authenticate_user(db_connection, username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user
    
    Args:
        db_connection: Your database connection object
        username: User's username
        password: Plain text password
        
    Returns:
        dict: User info if authentication successful, None if failed
    """
    try:
        # Get user from database
        user_data = db_connection.query(
            "SELECT id, username, password_hash, salt, email, is_active FROM users WHERE username = %s",
            (username,)
        )
        
        if not user_data or len(user_data) == 0:
            return None  # User not found
        
        user = user_data[0]  # Assuming query returns list of dictionaries
        
        # Check if user is active
        if not user.get('is_active', True):
            return None  # User account is deactivated
        
        # Verify password
        if PasswordManager.verify_password(user['password_hash'], user['salt'], password):
            # Update last login
            db_connection.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                (user['id'],)
            )
            
            # Return user info (without password data)
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        
        return None  # Password incorrect
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None