from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from plutus import Plutus
from architect import Architect

app = Flask(__name__)
CORS(app)

# Initialize core modules
plutus = Plutus()
architect = Architect()

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'active': True,
        'total_earnings': plutus.get_total_earnings(),
        'active_missions': architect.get_active_missions(),
        'sites_count': 435
    })

@app.route('/api/earnings', methods=['GET'])
def get_earnings():
    return jsonify({
        'crypto': plutus.get_crypto_balance(),
        'gift_cards': plutus.get_gift_card_balance(),
        'total_usd': plutus.get_total_usd_value(),
        'today': plutus.get_daily_earnings()
    })

@app.route('/api/missions', methods=['GET'])
def get_missions():
    return jsonify({
        'active': architect.get_active_missions(),
        'completed_today': architect.get_daily_completions(),
        'success_rate': architect.get_success_rate()
    })

@app.route('/api/control/<action>', methods=['POST'])
def control_system(action):
    if action == 'start':
        architect.start_missions()
        return jsonify({'status': 'started'})
    elif action == 'stop':
        architect.stop_missions()
        return jsonify({'status': 'stopped'})
    elif action == 'pause':
        architect.pause_missions()
        return jsonify({'status': 'paused'})
    return jsonify({'error': 'invalid action'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)