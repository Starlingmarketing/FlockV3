# Gmail Draft Assistant Web

A web-based application for creating personalized Gmail draft emails using CSV contact data and the Perplexity API.

## Features

- **CSV Upload**: Import contacts including email addresses, names, and company information
- **Email Templates**: Create reusable email templates with personalization variables
- **AI-Generated Content**: Generate unique emails for each recipient using Perplexity API
- **Simple Web Interface**: Easy-to-use web interface accessible from any browser
- **Copy & Paste Workflow**: Copy generated emails directly into Gmail

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gmail-draft-assistant-web.git
   cd gmail-draft-assistant-web
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create an uploads directory:
   ```bash
   mkdir uploads
   ```

## Usage

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

### Main Workflow

1. **Setup**: Upload your CSV file with contact information and configure column mappings
2. **AI Settings** (optional): Configure your Perplexity API key and custom prompt template
3. **Drafts**: Generate and copy email content for each recipient
4. **Gmail**: Paste the content into Gmail compose window to create drafts

## CSV Format

The application expects a CSV file with at least the following columns:
- Email addresses (default: column C)
- First names (default: column A)
- Company names (default: column F)

You can specify different column mappings during setup.

## Perplexity API Integration

To use the AI email generation feature:

1. Sign up for a Perplexity API account at [docs.perplexity.ai](https://docs.perplexity.ai/docs/getting-started)
2. Obtain an API key from your Perplexity account
3. Configure the API key and settings in the app

## Deployment

### Local Development

For local development, simply run:
```bash
python app.py
```

### Production Deployment (Heroku)

1. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

2. Add a Procfile (already included in repo):
   ```
   web: gunicorn app:app
   ```

3. Deploy to Heroku:
   ```bash
   git push heroku main
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project is a web-based adaptation of the original desktop Gmail Draft Assistant
- Uses the Perplexity AI API for generating personalized email content
