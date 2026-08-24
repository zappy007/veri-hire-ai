import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load the secret URL from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize the database engine
engine = create_engine(DATABASE_URL)

# Quick test to verify the connection
try:
    with engine.connect() as connection:
        print("✅ Successfully connected to Supabase PostgreSQL!")
except Exception as e:
    print(f"❌ Connection failed: {e}")