from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from bs4 import BeautifulSoup
from scrape_and_store import scrape_and_store
from models import db,User,MutualFund,Portfolio,MutualFunds
from auth import login_manager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from admin import admin_bp  # Import the admin blueprint
#from auth import User
from flask_migrate import Migrate
from flask import jsonify
from flask import flash
from flask_bcrypt import Bcrypt
import requests
app = Flask(__name__)

# Set the secret key
app.config['SECRET_KEY'] = 'c5064ddd7c72e2b528a770ff179e4d42'

# Replace 'mysql://username:password@localhost/dbname' with your MySQL connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:omg oh my god@localhost/mfdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(admin_bp)
login_manager= LoginManager(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Initialize db with the Flask app
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    #db.drop_all()
    db.create_all()
    scrape_and_store()

# Call the scrape_and_store function

login_state = False
# Context processor to pass login_state to all templates
@app.context_processor
def inject_login_state():
    return {'login_state': login_state}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mfinfo')
def mf_info():
    # You can pass any necessary data to mfinfo.html if needed
    return render_template('mfinfo.html')

@app.route('/data_entry')
def data_entry():
    return render_template('data_entry.html')
#old version
@app.route('/mutual_fund')
def mutual_fund():
    mutual_funds_list = MutualFund.query.all()
    return render_template('mutual_funds.html', mutual_funds=mutual_funds_list)

@app.route('/mutual_funds',methods=['GET','POST'])
def mutual_funds():
    name = None
    morningstar_rating = None
    if request.method == 'POST':
        name = request.form.get('name')
        morningstar_rating = request.form.get('morningstar_rating')
        try:
            if morningstar_rating:
                morningstar_rating = int(morningstar_rating)
        except ValueError:
            morningstar_rating = ''

    query = MutualFunds.query

    if name:
        query = query.filter(MutualFunds.name.like(f"%{name}%"))
    if morningstar_rating != '':
        query = query.filter(MutualFunds.morningstar_rating == morningstar_rating) 

    # If both fields are empty, return all records
    if request.method == 'GET' or (not name and morningstar_rating == ''):
        mutual_funds_list = MutualFunds.query.all()
    else:
        mutual_funds_list = query.all()
    login_state = current_user.is_authenticated
    return render_template('mutual_fund_scrape.html', mutual_funds=mutual_funds_list, login_state=login_state)

@app.route('/investment_form/<int:fund_id>')
def investment_form(fund_id):
    # Check if the user has already invested in this fund
    if fund_id in [p.fund_id for p in current_user.portfolios]:
        flash('You have already invested in this fund')
        return redirect(url_for('mutual_funds'))
    # Retrieve the fund name from the database based on its ID
    fund = MutualFunds.query.get(fund_id)
    if fund:
        fund_name = fund.name
        fund_return = fund.fund_return
    else:
        fund_name = None
        fund_return = None
    return render_template('invest.html', fund_name=fund_name,fund_return=fund_return,fund_id=fund_id)

@app.route('/submit_investment', methods=['POST'])
def submit_investment():
    # Process the form data
    amount = request.form['amount']
    duration = request.form['duration']
    fund_id = request.form['fund_id']
    user_id = current_user.id  # Assuming you're using Flask-Login
    

    # Create a new entry in the Portfolio table
    portfolio_entry = Portfolio(user_id=user_id, fund_id=fund_id, amount=amount, duration=duration)
    db.session.add(portfolio_entry)
    db.session.commit()

    # Redirect to the investment success page
    return redirect(url_for('mutual_funds'))

@app.route('/dictionary')
def dictionary():
    login_state = current_user.is_authenticated
    return render_template('imformation.html', login_state=login_state)

@app.route('/about')
def about():
    login_state = current_user.is_authenticated
    return render_template('about.html', login_state=login_state)

@app.route('/portfolio')
@login_required
def portfolio():
    user_id = current_user.id
    user_portfolio = Portfolio.query.filter_by(user_id=user_id).all()
    portfolio_funds = [p.fund_id for p in current_user.portfolios]  # Add this line here
    # Prepare data for the charts
    chart_data = []
    for entry in user_portfolio:
        labels = ['Invested Amount', 'Return']
        data = [entry.amount, entry.return_amount]  # Use the calculate_return method of the Portfolio model
        chart_data.append({'labels': labels, 'data': data})
        login_state = current_user.is_authenticated
    #return render_template('portfolio.html', user_portfolio=user_portfolio)
    return render_template('portfolio.html', user_portfolio=user_portfolio, chart_data=chart_data,portfolio_funds=portfolio_funds, login_state=login_state, user_name=current_user.username)


@app.route('/submit_data', methods=['POST'])
def submit_data():
    name = request.form.get('name')
    fund_type = request.form.get('fund_type')
    nav = float(request.form.get('nav'))
    returns = float(request.form.get('returns'))
    risk_tolerance = request.form.get('risk_tolerance')
    new_fund = MutualFund(name=name, fund_type=fund_type, nav=nav, returns=returns,risk_tolerance=risk_tolerance)
    db.session.add(new_fund)
    db.session.commit()

    return redirect(url_for('mutual_funds'))

# Add a new route for filtering funds
@app.route('/filter_funds', methods=['GET', 'POST'])
def filter_funds():
    if request.method == 'POST':
        # Get the selected risk tolerance and fund type from the form
        risk_tolerance = request.form.get('risk_tolerance')
        
        fund_category = request.form.get('fund_category')
        
        # Query the database to filter funds based on risk tolerance and fund type
        filtered_funds = MutualFund.query.filter_by(risk_tolerance=risk_tolerance, fund_type=fund_category).all()
        
        return render_template('filter_funds.html', filtered_funds=filtered_funds)

    # If it's a GET request, render the page with the form
    return render_template('filter_funds.html')

@app.route('/dashboard')
def dashboard():
    login_state = current_user.is_authenticated
    return render_template('index.html', login_state=login_state)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Implement login logic here
    if request.method == 'POST':
        # Validate user credentials and log them in
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin.admin_dashboard', user_name=user.username, user_id=user.id))
            else:
                return redirect(url_for('dashboard'))
    
    login_state = current_user.is_authenticated
    return render_template('admin/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    # Implement the signup logic here
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #is_admin = request.form.get('is_admin') == 'on'
        # Check if the 'is_admin' checkbox is selected
        is_admin = 'is_admin' in request.form
        # Validate the form data (e.g., check if passwords match)

        # Create a new user and add it to the database
        if password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password_hash=hashed_password,is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()

            # Redirect to the login page after successful signup
            return redirect(url_for('login'))
        else:
            # Handle the case where passwords don't match
            return render_template('admin/signup.html', message="Passwords do not match.")


    return render_template('admin/signup.html')
#to add user by admin
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # Add code here to add the new user to your database
         # Create a new user instance
        new_user = User(
            username=username,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
            is_admin=True if role == 'admin' else False
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin.manage_users'))

    return render_template('admin/add_user.html')

#manage users portfolio by admin
@app.route('/admin/manage_portfolios', methods=['GET'])
def manage_portfolios():
    # Query all users and their portfolios from the database
    users = User.query.all()

    return render_template('admin/manage_portfolios.html', users=users)

@app.route('/admin/delete_fund/<int:user_id>/<int:fund_id>', methods=['POST'])
def delete_fund(user_id, fund_id):
    # Query the user and the fund from the database
    user = User.query.get(user_id)
    fund_to_delete = None
    for portfolio in user.portfolios:
        if portfolio.fund.id == fund_id:
            fund_to_delete = portfolio
            break
    if fund_to_delete:
        # Delete the fund
        db.session.delete(fund_to_delete)
        db.session.commit()
    else:
        # Fund not found
        flash('Fund not found', 'error')
       


    return redirect(url_for('manage_portfolios'))

def get_financial_news():
    #api_key = 'H9D3T215Q1U9UUAM'
    url = f'https://financialmodelingprep.com/api/v3/stock_news?apikey=a5b58d816a52512f11d38eac14796b22'


    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        news_data = response.json()
        return news_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


@app.route('/daily_news')
def daily_news():
    login_state = current_user.is_authenticated
    return render_template('daily_news.html', login_state=login_state)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    login_state = False
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)