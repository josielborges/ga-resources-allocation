#!/usr/bin/env python3
"""
Script to setup database with migrations and seed data
"""
import subprocess
import sys
import os
from seed_data import create_tables, seed_data

def run_migrations():
    """Run Alembic migrations"""
    try:
        print("Running database migrations...")
        result = subprocess.run(["alembic", "upgrade", "head"], 
                              capture_output=True, text=True, check=True)
        print("Migrations completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Alembic not found. Creating tables directly...")
        create_tables()
        return True

def main():
    """Main setup function"""
    print("Setting up database...")
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run migrations
    if not run_migrations():
        print("Failed to run migrations. Exiting.")
        sys.exit(1)
    
    # Seed data
    print("Seeding database with initial data...")
    try:
        seed_data()
        print("Database setup completed successfully!")
    except Exception as e:
        print(f"Failed to seed data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()