from flask import Flask
from flask_restful import Api
from mongoengine import connect
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'mini_wallet_db',
    'host': 'mongodb://mongo:27017/mini_wallet_db'
}
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

api = Api(app)

# Connect to MongoDB using the default connection
connect('mini_wallet_db')

from app import routes

if __name__ == "__main__":
    app.run(debug=True)
