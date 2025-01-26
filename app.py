import re
import requests
from flask import Flask, render_template, request, redirect, url_for, flash,session
import os
import werkzeug
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'azbycx'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Parth-02052004'
app.config['MYSQL_DB'] = 'kisanmitra'

mysql = MySQL(app)
@app.route('/')
# Route to render the index form
@app.route('/', methods=['GET', 'POST']) 
def index(): 
    return render_template("index.html")

@app.route('/aboutus')
def aboutus(): 
    return render_template("aboutus.html")

@app.route('/FPO')
def FPO(): 
    return render_template("FPO.html")


# Function to fetch countries from the API
def get_countries():
    url = "https://api.countrystatecity.in/v1/countries"
    headers = {
        "X-CSCAPI-KEY": "UU5wdms0Z0JzWDZJT2dpSk1MeWUyTzhjWVNTMW5kSkpQSW1mUGJYSw=="
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    countries = [country["name"] for country in data]
    return countries

# Function to fetch states of a given country from the API
def get_states(country_code):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states"
    headers = {
        "X-CSCAPI-KEY": "UU5wdms0Z0JzWDZJT2dpSk1MeWUyTzhjWVNTMW5kSkpQSW1mUGJYSw=="
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    states = [state["name"] for state in data]
    return states

# Function to fetch cities of a given state from the API
def get_cities(country_code, state_code):
    url = f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}/cities"
    headers = {
        "X-CSCAPI-KEY": "UU5wdms0Z0JzWDZJT2dpSk1MeWUyTzhjWVNTMW5kSkpQSW1mUGJYSw=="
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    cities = [city["name"] for city in data]
    return cities

# Route to render the registration form
@app.route("/registration", methods=["GET", "POST"])
def registration():
    errors = []
    success_msg = None

    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        phonenum = request.form.get('phonenum')
        email = request.form.get('email')
        address = request.form.get('address')
        state = request.form.get('state')
        city = request.form.get('city')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        if not fname or not lname or not phonenum or not email or not address or not state or not city or not password or not cpassword:
            errors.append('All fields are required.')
            
        if password != cpassword:
            errors.append('Passwords do not match.')

        name_pattern = r"^[a-zA-Z]+$"
        password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        phone_pattern = r"^[0-9]{10}$"
        email_pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"

        if not re.match(name_pattern, fname):
            errors.append('First name should contain only letters.')
        if not re.match(name_pattern, lname):
            errors.append('Last name should contain only letters.')
        if not re.match(password_pattern, password):
            errors.append('Password should be 8 characters or more, alphanumeric with special characters. Example: Demo@123')
        if not re.match(phone_pattern, phonenum):
            errors.append('Phone number should be exactly 10 digits and contain only numbers.')
        if not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')

        if not errors:
            try:
                # If no errors, save data to the database
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO users (fname, lname, phonenum, email, address, state, city, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(fname, lname, phonenum, email, address, state, city, password))
                mysql.connection.commit()
                success_msg = 'Registration successful!'
                #return redirect(url_for('login'))
            except Exception as e:
                errors.append('Plese enter valid Phonenumber and Email.')
                print(e)

    # Get the list of countries and set default country as India
    countries = get_countries()
    default_country = 'India'
    return render_template('registration.html', errors=errors, success_msg=success_msg, countries=countries, default_country=default_country)

# Route to fetch states based on selected country via AJAX
@app.route("/states", methods=["GET"])
def fetch_states():
    country_code = request.args.get("country_code")
    states = get_states(country_code)
    return {"states": states}

# Route to fetch cities based on selected state via AJAX
@app.route("/cities", methods=["GET"])
def fetch_cities():
    country_code = request.args.get("country_code")
    state_code = request.args.get("state_code")
    cities = get_cities(country_code, state_code)
    return {"cities": cities}

@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    errors = []
    success_msg = None
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        email_pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
        
        if not re.match(password_pattern, password):
            errors.append('Password should be 8 characters or more, alphanumeric with special characters. Example: Demo@123')
        if not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
            
        if not errors:
            try:
                cursor = mysql.connection.cursor()
                
                # Check if the user exists and the password is correct
                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                users = cursor.fetchone()
                
                if users:
                    # Save user details in session
                    session['user_email'] = email
                    if email == 'superuser@gmail.com':
                        return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('index'))
                else:
                    errors.append('Invalid email or password.')
            except Exception as e:
                errors.append('Error occurred while logging in.')
                print(e)

    return render_template("login.html", errors=errors, success_msg=success_msg)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot(): 
    errors = []
    success_msg = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        email_pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
        
        if not re.match(password_pattern, password):
            errors.append('Password should be 8 characters or more, alphanumeric with special characters. Example: Demo@123')
        if not re.match(email_pattern, email):
            errors.append('Please enter a valid email address.')
            
        if not errors:
            try:
             # If no errors, save data to the database
                cursor = mysql.connection.cursor()
                # Check if the user exists
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                if user:
                    # Update the password
                    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (password, email))
                    mysql.connection.commit()
                    success_msg = 'Password Updated.'
                else:
                    errors.append('User does not exist.')
            except Exception as e:
                errors.append('Enter Valid Email.')
                print(e)

    return render_template("forgot.html", errors=errors, success_msg=success_msg)

