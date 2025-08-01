import streamlit as st
from auth import (
    init_session_state, is_authenticated, get_current_user, 
    create_login_form, create_registration_form, display_user_info,
    show_navigation, validate_session, logout_user, is_admin, is_student,
    check_persistent_messages
)
from database import init_database

# Initialize database on startup
init_database()

# Page configuration
st.set_page_config(
    page_title="Multi-Role Auth System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS
st.markdown("""
<style>
    .stButton > button {
        background: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def show_header():
    """Display simple application header"""
    st.title("🔐 Multi Role Authentication System")

def show_home_page():
    """Display home page content for authenticated users"""
    user = get_current_user()
    
    st.success(f"👋 Welcome back, {user['username']}! You are logged in as: **{user['role'].title()}**")
    
    # Simple action buttons
    if st.button("🔑 Change Password"):
        st.session_state.show_password_form = True
        
    if st.button("👤 View Profile"):
        st.session_state.show_profile = True
        
    # Role-specific quick actions
    if is_admin():
        st.page_link("pages/admin.py", label="👑 Go to Admin Dashboard", icon="👑")
    elif is_student():
        st.page_link("pages/student.py", label="🎓 Go to Student Dashboard", icon="🎓")

def show_user_view(view_type):
    """Handle different user view types"""
    if view_type == 'profile':
        user = get_current_user()
        st.subheader("👤 Profile Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Username:** {user['username']}")
            st.info(f"**Role:** {user['role'].title()}")
        with col2:
            st.info(f"**Email:** {user['email']}")
            st.info(f"**User ID:** {user['id']}")
        
        if st.button("Back to Home"):
            if 'show_profile' in st.session_state:
                del st.session_state.show_profile
    
    elif view_type == 'password':
        from auth import create_password_change_form
        create_password_change_form()
        
        if st.button("Back to Home"):
            if 'show_password_form' in st.session_state:
                del st.session_state.show_password_form

def show_public_page():
    """Display simple public landing page for non-authenticated users"""
    
    # Demo credentials info box
    with st.expander("🎯 Demo Credentials - Try the App!", expanded=False):
        st.info("**For visitors to explore the application:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**👑 Admin Access:**")
            st.code("Username: admin\nPassword: Admin123!")
            st.caption("Full user management capabilities")
        
        with col2:
            st.markdown("**🎓 Student Access:**")
            st.code("Username: student\nPassword: Student123!")
            st.caption("Personal dashboard access")
        
        st.warning("⚠️ Note: These are demo accounts for testing purposes only.")
    
    # Login and Registration tabs
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        create_login_form()
    
    with tab2:
        create_registration_form()

def main():
    """Main application logic"""
    # Initialize session state
    init_session_state()
    
    # Validate current session
    validate_session()
    
    # Check for persistent messages
    check_persistent_messages()
    
    # Display header
    show_header()
    
    # Sidebar navigation and user info (navigation first, user info at bottom)
    show_navigation()
    display_user_info()
    
    # Main content based on authentication status
    if is_authenticated():
        # Handle different views for authenticated users
        if st.session_state.get('show_profile', False):
            show_user_view('profile')
        elif st.session_state.get('show_password_form', False):
            show_user_view('password')
        else:
            show_home_page()
    
    else:
        # Public page for non-authenticated users
        show_public_page()

# Error handling wrapper
def run_app():
    """Run the application with error handling"""
    try:
        main()
    except Exception as e:
        st.error("An unexpected error occurred. Please refresh the page.")
        st.error(f"Error details: {str(e)}")
        
        # Add logout button if user is authenticated
        if is_authenticated():
            if st.button("🚪 Logout and Refresh"):
                logout_user()
                st.rerun()

if __name__ == "__main__":
    run_app()