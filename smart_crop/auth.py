"""
User authentication module for Smart Crop Recommendation System.
Handles user registration, login, and credential verification.
"""

import json
import os
import re
import bcrypt
from pathlib import Path


# User database file path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USERS_DB_PATH = os.path.join(BASE_DIR, ".users", "users.json")


def ensure_db_exists():
    """Ensure the users database directory and file exist."""
    db_dir = os.path.dirname(USERS_DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    if not os.path.exists(USERS_DB_PATH):
        with open(USERS_DB_PATH, "w") as f:
            json.dump({}, f)


def load_users():
    """Load all registered users from the database."""
    ensure_db_exists()
    try:
        with open(USERS_DB_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_users(users):
    """Save users to the database."""
    ensure_db_exists()
    with open(USERS_DB_PATH, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_password(password: str) -> bool:
    """
    Validate password strength.
    Requirements: at least 8 characters, with uppercase, lowercase, digit, and special char.
    """
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/~`" for c in password)
    return has_upper and has_lower and has_digit and has_special


def register_user(username: str, email: str, password: str, confirm_password: str) -> tuple:
    """
    Register a new user.
    
    Returns:
        (success: bool, message: str)
    """
    users = load_users()
    
    # Validation checks
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long."
    
    if not is_valid_email(email):
        return False, "Invalid email format."
    
    if password != confirm_password:
        return False, "Passwords do not match."
    
    if not is_valid_password(password):
        return False, (
            "Password must be at least 8 characters and include "
            "uppercase, lowercase, digit, and special character."
        )
    
    if username in users:
        return False, "Username already exists."
    
    if any(user["email"] == email for user in users.values()):
        return False, "Email already registered."
    
    # Register user
    from datetime import datetime
    users[username] = {
        "email": email,
        "password": hash_password(password),
        "farm_size": "Not specified",
        "location": "Not specified",
        "phone": "Not specified",
        "soil_type": "Not specified",
        "member_since": datetime.now().strftime("%b %Y"),
        "total_predictions": 0,
        "success_rate": 100
    }
    save_users(users)
    return True, "Registration successful! You can now log in."


def login_user(username: str, password: str) -> tuple:
    """
    Authenticate a user.
    
    Returns:
        (success: bool, message: str)
    """
    users = load_users()
    
    if username not in users:
        return False, "Username not found."
    
    user = users[username]
    if not verify_password(password, user["password"]):
        return False, "Incorrect password."
    
    return True, "Login successful!"


def user_exists(username: str) -> bool:
    """Check if a user exists."""
    users = load_users()
    return username in users


def get_user_email(username: str) -> str:
    """Get the email of a registered user."""
    users = load_users()
    if username in users:
        return users[username]["email"]
    return ""


def get_user_profile(username: str) -> dict:
    """Get the complete profile of a registered user."""
    users = load_users()
    if username in users:
        user_data = users[username].copy()
        # Remove password from profile data
        if "password" in user_data:
            del user_data["password"]
        return user_data
    return {}


def update_user_profile(username: str, profile_data: dict) -> tuple:
    """
    Update user profile information.
    
    Args:
        username: The username to update
        profile_data: Dictionary containing profile fields to update
            (e.g., farm_size, location, phone, soil_type)
    
    Returns:
        (success: bool, message: str)
    """
    users = load_users()
    
    if username not in users:
        return False, "User not found."
    
    # Update allowed profile fields
    allowed_fields = ["farm_size", "location", "phone", "soil_type", "email"]
    for field, value in profile_data.items():
        if field in allowed_fields:
            users[username][field] = value
    
    save_users(users)
    return True, "Profile updated successfully!"


def initialize_user_profile(username: str, email: str) -> None:
    """Initialize a new user with default profile fields."""
    users = load_users()
    
    if username in users:
        # Add default profile fields if they don't exist
        if "farm_size" not in users[username]:
            users[username]["farm_size"] = "Not specified"
        if "location" not in users[username]:
            users[username]["location"] = "Not specified"
        if "phone" not in users[username]:
            users[username]["phone"] = "Not specified"
        if "soil_type" not in users[username]:
            users[username]["soil_type"] = "Not specified"
        if "member_since" not in users[username]:
            from datetime import datetime
            users[username]["member_since"] = datetime.now().strftime("%b %Y")
        if "total_predictions" not in users[username]:
            users[username]["total_predictions"] = 0
        if "success_rate" not in users[username]:
            users[username]["success_rate"] = 100
        
        save_users(users)
