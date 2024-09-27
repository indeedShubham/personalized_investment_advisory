from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user




login_manager = LoginManager()
login_manager.login_view = 'login'  # Set the login view route

class User(UserMixin):
    pass
   
    

@login_manager.user_loader
def load_user(user_id):
    # Implement a function to load a user from the database
    return User.query.get(int(user_id))