@app.route('/logout')
def logout():
    # Check if the user is logged in by verifying the 'user_email' key in the session
    if 'user_email' in session:
        # Clear the session data
        session.clear()
        flash('Logged out successfully')
    else:
        flash('You are not logged in')

    # Redirect the user to the home page after logout
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user_email' in session and session['user_email'] == 'superuser@gmail.com':
        return render_template('admin.html')

# Specify the upload folder
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

    
@app.route('/addequipment', methods=['GET', 'POST'])
def addequipment():
    if  request.method == 'POST':
        product_name = request.form['product_name']
        code = request.form['code']
        price = request.form['price']
        description = request.form['description']
        action = request.form['action']
        try:

        # Handle image upload
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename:
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    image_path = werkzeug.utils.secure_filename(image.filename)
                else:
                    image_path = None
            else:
                image_path = None

            cur = mysql.connection.cursor()
            if action == 'submit':
                cur.execute("INSERT INTO equipments (product_name, code, price, description, image_path) VALUES (%s, %s, %s, %s, %s)", (product_name, code, price, description, image_path))
                flash('Equipment added successfully')
            elif action == 'delete':
                cur.execute("DELETE FROM equipments WHERE code = %s", (code,))
                flash('Equipment deleted successfully')

            mysql.connection.commit()
            cur.close()

        except Exception as e:
            print("An exception occurred: {e}")
            flash('Equipment not added or deleted..')

    return render_template('addequipment.html')


@app.route('/addpesticide', methods=['GET', 'POST'])
def addpesticide():
    if  request.method == 'POST':
        product_name = request.form['product_name']
        code = request.form['code']
        price = request.form['price']
        description = request.form['description']
        action = request.form['action']
        try:

        # Handle image upload
            if 'image' in request.files:
                image = request.files['image']
                if image and image.filename:
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    image_path = werkzeug.utils.secure_filename(image.filename)
                else:
                    image_path = None
            else:
                image_path = None

            # Insert data into the database
            cur = mysql.connection.cursor()
            if action == 'submit':
                cur.execute("INSERT INTO pesticides (product_name, code, price, description, image_path) VALUES (%s, %s, %s, %s, %s)", (product_name, code, price, description, image_path))
                flash('Equipment added successfully')
            elif action == 'delete':
                cur.execute("DELETE FROM equipments WHERE code = %s", (code,))
                flash('Pesticide deleted successfully')

            mysql.connection.commit()
            cur.close()

        except Exception as e:
            print("An exception occurred: {e}")
            flash('Pesticidet not added or deleted..')

    return render_template('addpesticide.html')


# Route for the customer side equipment page
@app.route('/showequipment')
def showequipment():
    try:
        # Fetch equipment data from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM equipments")
        equipment_data = cur.fetchall()
        cur.close()

        for equipment in equipment_data:
            print("Equipment Image Path:", equipment[5])

        return render_template('showequipment.html', equipment_data=equipment_data)
    except Exception as e:
        print(f"An exception occurred: {e}")
        flash('Failed to fetch equipment data.')

    return render_template('showequipment.html', equipment_data=[])
    

@app.route('/showpesticide')
def showpesticide():
    try:
        # Fetch pesticide data from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pesticides")
        pesticides = cur.fetchall()
        cur.close()

        for pesticide in pesticides:
            print("Pesticide Image Path:", pesticide[5])

        return render_template('showpesticide.html', pesticides=pesticides)
    except Exception as e:
        print(f"An exception occurred: {e}")
        flash('Failed to fetch pesticide data.')

    return render_template('showpesticide.html', pesticides=[])

@app.route('/add_to_cart/<string:product_type>/<string:product_code>', methods=['POST'])
def add_to_cart(product_type, product_code):
    try:
        # Fetch product data from the database based on the product_code
        cur = mysql.connection.cursor()
        if product_type == 'equipment':
            cur.execute("SELECT * FROM equipments WHERE code = %s", (product_code,))
        elif product_type == 'pesticide':
            cur.execute("SELECT * FROM pesticides WHERE code = %s", (product_code,))
        else:
            flash('Invalid product type.')
            return redirect(url_for('showequipment'))

        product = cur.fetchone()
        cur.close()

        # Check if the 'cart' key is already in the session, if not, initialize it
        if 'cart' not in session:
            session['cart'] = []

        # Add the product to the cart (for simplicity, we're storing the entire product dictionary)
        session['cart'].append({'type': product_type, 'data': product})
        flash('Product added to cart successfully')


    except Exception as e:
        print(f"An exception occurred: {e}")
        flash('Failed to add product to cart.')

    if product_type == 'equipment':
        return redirect(url_for('showequipment'))
    elif product_type == 'pesticide':
        return redirect(url_for('showpesticide'))
    else:
        return redirect(url_for('showequipment'))


# Route to display the cart content
@app.route('/cart')
def cart():
    try:
        # Check if the 'cart' key is in the session
        if 'cart' in session:
            cart_items = session['cart']
        else:
            cart_items = []

        return render_template('cart.html', cart_items=cart_items)

    except Exception as e:
        print(f"An exception occurred: {e}")
        flash('Failed to fetch cart data.')

    return render_template('cart.html', cart_items=[])
if __name__ == '__main__':
    app.run(debug=True)