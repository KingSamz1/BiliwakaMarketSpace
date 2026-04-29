from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import uuid
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Mobile Money API configurations
MTN_API_URL = "https://api.mtn.com/v1"  # Replace with actual MTN API endpoint
AIRTEL_API_URL = "https://api.airtel.com/v1"  # Replace with actual Airtel API endpoint

# API Keys (should be stored in environment variables)
MTN_API_KEY = os.getenv("MTN_API_KEY", "your_mtn_api_key")
MTN_SECRET = os.getenv("MTN_SECRET", "your_mtn_secret")
AIRTEL_API_KEY = os.getenv("AIRTEL_API_KEY", "your_airtel_api_key")
AIRTEL_SECRET = os.getenv("AIRTEL_SECRET", "your_airtel_secret")

# In-memory storage for transactions (in production, use a database)
transactions = {}

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['provider', 'phone', 'amount', 'package', 'merchant']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        provider = data['provider']
        phone = data['phone']
        amount = data['amount']
        package = data['package']
        merchant = data['merchant']
        
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())
        
        # Store transaction details
        transactions[transaction_id] = {
            'provider': provider,
            'phone': phone,
            'amount': amount,
            'package': package,
            'merchant': merchant,
            'status': 'pending',
            'created_at': datetime.datetime.now().isoformat(),
            'reference_id': None
        }
        
        # Process payment based on provider
        if provider == "MTN Mobile Money":
            result = process_mtn_payment(transaction_id, phone, amount, merchant)
        elif provider == "Airtel Money":
            result = process_airtel_payment(transaction_id, phone, amount, merchant)
        else:
            return jsonify({'error': 'Unsupported provider'}), 400
        
        if result['success']:
            transactions[transaction_id]['status'] = 'sent'
            transactions[transaction_id]['reference_id'] = result.get('reference_id')
            
            return jsonify({
                'success': True,
                'transaction_id': transaction_id,
                'reference_id': result.get('reference_id'),
                'message': 'Payment request sent successfully'
            })
        else:
            transactions[transaction_id]['status'] = 'failed'
            transactions[transaction_id]['error'] = result.get('error')
            
            return jsonify({
                'success': False,
                'error': result.get('error', 'Payment processing failed')
            }), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def process_mtn_payment(transaction_id, phone, amount, merchant):
    """Process MTN Mobile Money payment"""
    try:
        # MTN Mobile Money API integration
        headers = {
            'Authorization': f'Bearer {get_mtn_token()}',
            'Content-Type': 'application/json',
            'X-Reference-Id': transaction_id
        }
        
        payload = {
            'amount': str(amount),
            'currency': 'UGX',
            'externalId': transaction_id,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': phone
            },
            'payee': {
                'partyIdType': 'MSISDN',
                'partyId': merchant
            },
            'payerMessage': f'Payment for {package}',
            'payeeNote': 'Biliwaka Advertising Payment'
        }
        
        # Make API call to MTN
        response = requests.post(
            f'{MTN_API_URL}/collection/v1_0/requesttopay',
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 202:  # Accepted for processing
            return {
                'success': True,
                'reference_id': response.headers.get('X-Reference-Id', transaction_id)
            }
        else:
            return {
                'success': False,
                'error': f'MTN API error: {response.status_code} - {response.text}'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'MTN API connection error: {str(e)}'
        }

def process_airtel_payment(transaction_id, phone, amount, merchant):
    """Process Airtel Money payment"""
    try:
        # Airtel Money API integration
        headers = {
            'Authorization': f'Bearer {get_airtel_token()}',
            'Content-Type': 'application/json',
            'X-Country': 'UG',
            'X-Currency': 'UGX'
        }
        
        payload = {
            'transaction_id': transaction_id,
            'amount': str(amount),
            'currency': 'UGX',
            'msisdn': phone,
            'payee': merchant,
            'description': f'Payment for advertising package'
        }
        
        # Make API call to Airtel
        response = requests.post(
            f'{AIRTEL_API_URL}/merchant/v1/payments',
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'reference_id': data.get('transaction_id', transaction_id)
            }
        else:
            return {
                'success': False,
                'error': f'Airtel API error: {response.status_code} - {response.text}'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Airtel API connection error: {str(e)}'
        }

def get_mtn_token():
    """Get MTN API token"""
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            'client_id': MTN_API_KEY,
            'client_secret': MTN_SECRET,
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(
            f'{MTN_API_URL}/collection/v1_0/oauth2/token',
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            raise Exception(f'Failed to get MTN token: {response.status_code}')
            
    except Exception as e:
        print(f"MTN Token Error: {e}")
        return "demo_token"  # Fallback for development

def get_airtel_token():
    """Get Airtel API token"""
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            'client_id': AIRTEL_API_KEY,
            'client_secret': AIRTEL_SECRET,
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(
            f'{AIRTEL_API_URL}/auth/oauth2/token',
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            raise Exception(f'Failed to get Airtel token: {response.status_code}')
            
    except Exception as e:
        print(f"Airtel Token Error: {e}")
        return "demo_token"  # Fallback for development

@app.route('/status/<transaction_id>', methods=['GET'])
def check_status(transaction_id):
    """Check transaction status"""
    if transaction_id not in transactions:
        return jsonify({'error': 'Transaction not found'}), 404
    
    transaction = transactions[transaction_id]
    
    # In production, you would check the actual API for status
    # For now, return the stored status
    return jsonify({
        'transaction_id': transaction_id,
        'status': transaction['status'],
        'reference_id': transaction.get('reference_id'),
        'created_at': transaction['created_at']
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})

if __name__ == '__main__':
    print("Starting Payment Server...")
    print("Available endpoints:")
    print("  POST /checkout - Process payment")
    print("  GET /status/<transaction_id> - Check transaction status")
    print("  GET /health - Health check")
    print("\nServer running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
