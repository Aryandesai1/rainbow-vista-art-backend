from flask import Flask, send_from_directory, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)
# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # SMTP username
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # SMTP password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default sender email

mail = Mail(app)

# Serve the React app (index.html) for all routes that are not APIs
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

# This is important for routing in React when users visit nested URLs
@app.route('/<path:path>')
def serve_react_with_path(path):
    return send_from_directory(app.static_folder, 'index.html')

# Contact form API
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Create email content
    msg = Message(f"New Contact Form Submission from {name}",
                  recipients=['rainbowvistaart@gmail.com'])  # Your email as the recipient
    msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    try:
        # Send the email
        mail.send(msg)
        return jsonify({"status": "success", "message": "Thanks! Your message has been sent."})
    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to send email.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
