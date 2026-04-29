# Mobile Money Payment Integration Setup

## Overview
This guide shows how to set up real mobile money APIs for the Biliwaka marketplace payment system.

## Files Created
- `payment_server.py` - Flask backend server for payment processing
- `.env.example` - Environment variables template
- `requirements_payment.txt` - Payment server dependencies

## Setup Instructions

### 1. Install Dependencies
```bash
# Install payment server dependencies
pip install -r requirements_payment.txt

# Or install individually
pip install flask flask-cors requests python-dotenv
```

### 2. Configure API Keys
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys
nano .env
```

Add your real API credentials:
```env
# MTN Mobile Money API
MTN_API_KEY=your_actual_mtn_api_key
MTN_SECRET=your_actual_mtn_secret
MTN_API_URL=https://api.mtn.com/v1

# Airtel Money API  
AIRTEL_API_KEY=your_actual_airtel_api_key
AIRTEL_SECRET=your_actual_airtel_secret
AIRTEL_API_URL=https://api.airtel.com/v1
```

### 3. Start the Payment Server
```bash
# Run the payment server (in a separate terminal)
python payment_server.py
```

The server will start on `http://localhost:5000` with these endpoints:
- `POST /checkout` - Process payment
- `GET /status/<transaction_id>` - Check transaction status  
- `GET /health` - Health check

### 4. Test the Integration
1. Make sure the payment server is running
2. Go to the payment page in your Biliwaka app
3. Select a package and enter phone number
4. Click "Pay Now" - it should connect to the real API

## API Integration Details

### MTN Mobile Money API
The system integrates with MTN's Mobile Money API using:
- OAuth 2.0 authentication
- Collection API for payments
- Real-time transaction status

**Required from MTN:**
- API Client ID and Secret
- Collection API access
- Sandbox/Production environment details

### Airtel Money API
The system integrates with Airtel's Money API using:
- OAuth 2.0 authentication  
- Merchant payment API
- Transaction tracking

**Required from Airtel:**
- API Client ID and Secret
- Merchant payment access
- Environment credentials

## Production Considerations

### Security
- Store API keys in environment variables (never in code)
- Use HTTPS in production
- Implement webhook signatures for verification
- Add rate limiting and fraud detection

### Database
- Replace in-memory storage with proper database
- Store transaction history
- Implement retry logic for failed transactions
- Add audit logging

### Monitoring
- Add logging for all transactions
- Monitor API response times
- Set up alerts for failures
- Track success rates

## Testing in Sandbox Mode

Both MTN and Airtel provide sandbox environments for testing:

### MTN Sandbox
- Use MTN's sandbox credentials
- Test with test phone numbers
- Simulate different transaction scenarios

### Airtel Sandbox  
- Use Airtel's test environment
- Mock transactions for development
- Test error handling

## Troubleshooting

### Common Issues
1. **"Cannot connect to payment server"**
   - Ensure payment_server.py is running
   - Check it's on localhost:5000
   - Verify no firewall blocking

2. **"API authentication failed"**
   - Check API keys in .env file
   - Verify keys are correct for sandbox/production
   - Ensure API credentials are active

3. **"Transaction failed"**
   - Check phone number format (2567XXXXXXXX)
   - Verify merchant number is correct
   - Check sufficient API permissions

## Getting Real API Access

### MTN Uganda
1. Contact MTN Uganda Business team
2. Apply for Mobile Money API access
3. Complete compliance requirements
4. Receive sandbox credentials for testing
5. Upgrade to production after testing

### Airtel Uganda
1. Contact Airtel Money business team
2. Apply for Merchant API access
3. Complete KYC and compliance
4. Get sandbox environment access
5. Move to production after successful testing

## Support
For issues with the payment integration:
- Check server logs: `python payment_server.py` shows console output
- Review API documentation from MTN/Airtel
- Test with sandbox environments first
- Contact mobile money providers for API support
