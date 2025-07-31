import streamlit as st
from auth import require_student, get_current_user, display_user_info, show_navigation, create_password_change_form, check_persistent_messages

# Page configuration
st.set_page_config(
    page_title="Student Portal - Coplur",
    page_icon="🎓",
    layout="wide"
)

# Require student access
require_student()

# Simple CSS
st.markdown("""
<style>
    .stButton > button {
        background: #28a745;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def show_student_header():
    """Display student dashboard header"""
    st.title("🎓 Student Dashboard")

def show_password_change_section():
    """Display password change form"""
    st.markdown("---")
    st.subheader("🔐 Change Your Password")
    
    create_password_change_form()
    
    if st.button("← Back to Dashboard"):
        if 'show_password_form' in st.session_state:
            del st.session_state.show_password_form
        st.rerun()

def main():
    """Main student dashboard logic"""
    # Check for persistent messages first
    check_persistent_messages()
    
    # Display header and navigation (navigation first, user info at bottom)
    show_student_header()
    show_navigation()
    display_user_info()
    
    # Handle different views
    if st.session_state.get('show_password_form', False):
        show_password_change_section()
    else:
        # Default dashboard view - simplified
        user = get_current_user()
        st.success(f"👋 Welcome, {user['username']}! This is your student portal.")
        
        # Simple action buttons
        if st.button("🔐 Change Password"):
            st.session_state.show_password_form = True
            st.rerun()
            
        if st.button("🏠 Back to Home"):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()
