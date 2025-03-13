import os
import json
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from utils.csv_handler import parse_csv_file, get_column_values
from utils.perplexity_api import generate_email, test_api_connection

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """CSV upload and configuration page"""
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'csvFile' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
            
        file = request.files['csvFile']
        
        # Check if file is empty
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
            
        # Check if file is a CSV
        if file and allowed_file(file.filename):
            # Save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse the CSV file
            try:
                headers = parse_csv_file(filepath, preview_only=True)
                
                # Store filepath in session
                session['csv_filepath'] = filepath
                session['csv_filename'] = filename
                
                # Get column mappings from form
                email_col = request.form.get('emailColumn', '').strip().upper()
                firstname_col = request.form.get('firstNameColumn', '').strip().upper()
                company_col = request.form.get('companyColumn', '').strip().upper()
                
                # Store column mappings in session
                session['email_column'] = email_col
                session['firstname_column'] = firstname_col
                session['company_column'] = company_col
                
                # Store template information if provided
                use_template = 'useTemplate' in request.form
                session['use_template'] = use_template
                
                if use_template:
                    session['template_subject'] = request.form.get('subject', '')
                    session['template_body'] = request.form.get('body', '')
                
                # Store AI flag
                session['use_ai'] = 'useAI' in request.form
                
                flash('CSV file uploaded successfully!', 'success')
                
                # Redirect to AI settings or drafts page
                if session['use_ai']:
                    return redirect(url_for('ai_settings'))
                else:
                    return redirect(url_for('drafts'))
                    
            except Exception as e:
                flash(f'Error parsing CSV file: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Only CSV files are allowed', 'error')
            return redirect(request.url)
            
    return render_template('setup.html')

@app.route('/ai-settings', methods=['GET', 'POST'])
def ai_settings():
    """Perplexity API settings page"""
    if 'csv_filepath' not in session:
        flash('Please upload a CSV file first', 'error')
        return redirect(url_for('setup'))
        
    if request.method == 'POST':
        # Get API settings from form
        api_key = request.form.get('apiKey', '').strip()
        model = request.form.get('model', 'sonar').strip()
        temperature = float(request.form.get('temperature', 0.7))
        top_p = float(request.form.get('topP', 0.9))
        freq_penalty = float(request.form.get('freqPenalty', 0.0))
        custom_prompt = request.form.get('customPrompt', '').strip()
        
        # Validate API key
        if not api_key:
            flash('API key is required', 'error')
            return redirect(request.url)
            
        # Validate custom prompt
        if not custom_prompt:
            flash('Custom prompt is required', 'error')
            return redirect(request.url)
            
        # Store settings in session
        session['api_key'] = api_key
        session['model'] = model
        session['temperature'] = temperature
        session['top_p'] = top_p
        session['freq_penalty'] = freq_penalty
        session['custom_prompt'] = custom_prompt
        
        flash('AI settings saved successfully!', 'success')
        return redirect(url_for('drafts'))
        
    # Pre-fill the form with default values
    default_prompt = """Write a personalized email to {first_name} who works at {company}. 

Make the email:
1. Sound natural and conversational
2. Reference something specific about {company} that shows knowledge of their business
3. Be 3-4 short paragraphs (not too lengthy)
4. Include a clear call to action
5. Use a friendly, professional tone

Do not include a subject line or signature - just the body text."""

    return render_template('ai_settings.html', 
                         default_prompt=default_prompt)

@app.route('/test-api', methods=['POST'])
def test_api():
    """Test the Perplexity API connection"""
    api_key = request.json.get('apiKey', '').strip()
    model = request.json.get('model', 'sonar').strip()
    
    if not api_key:
        return jsonify({'success': False, 'message': 'API key is required'})
        
    result = test_api_connection(api_key, model)
    return jsonify(result)

@app.route('/drafts')
def drafts():
    """Email drafts page"""
    if 'csv_filepath' not in session:
        flash('Please upload a CSV file first', 'error')
        return redirect(url_for('setup'))
        
    # Get email data from CSV
    try:
        filepath = session['csv_filepath']
        email_col = session['email_column']
        firstname_col = session['firstname_column']
        company_col = session['company_column']
        
        # Extract data from CSV
        emails = get_column_values(filepath, email_col)
        first_names = get_column_values(filepath, firstname_col)
        companies = get_column_values(filepath, company_col)
        
        # Create a list of recipients
        recipients = []
        for i in range(min(len(emails), len(first_names), len(companies))):
            recipients.append({
                'email': emails[i],
                'first_name': first_names[i],
                'company': companies[i]
            })
            
        return render_template('drafts.html', 
                             recipients=recipients, 
                             use_ai=session.get('use_ai', False),
                             template_subject=session.get('template_subject', ''),
                             template_body=session.get('template_body', ''))
    except Exception as e:
        flash(f'Error processing CSV data: {str(e)}', 'error')
        return redirect(url_for('setup'))

@app.route('/generate-email', methods=['POST'])
def generate_email_route():
    """Generate an email using the Perplexity API"""
    if 'api_key' not in session or not session['use_ai']:
        return jsonify({'success': False, 'message': 'API key not configured or AI not enabled'})
        
    data = request.json
    first_name = data.get('firstName', '')
    company = data.get('company', '')
    
    try:
        # Generate email using Perplexity API
        email_body = generate_email(
            session['api_key'],
            session['model'],
            session['custom_prompt'],
            first_name,
            company,
            session['temperature'],
            session['top_p'],
            session['freq_penalty']
        )
        
        return jsonify({
            'success': True,
            'email_body': email_body
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating email: {str(e)}'
        })

@app.route('/success')
def success():
    """Success page"""
    # Clear session data
    session.clear()
    return render_template('success.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
