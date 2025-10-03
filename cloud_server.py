from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
import requests
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Global state
system_status = {'running': False, 'error': None, 'earnings': 0}
notification_webhook = None

def send_notification(message, level='info'):
    """Send notification to phone via webhook"""
    if notification_webhook:
        try:
            requests.post(notification_webhook, json={
                'message': message,
                'level': level,
                'timestamp': datetime.now().isoformat()
            })
        except:
            pass

def run_orion_missions():
    """Background thread for simulated missions"""
    global system_status
    
    try:
        system_status['running'] = True
        send_notification('Orion system started successfully', 'success')
        
        while system_status['running']:
            try:
                # Simulate mission completion
                import random
                earnings = random.uniform(0.5, 5.0)
                system_status['earnings'] += earnings
                send_notification(f"Mission completed: ${earnings:.2f}", 'success')
                time.sleep(300)  # 5 minute delay between missions
                
            except Exception as e:
                send_notification(f"Mission error: {str(e)}", 'error')
                time.sleep(600)  # 10 minute delay on error
                
    except Exception as e:
        system_status['error'] = str(e)
        system_status['running'] = False
        send_notification(f"System error: {str(e)}", 'critical')

@app.route('/api/start', methods=['POST'])
def start_system():
    global system_status
    if not system_status['running']:
        threading.Thread(target=run_orion_missions, daemon=True).start()
        return jsonify({'status': 'starting'})
    return jsonify({'status': 'already_running'})

@app.route('/api/stop', methods=['POST'])
def stop_system():
    global system_status
    system_status['running'] = False
    send_notification('System stopped by user', 'info')
    return jsonify({'status': 'stopped'})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'running': system_status['running'],
        'error': system_status['error'],
        'earnings': system_status['earnings'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/webhook', methods=['POST'])
def set_webhook():
    global notification_webhook
    notification_webhook = request.json.get('url')
    return jsonify({'status': 'webhook_set'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)