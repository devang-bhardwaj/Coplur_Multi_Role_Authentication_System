# 🔐 Coplur Multi-Role Authentication System

**COPLUR## 🔑 Default Demo Credentials

**For visitors to explore the application:**

**Admin User** (Full management access):
- **Username**: `admin`
- **Email**: `admin@coplur.com` 
- **Password**: `Admin123!`

**Student User** (Limited dashboard access):
- **Username**: `student`
- **Email**: `student@demo.com`
- **Password**: `Student123!`

> 💡 **Tip**: These credentials are displayed in an expandable info box on the login page for easy access!Challenge Submission** - A secure role-based authentication web application built with Streamlit.

## 🌐 Live Demo
**🚀 [View Live Application](https://coplurmultiroleothsystem.streamlit.app/)**

## 🎯 Problem Statement Implementation

This project implements a **Role-Based User Management Web Application** as per COPLUR requirements:

### ✅ Authentication Features (Common for all users)
- **Login** - Secure user authentication with session management
- **Logout** - Clean session termination
- **Change Password** - User can update their password securely
- **Register** - Self-registration for students only
- **Welcome Page** - Personalized dashboard upon successful login

### ✅ Role Implementation
- **👑 Admin Role** - Full user management capabilities
- **🎓 Student Role** - Limited access to personal features

### ✅ Admin Features
- Admin user created during application initialization (seeding)
- **Create new users** with role assignment (admin/student)
- **Delete existing users** with confirmation
- **View list of all users** with comprehensive dashboard
- **User statistics** and management interface

### ✅ Student Features
- **Welcome dashboard** after login
- **Profile viewing** capabilities
- **Cannot access** user management screens (protected routes)

## 🛡️ Technical Requirements Met

### Role-Based Access Control
- ✅ Secure role-based routing and permissions
- ✅ Unauthorized access blocked with proper messaging
- ✅ Admin-only routes protection

### Edge Case Handling
- ✅ **Duplicate user prevention** during registration
- ✅ **Wrong credentials** error handling
- ✅ **Strong password policies** (min 8 chars, letters + numbers)
- ✅ **Protected admin routes** 
- ✅ **Empty fields validation** and malformed input handling

## 🏗️ Tech Stack

- **Frontend**: Streamlit (Python-based web framework)
- **Backend**: Python with secure session management
- **Database**: SQLite with proper schema design
- **Authentication**: bcrypt password hashing
- **API Design**: Clean function-based architecture

## � Default Admin Credentials

**Default Admin User** (Auto-created on startup):
- **Username**: `admin`
- **Email**: `admin@coplur.com` 
- **Password**: `Admin123!`

## 🚀 Quick Start

### Option 1: Use Live Demo
Simply visit: **[https://coplurmultiroleothsystem.streamlit.app/](https://coplurmultiroleothsystem.streamlit.app/)**

### Option 2: Run Locally
```bash
# Clone repository
git clone https://github.com/devang-bhardwaj/Coplur_Multi_Role_Authentication_System.git
cd Coplur_Multi_Role_Authentication_System

# Install dependencies  
pip install -r requirements.txt

# Run application
streamlit run main.py
```

## 📂 Project Structure
```
├── main.py              # Main application entry point
├── auth.py              # Authentication & session management  
├── database.py          # Database operations & user management
├── requirements.txt     # Dependencies
├── .streamlit/          # Streamlit configuration
└── components/
    ├── admin.py        # Admin dashboard
    └── student.py      # Student portal
```

## 🎯 How to Use

### For Students:
1. **Register** using the registration form
2. **Login** with your credentials  
3. Access your **student dashboard**
4. **Change password** as needed

### For Administrators:
1. **Login** with admin credentials above
2. Access **admin dashboard**
3. **Create/delete users** and assign roles
4. **View user statistics** and manage system

## � Development Highlights

### Code Quality
- ✅ Clean, maintainable code structure
- ✅ Proper error handling and validation
- ✅ Secure coding practices implemented
- ✅ Modular design with separation of concerns

### Git Workflow  
- ✅ Regular commits with meaningful messages
- ✅ Collaborative development ready
- ✅ Proper version control practices
- ✅ No last-minute code dumps

### Security Implementation
- ✅ **Password Hashing** - bcrypt encryption
- ✅ **Session Management** - Secure user sessions  
- ✅ **Input Validation** - Comprehensive data validation
- ✅ **SQL Injection Protection** - Parameterized queries
- ✅ **Role Enforcement** - Strict access control

## 👥 Team Contribution

**Project developed for COPLUR Code Challenge by:**
- **Developer**: [Your Name] - Full-stack development, authentication system, database design, UI/UX
- **Contribution**: 100% individual effort with focus on security and user experience

## 🏆 Challenge Requirements Fulfilled

| Requirement | Implementation | Status |
|------------|----------------|---------|
| Role Management | Admin/Student roles with proper access control | ✅ Complete |
| Edge Case Handling | All validation and error scenarios covered | ✅ Complete |
| Code Quality | Clean, maintainable, well-structured code | ✅ Complete |
| Commit History | Regular meaningful commits, no dumps | ✅ Complete |
| Documentation | Comprehensive README with setup instructions | ✅ Complete |
| Security | Secure authentication and role enforcement | ✅ Complete |
| Live Demo | Deployed on Streamlit Cloud | ✅ Complete |

## 🎨 UI/UX Features

- **Clean Interface** - Intuitive Streamlit-based design
- **Responsive Layout** - Works on desktop and mobile
- **Role-based Navigation** - Context-aware menu system
- **Visual Feedback** - Clear success/error messaging
- **Dashboard Analytics** - User statistics and insights

---

**🌟 Built for COPLUR Code Challenge - Demonstrating secure web development and team collaboration skills.**

**📅 Submission Date**: August 1, 2025  
**🔗 Live Demo**: [https://coplurmultiroleothsystem.streamlit.app/](https://coplurmultiroleothsystem.streamlit.app/)  
**� Repository**: [GitHub](https://github.com/devang-bhardwaj/Coplur_Multi_Role_Authentication_System)