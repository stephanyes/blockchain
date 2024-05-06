from uuid import uuid4
from flask import Flask, jsonify, request, make_response
from flask_cors import cross_origin
from blockchain import create_app, create_blockchain

app = create_app()
blockchain = create_blockchain()

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.route('/demo', methods=['GET'])
def demo():
    try:
        # Create two wallets
        wallet1 = blockchain.create_wallet()
        wallet2 = blockchain.create_wallet()
        
        app.logger.info('%s wallet stored in our blockchain.', wallet1.address)
        app.logger.info('%s wallet stored in our blockchain.', wallet2.address)
        
        # Generate 5 transactions between wallet1 and wallet2
        for _ in range(5):
            blockchain.new_transaction(wallet1.address, wallet2.address, 10)
            blockchain.new_transaction(wallet2.address, wallet1.address, 10)  # Reverse transaction
        
        # Return the response
        return jsonify({
            'message': 'Demo completed',
            'transactions': 5,
            'wallet1': wallet1.address,
            'wallet2': wallet2.address
        }), 200
    except Exception as e:
        # Log the error
        app.logger.error(f"An error occurred: {e}")
        # Return an error response
        return jsonify({'error': 'An error occurred during the demo.'}), 500

@app.route('/mine', methods=['GET'])
def mine():
    try:
        # Mine a new block
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)
        previous_hash = blockchain.hash(last_block)
        blockchain.new_transaction(
            sender_address="0",  # Sender is "0" to denote a mining reward
            recipient_address=node_identifier,
            amount=1,  # Mining reward
        )
        block = blockchain.new_block(proof, previous_hash)

        # Convert public keys to strings for JSON serialization
        serialized_wallets = {}
        for address, wallet in blockchain.wallets.items():
            serialized_wallets[wallet.address] = {
                'public_key': wallet.public_key_str,  # Use the stored string representation
                'balance': wallet.balance
            }

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'wallets': serialized_wallets  # Include serialized wallets in the response
        }
        return jsonify(response), 200
    except Exception as e:
        app.logger.error(f"An error occurred while mining a new block: {str(e)}")
        return jsonify({'message': 'An error occurred'}), 500

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    try:
        values = request.get_json()

        # Check that the required fields are in the POST'ed data
        required = ['sender_public_key', 'recipient_public_key', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['sender_public_key'], values['recipient_public_key'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/transactions/verify-transaction', methods=['POST'])
@cross_origin()
def demo_verify_transaction():
    # Ensure that the request contains JSON data
    if not request.json:
        abort(400, description="Request must be in JSON format")
    # Extract parameters from the request body
    sender = request.json.get('sender')
    recipient = request.json.get('recipient')
    amount = int(request.json.get('amount'))
    signature = request.json.get('signature')

    # Validate the presence of required parameters
    if not all([sender, recipient, amount, signature]):
        abort(400, description="Missing required parameters")
    
    sender_wallet = blockchain.wallets.get(sender)
    # Create a new transaction dictionary
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'signature': signature,
        'sender_public_key': sender_wallet.public_key
    }
    # Verify the transaction signature using the sender's public key
    verification_result = blockchain.verify_transaction(transaction)

    # Return the verification result
    if verification_result:
        return jsonify({'message': 'Transaction signature is valid.'}), 200
    else:
        return jsonify({'message': 'Transaction signature is invalid.'}), 400

@app.route('/transactions/address', methods=['GET'])
def get_all_transactions():
    try:
        # Ensure that the request contains JSON data
        if not request.json:
            abort(400, description="Request must be in JSON format")
        
        # Extract parameters from the request body
        address = request.json.get('address')
        print('Address retrieved ', address)
        result = blockchain.get_transactions(address)
        
        # Return the verification result
        if result:
            return jsonify({'message': 'Transactions found!.', 'transactions': result}), 200
        else:
            return jsonify({'message': 'No Transactions found.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@app.route('/transactions/id', methods=['GET'])
def get_transaction_by_id():
    try:
        # Ensure that the request contains JSON data
        if not request.json:
            abort(400, description="Request must be in JSON format")
        
        # Extract parameters from the request body
        txID = request.json.get('txID')
        print('Transaction ID retrieved ', txID)
        result = blockchain.get_transaction_by_id(txID)
        
        # Return the verification result
        if result:
            return jsonify({'message': 'Transaction found!.', 'transactions': result}), 200
        else:
            return jsonify({'message': 'No Transaction found.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transactions/seed', methods=['POST'])
def create_transactions():
    """
    Endpoint to create a specified number of transactions.
    Expects JSON data in the request body with sender, recipient, amount, and rounds.
    """
    try:
        data = request.get_json()

        # Check if all required fields are present in the request data
        required_fields = ['sender', 'recipient', 'amount', 'rounds']
        if not all(field in data for field in required_fields):
            raise ValueError('Missing required fields in JSON data')

        sender = data['sender']
        recipient = data['recipient']
        amount = data['amount']
        rounds = data['rounds']

        # Validate amount and rounds as positive integers
        if not isinstance(amount, int) or not isinstance(rounds, int) or amount <= 0 or rounds <= 0:
            raise ValueError('Amount and rounds must be positive integers')

        # Create specified number of transactions
        for _ in range(rounds):
            blockchain.new_transaction(sender, recipient, amount)

        return jsonify({'message': f'{rounds} transactions created successfully'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

@app.route('/create-wallet', methods=['GET'])
def create_wallet():
    """
    Endpoint to create a new wallet and return its details
    """
    try:
        wallet = blockchain.create_wallet()
        return jsonify({
            'address': wallet.address,
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'balance': wallet.balance
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/wallets', methods=['GET'])
def fetch_wallets():
    """
    Endpoint to create a new wallet and return its details
    """
    try:
        return jsonify({
            'wallets': blockchain.wallets,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
