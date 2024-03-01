from flask_restful import Resource, reqparse
from app.models import Wallet, Transaction
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid  # Add this line at the top of your script
from decimal import Decimal

parser = reqparse.RequestParser()
parser.add_argument('amount', type=float, required=True, help='Amount must be provided', location='form')
parser.add_argument('reference_id', type=str, required=True, help='Reference ID must be provided', location='form')

class Deposit(Resource):
    @jwt_required()  # Require JWT token for this endpoint
    def post(self):
        args = parser.parse_args()
        amount = Decimal(args['amount'])  # Convert amount to Decimal
        reference_id = args['reference_id']

        # Retrieve customer ID from JWT token
        curr_user = get_jwt_identity()
        customer_xid = curr_user.get('customer_xid')
        
        wallet = Wallet.objects(customer_id=customer_xid).first()
        if not wallet:
            return {'status': 'error', 'message': 'Wallet not found for this customer'}, 404

        # Check if wallet status is enabled
        if wallet.status != 'enabled':
            return {'status': 'error', 'message': 'Wallet is not enabled'}, 403

        # Add deposit
        transaction = Transaction(
            id=str(uuid.uuid4()),  # Generate a unique ID for the transaction
            status="success",  # Assuming status should be set to "success" initially
            deposited_by=customer_xid,
            amount=amount,
            reference_id=reference_id,
            deposited_at=datetime.utcnow()
        )
        transaction.save()

        # Update wallet balance
        wallet.balance += amount
        wallet.save()

        # Construct response data
        deposit_data = {
            "id": str(transaction.id),
            "deposited_by": str(transaction.deposited_by),
            "status": "success",
            "deposited_at": transaction.deposited_at.isoformat(),
            "amount": float(transaction.amount),
            "reference_id": transaction.reference_id
        }

        return {'status': 'success', 'data': {'deposit': deposit_data}}, 201
