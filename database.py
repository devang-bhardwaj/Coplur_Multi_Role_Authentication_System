import sqlite3
import bcrypt
import os
from contextlib import contextmanager

# Database configuration
DATABASE_FILE = 'coplur_users.db'

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

def handle_db_operation(operation_func):
    """Decorator to handle database operations with error handling"""
    def wrapper(*args, **kwargs):
        try:
            return operation_func(*args, **kwargs)
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
    return wrapper

def init_database():
    """Initialize database with users table and default admin"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create users table with proper constraints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'student')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create default admin if none exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Updated admin password to meet new requirements
            admin_password = hash_password('Admin123!')
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role) 
                VALUES (?, ?, ?, ?)
            """, ('admin', 'admin@coplur.com', admin_password, 'admin'))
            
        conn.commit()

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def create_user(username, email, password, role='student'):
    """
    Create new user with validation
    Returns: (success: bool, message: str)
    """
    # Input validation and sanitization
    if not all([username, email, password, role]):
        return False, "All fields are required"
    
    # Trim and validate inputs
    username = username.strip()
    email = email.strip().lower()  # Normalize email to lowercase
    
    if not all([username, email, password, role]):
        return False, "Fields cannot be empty or contain only spaces"
    
    if role not in ['admin', 'student']:
        return False, "Invalid role specified"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # Length validation
    if len(username) > 20:
        return False, "Username cannot be longer than 20 characters"
    
    if len(email) > 100:
        return False, "Email address is too long"
    
    # Basic password strength check (more detailed validation in auth.py)
    if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
        return False, "Password must contain at least one letter and one number"
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check for existing user
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE username = ? OR email = ?
            """, (username, email))
            
            if cursor.fetchone()[0] > 0:
                return False, "Username or email already exists"
            
            # Create user
            password_hash = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role) 
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, role))
            
            conn.commit()
            return True, "User created successfully"
            
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def authenticate_user(username, password):
    """
    Authenticate user login
    Returns: user dict if successful, None if failed
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, role 
                FROM users WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            if user and verify_password(password, user['password_hash']):
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role']
                }
            return None
            
    except sqlite3.Error:
        return None

def get_all_users():
    """Get all users for admin dashboard"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, role, created_at 
                FROM users ORDER BY created_at DESC
            """)
            
            return [dict(row) for row in cursor.fetchall()]
            
    except sqlite3.Error:
        return []

def delete_user(user_id):
    """
    Delete user by ID with admin protection
    Returns: (success: bool, message: str)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Get user info
            cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return False, "User not found"
            
            # Prevent deletion of last admin
            if user['role'] == 'admin':
                cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
                admin_count = cursor.fetchone()[0]
                
                if admin_count <= 1:
                    return False, "Cannot delete the last admin user"
            
            # Delete user
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            
            return True, "User deleted successfully"
            
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def update_password(username, new_password):
    """Update user password"""
    if len(new_password) < 8:
        return False, "Password must be at least 8 characters"
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            password_hash = hash_password(new_password)
            cursor.execute("""
                UPDATE users SET password_hash = ? WHERE username = ?
            """, (password_hash, username))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Password updated successfully"
            else:
                return False, "User not found"
                
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def update_user(user_id, username, email, role):
    """
    Update user information with comprehensive validation
    Returns: (success: bool, message: str)
    """
    # Input validation and sanitization
    if not all([username, email, role]):
        return False, "All fields are required"
    
    # Trim and validate inputs
    username = username.strip()
    email = email.strip().lower()  # Normalize email to lowercase
    
    if not all([username, email, role]):
        return False, "Fields cannot be empty or contain only spaces"
    
    if role not in ['admin', 'student']:
        return False, "Invalid role specified"
    
    # Length validation
    if len(username) > 20:
        return False, "Username cannot be longer than 20 characters"
    
    if len(email) > 100:
        return False, "Email address is too long"
    
    # Validate user_id
    if not isinstance(user_id, int) or user_id <= 0:
        return False, "Invalid user ID"
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if user exists and get current role
            cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
            current_user = cursor.fetchone()
            if not current_user:
                return False, "User not found"
            
            current_role = current_user['role']
            
            # Prevent removing admin role if it would leave no admins
            if current_role == 'admin' and role != 'admin':
                cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
                admin_count = cursor.fetchone()[0]
                
                if admin_count <= 1:
                    return False, "Cannot change role: This is the last admin user in the system"
            
            # Check for duplicate username/email (excluding current user)
            cursor.execute("""
                SELECT COUNT(*) FROM users 
                WHERE (username = ? OR email = ?) AND id != ?
            """, (username, email, user_id))
            
            if cursor.fetchone()[0] > 0:
                return False, "Username or email already exists"
            
            # Update user
            cursor.execute("""
                UPDATE users SET username = ?, email = ?, role = ? 
                WHERE id = ?
            """, (username, email, role, user_id))
            
            conn.commit()
            return True, "User updated successfully"
            
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def get_user_by_id(user_id):
    """Get user details by ID"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, role, created_at 
                FROM users WHERE id = ?
            """, (user_id,))
            
            user = cursor.fetchone()
            return dict(user) if user else None
            
    except sqlite3.Error:
        return None

# Initialize database when module is imported
init_database()
