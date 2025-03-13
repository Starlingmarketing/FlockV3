import json
import http.client
import ssl
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import OpenAI library if available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    logger.info("OpenAI client library detected")
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI client library not found, using direct HTTP requests")

def test_api_connection(api_key, model="sonar"):
    """
    Test the connection to the Perplexity API
    
    Args:
        api_key (str): Perplexity API key
        model (str): Model to use
        
    Returns:
        dict: Result of the API test
    """
    logger.info(f"Testing Perplexity API connection with model: {model}")
    
    try:
        # Try using OpenAI client if available
        if OPENAI_AVAILABLE:
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.perplexity.ai"
                )
                
                # Simple test messages
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": "Say hello and confirm that this API connection is working correctly."
                    }
                ]
                
                # Make the API call
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=100,
                    top_p=0.9,
                    frequency_penalty=0.0,
                    presence_penalty=0,
                    stream=False
                )
                
                content = response.choices[0].message.content
                
                return {
                    'success': True,
                    'content': content,
                    'usage': {
                        'completion_tokens': response.usage.completion_tokens,
                        'prompt_tokens': response.usage.prompt_tokens,
                        'total_tokens': response.usage.total_tokens
                    },
                    'model': response.model
                }
                
            except Exception as e:
                logger.error(f"Error with OpenAI client: {str(e)}. Falling back to HTTP requests.")
        
        # If OpenAI client is not available or failed, use direct HTTP requests
        context = ssl._create_unverified_context()
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm that this API connection is working correctly."}
            ],
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0,
            "stream": False
        }
        
        json_payload = json.dumps(payload)
        
        # Create the connection
        conn = http.client.HTTPSConnection("api.perplexity.ai", context=context)
        
        # Send the request
        conn.request("POST", "/chat/completions", json_payload, headers)
        
        # Get the response
        response = conn.getresponse()
        status = response.status
        response_data = response.read().decode()
        
        # Close the connection
        conn.close()
        
        if status == 200:
            data = json.loads(response_data)
            content = data["choices"][0]["message"]["content"] if "choices" in data and len(data["choices"]) > 0 else ""
            
            return {
                'success': True,
                'content': content,
                'usage': data.get('usage', {}),
                'model': data.get('model', model)
            }
        else:
            error_data = json.loads(response_data)
            error_message = error_data.get('error', {}).get('message', 'Unknown error')
            
            return {
                'success': False,
                'error': error_message,
                'status': status
            }
            
    except Exception as e:
        logger.error(f"API test error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def generate_email(api_key, model, prompt_template, first_name, company, temperature=0.7, top_p=0.9, freq_penalty=0.0):
    """
    Generate an email using the Perplexity API
    
    Args:
        api_key (str): Perplexity API key
        model (str): Model to use
        prompt_template (str): Template for the prompt
        first_name (str): Recipient's first name
        company (str): Recipient's company
        temperature (float): Temperature parameter (0.0-1.0)
        top_p (float): Top p parameter (0.0-1.0)
        freq_penalty (float): Frequency penalty parameter (0.0-2.0)
        
    Returns:
        str: Generated email body
    """
    # Replace variables in the prompt
    prompt = prompt_template.replace("{first_name}", first_name).replace("{company}", company)
    
    logger.info(f"Generating email for {first_name} at {company} using model {model}")
    
    try:
        # Try using OpenAI client if available
        if OPENAI_AVAILABLE:
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.perplexity.ai"
                )
                
                # Prepare messages
                messages = [
                    {
                        "role": "system",
                        "content": "You are a personal assistant who writes highly personalized, authentic-sounding emails."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                
                # Make the API call
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=800,
                    top_p=top_p,
                    frequency_penalty=freq_penalty,
                    presence_penalty=0,
                    stream=False
                )
                
                # Extract the generated content
                generated_text = response.choices[0].message.content.strip()
                return generated_text
                
            except Exception as e:
                logger.error(f"Error with OpenAI client: {str(e)}. Falling back to HTTP requests.")
        
        # If OpenAI client is not available or failed, use direct HTTP requests
        context = ssl._create_unverified_context()
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a personal assistant who writes highly personalized, authentic-sounding emails."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 800,
            "top_p": top_p,
            "frequency_penalty": freq_penalty,
            "presence_penalty": 0,
            "stream": False
        }
        
        json_payload = json.dumps(payload)
        
        # Create the connection
        conn = http.client.HTTPSConnection("api.perplexity.ai", context=context)
        
        # Send the request
        conn.request("POST", "/chat/completions", json_payload, headers)
        
        # Get the response
        response = conn.getresponse()
        response_data = response.read().decode()
        
        # Close the connection
        conn.close()
        
        if response.status == 200:
            data = json.loads(response_data)
            
            if "choices" in data and len(data["choices"]) > 0:
                generated_text = data["choices"][0]["message"]["content"].strip()
                return generated_text
            else:
                raise Exception("No text generated from API")
        else:
            error_data = json.loads(response_data)
            error_message = error_data.get('error', {}).get('message', 'Unknown error')
            raise Exception(f"API Error: {error_message}")
            
    except Exception as e:
        logger.error(f"Email generation error: {str(e)}")
        raise Exception(f"Failed to generate email: {str(e)}")

def generate_template_email(first_name, company, template):
    """
    Generate a personalized email using a template
    
    Args:
        first_name (str): Recipient's first name
        company (str): Recipient's company
        template (str): Email template
        
    Returns:
        str: Personalized email body
    """
    # Replace template variables
    email_body = template.replace("{first_name}", first_name).replace("{company}", company)
    return email_body
