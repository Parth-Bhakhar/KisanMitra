from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import random
import os

app = Flask(__name__)

# Twilio credentials (replace with your actual Twilio credentials)
account_sid = "ACfa186fc6fe8d62e038bd50b3546822b1"
auth_token = "f2326e3d755f7528d05f223a89dc72a8"
twilio_phone_number = "+12015590637"

client = Client(account_sid, auth_token)

# Store registered farmers and their OTPs (for demonstration purposes, use a database in a production environment)
registered_farmers = {}

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp(phone_number, otp):
    try:
        message = client.messages.create(
            body=f"Your OTP for farmer registration: {otp}",
            from_=twilio_phone_number,
            to=phone_number
        )
        return message.sid
    except Exception as e:
        print(f"TwilioRestException: {str(e)}")
        return None

@app.route('/')
def registration_form():
    return render_template('registration.html', registration_submitted=False)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form
    first_name = data['first_name']
    last_name = data['last_name']
    phone_number = f"+{data['country_code']}{data['phone_number']}"  # Combine country code and phone number
    email = data['email']
    dob = data['dob']
    gender = data['gender']
    farm_details = data['farm_details']
    location = data['location']

    # Generate OTP and store it with the farmer's phone number
    otp = generate_otp()
    registered_farmers[phone_number] = otp

    # Send OTP to the farmer's phone number
    send_otp(phone_number, otp)

    return render_template('registration.html', registration_submitted=True)

@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.form
    phone_number = f"+{data['country_code']}{data['phone_number']}"  # Combine country code and phone number
    user_otp = data['otp']

    # Verify OTP
    stored_otp = registered_farmers.get(phone_number)
    if user_otp == stored_otp:
        return jsonify({'success': True, 'message': 'OTP validation successful.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)
