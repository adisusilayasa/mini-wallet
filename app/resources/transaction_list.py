from flask_restful import Resource
from app.models import Transaction, Wallet
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.json_util import dumps
from mongoengine.queryset.visitor import Q  # Add this import

class TransactionList(Resource):
    @jwt_required()  # Require JWT token for this endpoint
    def get(self):
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

        # Retrieve transactions for the customer
        transactions = Transaction.objects(
            Q(withdrawn_by=customer_xid) | Q(deposited_by=customer_xid)
        )

        # Serialize the transactions directly into JSON format
        serialized_transactions = []
        for transaction in transactions:
            transaction_data = {
                'id': str(transaction.id),
                'withdrawn_by': str(transaction.withdrawn_by),
                'deposited_by': str(transaction.deposited_by),
                'status': transaction.status,
                'amount': float(transaction.amount),
                'reference_id': transaction.reference_id,
                'deposited_at': str(transaction.deposited_at),
                'withdrawn_at': str(transaction.withdrawn_at)
                
            }
            serialized_transactions.append(transaction_data)

        return {'status': 'success', 'data': serialized_transactions}, 200
