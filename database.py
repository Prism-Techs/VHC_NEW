# db_connection.py

import sqlite3
from datetime import datetime
import json

class DatabaseConnection:
    def __init__(self, db_file="densitometer.db"):
        self.db_file = db_file
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Create a database connection"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.row_factory = sqlite3.Row  # This allows accessing columns by name
            self.cursor = self.connection.cursor()
            self.create_tables()
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
            
    def disconnect(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            
    def create_tables(self):
        """Create AuthUser table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password VARCHAR(128) NOT NULL,
                last_login DATETIME NULL,
                is_admin BOOLEAN NOT NULL DEFAULT 0,
                username VARCHAR(150) UNIQUE NOT NULL,
                first_name VARCHAR(150) NOT NULL,
                last_name VARCHAR(150) NOT NULL,
                email VARCHAR(254) NOT NULL,
                is_doctor BOOLEAN NOT NULL DEFAULT 1,
                is_active INTEGER NOT NULL DEFAULT 1,
                date_joined DATETIME NULL,
                phone INTEGER NULL,
                address TEXT NULL,
                created_by INTEGER NULL,
                city INTEGER NULL,
                state INTEGER NULL,
                machine_access_list TEXT DEFAULT '{}',
                title VARCHAR(45) NULL,
                is_operator BOOLEAN NOT NULL DEFAULT 1,
                is_superuser BOOLEAN NOT NULL DEFAULT 0,
                is_staff BOOLEAN NOT NULL DEFAULT 0,
                is_sync TINYINT NOT NULL DEFAULT 0
            )
        ''')
        self.connection.commit()

    def add_user(self, **kwargs):
        """Add a new user to auth_user table"""
        try:
            # Convert machine_access_list to JSON string if it's a dict
            if 'machine_access_list' in kwargs and isinstance(kwargs['machine_access_list'], dict):
                kwargs['machine_access_list'] = json.dumps(kwargs['machine_access_list'])
            
            # Prepare fields and values for the query
            fields = ', '.join(kwargs.keys())
            placeholders = ', '.join(['?' for _ in kwargs])
            values = tuple(kwargs.values())
            
            query = f'INSERT INTO auth_user ({fields}) VALUES ({placeholders})'
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding user: {e}")
            return None

    def get_user(self, username):
        """Get user by username"""
        try:
            self.cursor.execute('SELECT * FROM auth_user WHERE username = ?', (username,))
            user = self.cursor.fetchone()
            if user:
                # Convert JSON string back to dict for machine_access_list
                user_dict = dict(user)
                user_dict['machine_access_list'] = json.loads(user_dict['machine_access_list'])
                return user_dict
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def update_user(self, username, **kwargs):
        """Update user details"""
        try:
            # Convert machine_access_list to JSON string if it's present and is a dict
            if 'machine_access_list' in kwargs and isinstance(kwargs['machine_access_list'], dict):
                kwargs['machine_access_list'] = json.dumps(kwargs['machine_access_list'])
            
            # Prepare the SET clause
            set_clause = ', '.join([f'{key} = ?' for key in kwargs.keys()])
            values = tuple(kwargs.values()) + (username,)
            
            query = f'UPDATE auth_user SET {set_clause} WHERE username = ?'
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, username):
        """Delete a user"""
        try:
            self.cursor.execute('DELETE FROM auth_user WHERE username = ?', (username,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def verify_login(self, username, password):
        """Verify user login credentials"""
        try:
            self.cursor.execute('''
                SELECT * FROM auth_user 
                WHERE username = ? AND password = ? AND is_active = 1
            ''', (username, password))
            user = self.cursor.fetchone()
            if user:
                # Update last_login
                self.update_user(username, last_login=datetime.now())
                # Convert JSON string to dict for machine_access_list
                user_dict = dict(user)
                user_dict['machine_access_list'] = json.loads(user_dict['machine_access_list'])
                return user_dict
            return None
        except Exception as e:
            print(f"Error verifying login: {e}")
            return None