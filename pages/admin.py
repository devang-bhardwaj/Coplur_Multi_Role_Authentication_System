import streamlit as st
import pandas as pd
from auth import require_admin, get_current_user, display_user_info, show_navigation, show_persistent_message, check_persistent_messages
from database import get_all_users, create_user, delete_user, get_user_by_id, update_user

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard - Coplur",
    page_icon="👑",
    layout="wide"
)

# Require admin access
require_admin()

# Simple CSS
st.markdown("""
<style>
    .stButton > button {
        background: #dc3545;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def show_admin_header():
    """Display admin dashboard header"""
    st.title("👑 Admin Dashboard")

def show_user_stats():
    """Display user statistics"""
    users = get_all_users()
    
    if users:
        total_users = len(users)
        admin_count = len([u for u in users if u['role'] == 'admin'])
        student_count = len([u for u in users if u['role'] == 'student'])
    else:
        total_users = admin_count = student_count = 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Users", total_users)
    
    with col2:
        st.metric("👑 Administrators", admin_count)
    
    with col3:
        st.metric("🎓 Students", student_count)

def create_user_form():
    """Display create new user form"""
    st.subheader("➕ Create New User")
    
    # Show password requirements
    with st.expander("🔐 Password Requirements", expanded=False):
        st.markdown("""
        **Password must contain:**
        - At least 8 characters
        - At least one uppercase letter (A-Z)
        - At least one lowercase letter (a-z)
        - At least one number (0-9)
        - At least one special character (!@#$%^&*...)
        """)
    
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter strong password")
        
        with col2:
            email = st.text_input("Email", placeholder="user@example.com")
            role = st.selectbox("Role", ["student", "admin"])
        
        submit_button = st.form_submit_button("Create User", use_container_width=True)
        
        if submit_button:
            if username and email and password and role:
                success, message = create_user(username, email, password, role)
                if success:
                    show_persistent_message('success', f"✅ {message}")
                    # Don't rerun immediately to let user see the message
                else:
                    show_persistent_message('error', f"❌ {message}")
            else:
                show_persistent_message('error', "Please fill in all fields")

def edit_user_form(user_id):
    """Display edit user form"""
    user = get_user_by_id(user_id)
    if not user:
        st.error("User not found")
        return
    
    st.subheader(f"📝 Edit User: {user['username']}")
    
    # Check if this is an admin and if they're the last admin
    is_last_admin = False
    if user['role'] == 'admin':
        all_users = get_all_users()
        admin_count = len([u for u in all_users if u['role'] == 'admin'])
        is_last_admin = admin_count <= 1
        
        if is_last_admin:
            st.warning("⚠️ **Warning:** This is the last admin user. Role cannot be changed to prevent system lockout.")
    
    with st.form(f"edit_user_form_{user_id}"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", value=user['username'])
            # Disable role change for last admin
            if is_last_admin:
                role = st.selectbox("Role", ["admin"], 
                                   index=0, disabled=True,
                                   help="Cannot change role of the last admin user")
            else:
                role = st.selectbox("Role", ["student", "admin"], 
                                   index=0 if user['role'] == 'student' else 1)
        
        with col2:
            email = st.text_input("Email", value=user['email'])
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            save_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        with col_cancel:
            cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if save_button:
            if username and email and role:
                success, message = update_user(user_id, username, email, role)
                if success:
                    show_persistent_message('success', f"✅ {message}")
                    # Clear edit state
                    if f'edit_user_{user_id}' in st.session_state:
                        del st.session_state[f'edit_user_{user_id}']
                    # Don't rerun immediately to let user see the message
                else:
                    show_persistent_message('error', f"❌ {message}")
            else:
                show_persistent_message('error', "Please fill in all fields")
        
        if cancel_button:
            # Clear edit state
            if f'edit_user_{user_id}' in st.session_state:
                del st.session_state[f'edit_user_{user_id}']
            st.rerun()

def display_users_table():
    """Display users in a formatted table"""
    users = get_all_users()
    
    if not users:
        st.info("No users found in the system.")
        return
    
    st.subheader("👥 User Management")
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(users)
    
    # Format the display
    df['Actions'] = range(len(df))  # Placeholder for action buttons
    
    # Display table
    st.markdown('<div class="user-table">', unsafe_allow_html=True)
    
    # Count admins for last admin protection
    admin_count = len([u for u in users if u['role'] == 'admin'])
    
    for idx, user in enumerate(users):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
            
            with col1:
                st.write(f"**{user['username']}**")
                st.caption(f"ID: {user['id']}")
            
            with col2:
                st.write(user['email'])
            
            with col3:
                role_color = "🔴" if user['role'] == 'admin' else "🔵"
                role_text = f"{role_color} {user['role'].title()}"
                # Add indicator for last admin
                if user['role'] == 'admin' and admin_count <= 1:
                    role_text += " (Last Admin)"
                st.write(role_text)
            
            with col4:
                # Show edit button for all users
                if st.button("📝", key=f"edit_{user['id']}", help="Edit user"):
                    st.session_state[f'edit_user_{user["id"]}'] = True
            
            with col5:
                # Prevent deletion of current admin
                current_user = get_current_user()
                can_delete = user['id'] != current_user['id']
                
                if can_delete:
                    if st.button("🗑️", key=f"delete_{user['id']}", help="Delete user"):
                        st.session_state[f'confirm_delete_{user["id"]}'] = True
                else:
                    st.button("🚫", key=f"nodelete_{user['id']}", help="Cannot delete yourself", disabled=True)
        
        # Handle delete confirmation
        if st.session_state.get(f'confirm_delete_{user["id"]}', False):
            st.warning(f"⚠️ Are you sure you want to delete user '{user['username']}'?")
            col_yes, col_no = st.columns(2)
            
            with col_yes:
                if st.button("Yes, Delete", key=f"yes_delete_{user['id']}"):
                    success, message = delete_user(user['id'])
                    if success:
                        show_persistent_message('success', f"✅ {message}")
                        # Clear confirmation state
                        del st.session_state[f'confirm_delete_{user["id"]}']
                        # Don't rerun immediately to let user see the message
                    else:
                        show_persistent_message('error', f"❌ {message}")
            
            with col_no:
                if st.button("Cancel", key=f"cancel_delete_{user['id']}"):
                    del st.session_state[f'confirm_delete_{user["id"]}']
                    st.rerun()
        
        # Handle edit form
        if st.session_state.get(f'edit_user_{user["id"]}', False):
            st.markdown("---")
            edit_user_form(user['id'])
            st.markdown("---")
        
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main admin dashboard logic"""
    # Check for persistent messages first
    check_persistent_messages()
    
    # Display header and navigation (navigation first, user info at bottom)
    show_admin_header()
    show_navigation()
    display_user_info()
    
    # Main content
    show_user_stats()
    
    st.markdown("---")
    
    # Create tabs for different admin functions
    tab1, tab2 = st.tabs(["👥 Manage Users", "➕ Create User"])
    
    with tab1:
        display_users_table()
    
    with tab2:
        create_user_form()

if __name__ == "__main__":
    main()
