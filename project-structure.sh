gmail-draft-assistant-web/
├── app.py                      # Main Flask application
├── requirements.txt            # Dependencies for deployment
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/                  # HTML templates
│   ├── base.html               # Base template with common elements
│   ├── index.html              # Home page
│   ├── setup.html              # CSV upload and configuration
│   ├── ai_settings.html        # Perplexity API settings
│   ├── drafts.html             # Email drafts page
│   └── success.html            # Success page
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── csv_handler.py          # CSV processing
│   └── perplexity_api.py       # Perplexity API integration
└── README.md                   # Documentation
