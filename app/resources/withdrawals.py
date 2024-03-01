from flask_restful import Resource, reqparse
from app.models import Wallet, Transaction
from datetime import datetime
from decimal import Decimal
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity

parser = reqparse.RequestParser()
parser.add_argument('amount', type=float, required=True, help='Amount must be provided')
parser.add_argument('reference_id', type=str, required=True, help='Reference ID must be provided')

class Withdrawal(Resource):
    @jwt_required()  # Require JWT token for this endpoint
    def post(self):
        args = parser.parse_args()
        amount = Decimal(args['amount'])  # Convert amount to Decimal
        reference_id = args['reference_id']

        # Retrieve customer ID from JWT token
        curr_user = get_jwt_identity()
        customer_xid = curr_user.get('customer_xid')
        
        # Check if wallet exists for the customer
        wallet = Wallet.objects(customer_xid=customer_xid).first()
        if not wallet:
            return {'status': 'error', 'message': 'Wallet not found for this customer'}, 404

        # Check if wallet status is enabled
        if wallet.status != 'enabled':
            return {'status': 'error', 'message': 'Wallet is not enabled'}, 403

        # Check if balance is sufficient for withdrawal
        if wallet.balance < amount:
            return {'status': 'error', 'message': 'Insufficient balance'}, 400

        # Add withdrawal
        transaction = Transaction(
            id=str(uuid.uuid4()),  # Generate a unique ID for the transaction
            withdrawn_by=customer_xid,
            status="success",  # Assuming status should be set to "success" initially
            amount=amount,
            reference_id=reference_id,
            withdrawn_at=datetime.utcnow()
        )
        transaction.save()

        # Update wallet balance
        wallet.balance -= amount  # Now both are Decimal objects
        wallet.save()

        # Construct response data
        withdrawal_data = {
            "id": str(transaction.id),
            "withdrawn_by": str(transaction.withdrawn_by),
            "status": transaction.status,
            "withdrawn_at": transaction.withdrawn_at.isoformat(),
            "amount": str(transaction.amount),  # Convert Decimal to string for JSON serialization
            "reference_id": transaction.reference_id
        }

        return {'status': 'success', 'data': {'withdrawal': withdrawal_data}}, 201
