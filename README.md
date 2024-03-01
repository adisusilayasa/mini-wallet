## Running Mini Wallet Project

### Introduction
This documentation provides step-by-step instructions on how to run the Mini Wallet project. The Mini Wallet project is a Flask-based web application that allows users to manage their digital wallets, make deposits, withdrawals, and view transaction history.

### Prerequisites
- Python 3.x
- Docker
- Postman (optional, for API testing)

### Setup Environment
1. Clone the project repository:
   ```
   git clone <project repository>
   ```

2. Navigate to the project directory:
   ```
   cd mini-wallet
   ```

3. Install Docker and Docker Compose if not already installed.

### Running with Docker
1. Start Docker Compose to spin up the required containers:
   ```
   docker-compose up -d
   ```

### Running without Docker
1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```
     source venv/bin/activate
     ```

3. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```

### Running the Server
1. Start the Flask server:
   ```
   python3 run.py
   ```

### Accessing the API
- The API endpoints can be accessed using Postman or any other REST client.
- Base URL: `http://localhost:5000/api/v1/`

### Importing Postman Collection
1. Open Postman.
2. Import the provided Postman collection file.
3. You can now use the imported requests to interact with the Mini Wallet API.

### Conclusion
You have successfully set up and run the Mini Wallet project. You can now use the provided API endpoints to manage digital wallets and perform transactions. If you encounter any issues, please refer to the troubleshooting section in the documentation or reach out to the project maintainers for assistance.
