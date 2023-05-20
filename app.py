from flask import Flask, render_template, request, redirect
import smtplib
import random

app = Flask(__name__)

# A dictionary to store the generated OTPs and their corresponding email addresses
otp_data = {}

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/get_started')
def get_started():
    # Code to handle the "Get Started" button click
    return render_template('login.html')

@app.route('/')
def signup():
    return render_template('Register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/career_connect')
def career_connect():
    return render_template('dashboard.html')

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        name = data['name']
        email = data['email']
        message = data['message']
        file = database.write(f'\n{name},{email},{message}')

@app.route('/submit_form', methods=['POST','GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        write_to_file(data)
        return 'THANK YOU'
    else:
        return "somthing went wrong ,please try again!"

#login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit_login', methods=['GET', 'POST'])
def login_1():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the login credentials match
        if validate_login(username, password):
            return redirect('/OTP')  # Redirect to the dashboard page after successful login
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')

    return render_template('login.html')

def validate_login(username, password):
    # Read the login data from the database file
    with open('login.txt', 'r') as file:
        lines = file.readlines()

    # Check if any line in the file matches the provided credentials
    for line in lines:
        stored_username, stored_password = line.strip().split(',')
        if username == stored_username and password == stored_password:
            return True

    return False

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/OTP')
def OTP():
    return render_template('OTP.html')

@app.route('/Product_Manager')
def productManager():
    return render_template('product_Manager.html')

@app.route('/Register')
def record():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Save the user data to a file or database
    with open('users.txt', 'a') as file:
        file.write(f'{name}, {email}, {password}\n')

    return redirect('/OTP')



@app.route('/verify', methods=['POST'])
def send_verification():
    email = request.form['email']
    otp = generate_otp()

    # Store the OTP in the dictionary with the email as the key
    otp_data[email] = otp

    # Send the OTP to the provided email address using SMTP
    send_email(email, otp)

    # Redirect to the OTP verification page with the email as a query parameter
    return redirect('/verify_otp?email=' + email)

@app.route('/verify_otp')
def verify_otp():
    email = request.args.get('email')
    return render_template('verify_otp.html', email=email)

@app.route('/check_otp', methods=['POST'])
def check_otp():
    email = request.form['email']
    entered_otp = request.form['otp']
    stored_otp = otp_data.get(email)

    if entered_otp == stored_otp:
        # OTP is correct, remove it from the dictionary
        del otp_data[email]
        return render_template('dashboard.html')
    else:
        # OTP is incorrect, display an error message
        error_message = 'Invalid OTP. Please try again.'
        return render_template('verify_otp.html', email=email, error_message=error_message)

def generate_otp():
    # Generate a 6-digit random OTP
    return str(random.randint(100000, 999999))

def send_email(email, otp):
    # Replace the placeholders with your SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'feature.careerconnect@gmail.com'
    smtp_password = 'xghffrpmcgkzfrcz'

    subject = 'Email Verification OTP'
    body = f'Your OTP for email verification is: {otp}'
    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email, message)

if __name__ == '__main__':
    app.run(debug=True)
