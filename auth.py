import streamlit as st
from database import authenticate_user, create_user, update_password
import re

def init_session_state():
    """Initialize session state variables with persistence"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    # Add session persistence flag
    if 'session_initialized' not in st.session_state:
        st.session_state.session_initialized = True

def is_authenticated():
    """Check if user is currently authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current logged-in user info"""
    return st.session_state.get('user', None)

def is_admin():
    """Check if current user is admin"""
    user = get_current_user()
    return user and user.get('role') == 'admin'

def is_student():
    """Check if current user is student"""
    user = get_current_user()
    return user and user.get('role') == 'student'

# Simple message functions removed for cleaner code

def show_persistent_message(message_type, message, duration=3):
    """Show a message that persists for a specified duration"""
    import time
    
    # Store message in session state with timestamp
    if f'{message_type}_message' not in st.session_state:
        st.session_state[f'{message_type}_message'] = None
        st.session_state[f'{message_type}_timestamp'] = None
    
    # Set new message
    st.session_state[f'{message_type}_message'] = message
    st.session_state[f'{message_type}_timestamp'] = time.time()
    
    # Display message
    if message_type == 'success':
        st.success(message)
    elif message_type == 'error':
        st.error(message)
    elif message_type == 'warning':
        st.warning(message)
    elif message_type == 'info':
        st.info(message)

def check_persistent_messages():
    """Check and display any persistent messages"""
    import time
    current_time = time.time()
    
    for msg_type in ['success', 'error', 'warning', 'info']:
        message = st.session_state.get(f'{msg_type}_message')
        timestamp = st.session_state.get(f'{msg_type}_timestamp')
        
        if message and timestamp:
            # Show message if it's less than 3 seconds old
            if current_time - timestamp < 3:
                if msg_type == 'success':
                    st.success(message)
                elif msg_type == 'error':
                    st.error(message)
                elif msg_type == 'warning':
                    st.warning(message)
                elif msg_type == 'info':
                    st.info(message)
            else:
                # Clear old message
                st.session_state[f'{msg_type}_message'] = None
                st.session_state[f'{msg_type}_timestamp'] = None

def login_user(username, password):
    """Simple login function"""
    if not username or not password:
        return False, "Please enter both username and password"
    
    if st.session_state.login_attempts >= 5:
        return False, "Too many login attempts. Please refresh."
    
    user = authenticate_user(username, password)
    if user:
        st.session_state.authenticated = True
        st.session_state.user = user
        st.session_state.login_attempts = 0
        return True, f"Welcome back, {user['username']}!"
    else:
        st.session_state.login_attempts += 1
        return False, "Invalid credentials"

def logout_user():
    """Clear user session and logout"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_attempts = 0
    # Clear other session data if needed
    for key in list(st.session_state.keys()):
        if key.startswith('temp_'):
            del st.session_state[key]

def register_student(username, email, password, confirm_password):
    """
    Register new student account
    Returns: (success: bool, message: str)
    """
    # Input validation
    validation_result = validate_registration_data(username, email, password, confirm_password)
    if not validation_result[0]:
        return validation_result
    
    # Create student account
    success, message = create_user(username, email, password, 'student')
    return success, message

def validate_registration_data(username, email, password, confirm_password):
    """Simple validation for registration"""
    if not all([username, email, password, confirm_password]):
        return False, "All fields are required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if '@' not in email:
        return False, "Please enter a valid email"
    
    return validate_password(password, confirm_password)

def validate_password(password, confirm_password=None):
    """Simple password validation"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if confirm_password and password != confirm_password:
        return False, "Passwords do not match"
    
    return True, "Password is valid"

def change_user_password(current_password, new_password, confirm_password):
    """
    Change current user's password
    Returns: (success: bool, message: str)
    """
    user = get_current_user()
    if not user:
        return False, "User not authenticated"
    
    # Validate current password
    auth_user = authenticate_user(user['username'], current_password)
    if not auth_user:
        return False, "Current password is incorrect"
    
    # Validate new password
    password_valid, password_msg = validate_password(new_password, confirm_password)
    if not password_valid:
        return False, password_msg
    
    # Update password
    success, message = update_password(user['username'], new_password)
    return success, message

def require_role(required_role=None):
    """Require specific role for page access"""
    if not is_authenticated():
        st.error("🔒 Please log in to access this page")
        st.stop()
    
    if required_role == 'admin' and not is_admin():
        st.error("⛔ Admin access required")
        st.info("Contact your administrator for access to this page")
        st.stop()
    elif required_role == 'student' and not is_student():
        st.error("⛔ Student access required")
        st.stop()

def require_authentication():
    """Require authentication for page access"""
    require_role()

def require_admin():
    """Require admin role for page access"""
    require_role('admin')

def require_student():
    """Require student role for page access"""
    require_role('student')



def create_login_form():
    """Simple login form"""
    st.subheader("🔐 Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")

def create_registration_form():
    """Simple student registration form"""
    st.subheader("📝 Student Registration")
    
    with st.form("registration_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            success, message = register_student(username, email, password, confirm_password)
            if success:
                show_persistent_message('success', message)
                show_persistent_message('info', "You can now log in with your new account!")
            else:
                show_persistent_message('error', message)

def create_password_change_form():
    """Simple password change form"""
    st.subheader("🔑 Change Password")
    
    with st.form("password_change_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submit_button = st.form_submit_button("Change Password")
        
        if submit_button:
            success, message = change_user_password(current_password, new_password, confirm_password)
            if success:
                show_persistent_message('success', message)
                show_persistent_message('info', "Please log in again with your new password")
                logout_user()
                st.rerun()
            else:
                show_persistent_message('error', message)

def show_navigation():
    """Display role-based navigation menu"""
    if not is_authenticated():
        return
    
    user = get_current_user()
    st.sidebar.markdown("## 🧭 Navigation")
    
    if is_admin():
        st.sidebar.page_link("components/admin.py", label="Admin Dashboard", icon="👑")
        st.sidebar.page_link("main.py", label="Home", icon="👑")
    elif is_student():
        st.sidebar.page_link("components/student.py", label="🎓 Student Dashboard", icon="🏠")
        st.sidebar.page_link("main.py", label="Home", icon="🏠")

def display_user_info():
    """Display current user info in sidebar"""
    if is_authenticated():
        user = get_current_user()
        st.sidebar.markdown("---")
        st.sidebar.success(f"👤 **{user['username']}**")
        st.sidebar.info(f"🏷️ Role: {user['role'].title()}")
        
        if st.sidebar.button("🚪 Logout"):
            logout_user()
            st.rerun()
    else:
        st.sidebar.info("👤 Not logged in")

def validate_session():
    """Validate current session"""
    if is_authenticated():
        user = get_current_user()
        if not user or not isinstance(user, dict):
            logout_user()
            return False
    return True

# Initialize session state when module is imported
init_session_state()
