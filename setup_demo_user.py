"""
Script to create demo user for testing the authentication system.
Run this once to set up the demo account.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from smart_crop import auth

if __name__ == "__main__":
    print("Creating demo user...\n")
    
    success, message = auth.register_user(
        username="demo",
        email="demo@example.com",
        password="Demo@123",
        confirm_password="Demo@123"
    )
    
    if success:
        print(f"✅ {message}")
        print("\nDemo account created successfully!")
        print("Username: demo")
        print("Password: Demo@123")
        print("Email: demo@example.com")
        print("\nYou can now use these credentials to log in to the app.")
    else:
        print(f"❌ {message}")
        if "already exists" in message:
            print("Demo account already exists!")
