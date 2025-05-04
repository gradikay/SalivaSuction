import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure logging
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Log the form submission for now
        # In a real app, you would save to a database or send an email
        logger.info(f"Contact form submission: {name} ({email}): {message}")
        
        flash('Thank you for your inquiry! We will contact you shortly.', 'success')
        return redirect(url_for('index', _anchor='contact'))
    
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        flash('There was an error processing your request. Please try again.', 'error')
        return redirect(url_for('index', _anchor='contact'))

# Add error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html'), 500
