from flask_restful import Resource, reqparse
from app.models import Wallet
from flask_jwt_extended import jwt_required, get_jwt_identity

class DisableWallet(Resource):
    @jwt_required()  # Require JWT token for this endpoint
    def patch(self):

        # Retrieve customer ID from JWT token
        curr_user = get_jwt_identity()
        customer_xid = curr_user.get('customer_xid')
        
        # Check if wallet exists for the customer
        wallet = Wallet.objects(customer_id=customer_xid).first()
        if not wallet:
            return {'status': 'error', 'message': 'Wallet not found for this customer'}, 404

        # Enable wallet
        wallet.status = 'disabled'
        wallet.save()

        return {'status': 'success', 'message': 'Wallet disabled successfully'}, 200
