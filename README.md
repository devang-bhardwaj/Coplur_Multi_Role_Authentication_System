# Coplur Multi-Role Authentication System

A robust web application built with Streamlit that implements role-based user authentication and management.

## 🌟 Features

### Authentication Features (Common for all users)
- ✅ **Login/Logout** - Secure user authentication
- ✅ **Registration** - Students can self-register
- ✅ **Password Change** - Users can update their passwords
- ✅ **Welcome Dashboard** - Personalized landing page after login

### Role-Based Access Control
- 👑 **Admin Role** - Full user management capabilities
- 🎓 **Student Role** - Limited access to personal dashboard

### Admin Features
- ✅ Create new users (admin/student roles)
- ✅ Delete existing users
- ✅ View and manage all users
- ✅ User statistics dashboard
- ✅ Role assignment during user creation

### Student Features
- ✅ Personal welcome dashboard
- ✅ Profile viewing
- ✅ Password change functionality

## 🛡️ Security Features

- **Password Hashing** - bcrypt encryption for secure password storage
- **Role-Based Routing** - Unauthorized access prevention
- **Input Validation** - Strong password policies and data validation
- **Session Management** - Secure user session handling
- **SQL Injection Protection** - Parameterized database queries

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Authentication**: bcrypt
- **Data Processing**: Pandas

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/devang-bhardwaj/Coplur_Multi_Role_Authentication_System.git
   cd Coplur_Multi_Role_Authentication_System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`

## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment files"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `main.py` as the main file
   - Deploy!

## 🔑 Default Credentials

**Admin User** (Created automatically on first run):
- **Username**: `admin`
- **Email**: `admin@coplur.com`
- **Password**: `Admin123!`

## 📂 Project Structure

```
├── main.py              # Main application entry point
├── auth.py              # Authentication and session management
├── database.py          # Database operations and user management
├── requirements.txt     # Project dependencies
├── README.md           # Project documentation
└── pages/
    ├── admin.py        # Admin dashboard
    └── student.py      # Student dashboard
```

## 🎯 Usage

### For Students
1. **Register** a new account using the registration form
2. **Login** with your credentials
3. Access your **personal dashboard**
4. **Change password** when needed

### For Administrators
1. **Login** with admin credentials
2. Access the **admin dashboard**
3. **Create new users** (admin or student roles)
4. **Manage existing users** (view/delete)
5. **Monitor user statistics**

## 🛠️ Edge Cases Handled

- ✅ **Duplicate User Prevention** - Unique username/email validation
- ✅ **Wrong Credentials** - Appropriate error messaging
- ✅ **Strong Password Policy** - Minimum length and complexity requirements
- ✅ **Protected Routes** - Admin-only access enforcement
- ✅ **Input Validation** - Empty fields and malformed input handling
- ✅ **Session Security** - Secure session management and validation

## 👥 Team Contributions

This project was developed as part of the COPLUR Code Challenge for Role-Based Authentication Web Application.

**Team Members & Contributions:**
- **[Your Name]** - [Your contributions]
- **[Team Member 2]** - [Their contributions]
- **[Team Member 3]** - [Their contributions]
- **[Team Member 4]** - [Their contributions]

## 📋 Development Process

### Git Workflow
- Feature-based branching
- Regular commits with meaningful messages
- Code reviews and collaborative development
- Proper version control practices

### Code Quality
- Clean, maintainable code structure
- Proper error handling and validation
- Comprehensive input sanitization
- Role-based access control implementation

## 🎨 UI/UX Features

- **Responsive Design** - Works on desktop and mobile
- **Intuitive Navigation** - Clear role-based routing
- **User-Friendly Interface** - Clean Streamlit components
- **Visual Feedback** - Success/error message system
- **Dashboard Analytics** - User statistics and metrics

## 🔧 Configuration

The application uses SQLite database (`coplur_users.db`) which is created automatically on first run. The database includes:

- **Users Table** - Stores user credentials and roles
- **Auto-seeding** - Creates default admin user
- **Data Integrity** - Proper constraints and validation

## 📞 Support

For issues, questions, or contributions, please:
1. Create an issue in the GitHub repository
2. Follow the contribution guidelines
3. Ensure proper testing before submitting PRs

## 📝 License

This project is developed for educational purposes as part of the COPLUR Code Challenge.

---

**Built with ❤️ for secure web application development and team collaboration.**