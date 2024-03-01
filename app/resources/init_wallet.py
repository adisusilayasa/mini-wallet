from flask_restful import Resource, reqparse
from app.models import Wallet
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

parser = reqparse.RequestParser()
parser.add_argument('customer_xid', type=str, required=True, help='Customer ID must be provided', location='form')

class InitWallet(Resource):
    def post(self):
        args = parser.parse_args()
        customer_xid = args['customer_xid']

        # Check if wallet already exists for the customer
        existing_wallet = Wallet.objects(customer_id=customer_xid).first()
        if existing_wallet:
            return {'status': 'error', 'message': 'Wallet already initialized for this customer'}, 400

        # Initialize wallet
        wallet = Wallet(customer_id=customer_xid)
        wallet.save()
        
        # Inside your initwallet endpoint
        # Generate token payload
        token_payload = {
            'customer_xid': customer_xid,  # Assuming customer_xid is available
            'exp': datetime.now() + timedelta(days=1)  # Token expiration time (e.g., 1 day)
        }

        # Generate JWT token
        token = create_access_token(identity=token_payload)
        response = {
            'access_token': token,
        }

        return {'status': 'success', 'message': 'Wallet initialized successfully', 'data': response}, 201
