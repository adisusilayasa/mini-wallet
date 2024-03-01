from flask import jsonify
from flask_restful import Resource
from app import api
from app.resources import transaction_list, balance, deposits, withdrawals, init_wallet, enable_wallet, disable_wallet

# Define API resources
api.add_resource(balance.Balance, '/api/v1/wallet')
api.add_resource(deposits.Deposit, '/api/v1/wallet/deposits')
api.add_resource(withdrawals.Withdrawal, '/api/v1/wallet/withdrawals')
api.add_resource(init_wallet.InitWallet, '/api/v1/init')
api.add_resource(enable_wallet.EnableWallet, '/api/v1/wallet')
api.add_resource(disable_wallet.DisableWallet, '/api/v1/wallet')
api.add_resource(transaction_list.TransactionList, '/api/v1/wallet/transactions')
