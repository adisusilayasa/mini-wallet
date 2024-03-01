from flask_restful import Resource
from app.models import Wallet
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth_middleware import token_required

class Balance(Resource):
    @token_required
    def get(self):
        # Retrieve the wallet balance
        curr_user = get_jwt_identity()
        customer_xid = curr_user.get('customer_xid')
        wallet = Wallet.objects(customer_xid=customer_xid).first()
        if wallet:
            # Check if the wallet status is enabled
            if wallet.status == 'enabled':
                # Prepare the response data
                response_data = {
                    'status': 'success',
                    'data': {
                        'wallet': {
                            'id': str(wallet.id),
                            'owned_by': str(wallet.customer_xid),
                            'status': wallet.status,
                            'enabled_at': wallet.enabled_at.isoformat(),
                            'balance': float(wallet.balance)
                        }
                    }
                }
                return response_data, 200
            else:
                return {'status': 'error', 'message': 'Wallet is not enabled'}, 403
        else:
            return {'status': 'error', 'message': 'Wallet not found'}, 404
