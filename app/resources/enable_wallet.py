from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Wallet
from datetime import datetime
from app.auth_middleware import token_required

class EnableWallet(Resource):
    @jwt_required()  # Require JWT token for this endpoint
    # @token_required  # Require JWT token for this endpoint
    def post(self):

        # Retrieve customer ID from JWT token
        curr_user = get_jwt_identity()
        customer_xid = curr_user.get('customer_xid')

        # Check if wallet exists for the customer
        wallet = Wallet.objects(customer_id=customer_xid).first()
        if not wallet:
            return {'status': 'error', 'message': 'Wallet not found for this customer'}, 404

        # Enable wallet
        wallet.status = 'enabled'
        wallet.enabled_at = datetime.now()
        wallet.save()

        # Prepare the response data
        response_data = {
            'status': 'success',
            'data': {
                'wallet': {
                    'id': str(wallet.id),
                    'owned_by': str(wallet.customer_id),
                    'status': wallet.status,
                    'enabled_at': wallet.enabled_at.isoformat(),
                    'balance': float(wallet.balance)
                }
            }
        }

        return response_data, 200
