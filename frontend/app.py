from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.exception_manager import ExceptionManager
from backend.email_scanner import EmailScanner
from backend.logging_module import setup_logging

app = Flask(__name__)
logger = setup_logging()

# Initialize components
exception_manager = ExceptionManager()
email_scanner = EmailScanner()

@app.route('/')
def index():
    """
    Main dashboard route
    """
    try:
        # Fetch recent logs and exceptions
        recent_logs = _get_recent_logs()
        exceptions = exception_manager.get_exceptions()
        
        return render_template('dashboard.html', 
                               logs=recent_logs, 
                               exceptions=exceptions)
    except Exception as e:
        logger.error(f"Dashboard rendering error: {e}")
        return render_template('error.html', error=str(e))

@app.route('/exceptions', methods=['GET', 'POST'])
def manage_exceptions():
    """
    Manage DLP exceptions
    """
    if request.method == 'POST':
        try:
            # Extract exception data from form
            exception_data = {
                'type': request.form.get('type'),
                'value': request.form.get('value'),
                'expiration': request.form.get('expiration')
            }
            
            # Add exception
            exception_manager.add_exception(exception_data)
            
            logger.info(f"New exception added: {exception_data}")
            return redirect(url_for('index'))
        
        except Exception as e:
            logger.error(f"Exception management error: {e}")
            return render_template('error.html', error=str(e))
    
    # GET request - show exceptions form
    return render_template('exceptions.html', 
                           exception_types=exception_manager.EXCEPTION_TYPES)

@app.route('/scan_email', methods=['GET', 'POST'])
def scan_email():
    """
    Manual email scanning route
    """
    if request.method == 'POST':
        try:
            # Check if file is uploaded
            if 'email_file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            email_file = request.files['email_file']
            
            # Save temporary file
            temp_path = os.path.join('/tmp', email_file.filename)
            email_file.save(temp_path)
            
            # Scan email
            scan_result = email_scanner.process_email(temp_path)
            
            # Remove temporary file
            os.remove(temp_path)
            
            return jsonify(scan_result), 200
        
        except Exception as e:
            logger.error(f"Email scanning error: {e}")
            return jsonify({'error': str(e)}), 500
    
    return render_template('scan_email.html')

def _get_recent_logs(limit=50):
    """
    Retrieve recent logs
    """
    try:
        # In a real-world scenario, you'd implement log retrieval from a log file
        # This is a placeholder implementation
        with open('/var/log/dlp_email_solution/dlp_email.log', 'r') as log_file:
            logs = log_file.readlines()[-limit:]
        return logs
    except Exception as e:
        logger.error(f"Log retrieval error: {e}")
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)