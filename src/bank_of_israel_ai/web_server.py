"""Flask web server for the procurement agent."""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from .agents.procurement_agent import ProcurementRequest, run_procurement_agent
import re
import threading

app = Flask(__name__, template_folder='templates', static_folder='static')
load_dotenv()

def extract_email_from_prompt(prompt: str) -> tuple[str, str, bool]:
    """Extract product query, email, and whether to send email from user prompt.
    
    Returns:
        (product_query, email, should_send_email)
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, prompt)
    
    send_email_keywords = r'(שלח|תשלח|email|mail|send to|ותשלח|send me)'
    should_send_email = bool(re.search(send_email_keywords, prompt, re.IGNORECASE))
    
    if emails:
        email = emails[0]
        query = prompt.replace(email, "").strip()
        query = re.sub(r'(ותשלח ל-?|and send to|email|mail|send)', '', query, flags=re.IGNORECASE).strip()
        return query, email, should_send_email
    
    default_email = os.getenv("EMAIL_TO", "dvorizing@gmail.com")
    return prompt, default_email, should_send_email


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Handle procurement search request."""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'error': 'Empty prompt'}), 400
        
        query, email, should_send_email = extract_email_from_prompt(prompt)
        
        if not query:
            return jsonify({'error': 'Could not extract product from prompt'}), 400
        
        request_obj = ProcurementRequest(query=query)
        
        results = run_procurement_agent(
            request=request_obj,
            send_email_results=should_send_email,
            env_path=".env"
        )
        
        email_status = f"📧 תוצאות שלחו ל- {email}" if should_send_email else f"📧 (לא נשלחו תוצאות למייל - כדי לשלוח כתוב 'שלח מייל')"
        
        return jsonify({
            'success': True,
            'product': query,
            'email': email,
            'should_send_email': should_send_email,
            'email_status': email_status,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def run_web():
    """Run the Flask web server."""
    print("\n" + "="*80)
    print("🌐 BANK OF ISRAEL AI - WEB INTERFACE")
    print("="*80)
    print("\n📍 Opening: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    run_web()
