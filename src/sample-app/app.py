"""
Flask Web Application for HR Chatbot Demo
Provides a simple web interface for the vulnerable RAG system
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from chatbot import HRChatbot

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-prod')

# Initialize chatbot
chatbot = HRChatbot()


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def ask():
    """API endpoint to ask questions"""
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        response = chatbot.ask(question)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get system statistics"""
    return jsonify({
        'mode': os.getenv('WORKSHOP_MODE', 'demo'),
        'vulnerabilities_enabled': os.getenv('ENABLE_VULNERABILITIES', 'true').lower() == 'true',
        'protections_enabled': os.getenv('ENABLE_PROTECTIONS', 'false').lower() == 'true'
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Starting HR Chatbot on port {port}")
    print(f"Workshop Mode: {os.getenv('WORKSHOP_MODE', 'demo')}")
    print(f"Vulnerabilities Enabled: {os.getenv('ENABLE_VULNERABILITIES', 'true')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
