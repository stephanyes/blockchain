import hashlib
import base58
import json
import uuid
import rsa
import base64
import requests
import logging
import os
from dotenv import load_dotenv
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

class Wallet:
    def __init__(self):
        # Generate RSA key pair
        self.public_key_obj, self.private_key_obj = rsa.newkeys(512)  # Example key size, adjust as needed
        
        # Serialize public and private keys to strings
        self.public_key = self.public_key_obj.save_pkcs1().decode('utf-8')
        self.private_key = self.private_key_obj.save_pkcs1().decode('utf-8')
        
        # Serialize public key to string
        self.public_key_str = self.public_key_obj.save_pkcs1().decode('utf-8')
        
        # Generate the address from the public key
        self.address = self.generate_address()

        self.balance = 1000

    def __str__(self):
        return f"Wallet(public_key={self.public_key}, address={self.address}, private_key={self.private_key}, balance={self.balance})"
    
    def generate_address(self):
        """
        Generate an address from the public key.
        """
        # Hash the public key using SHA-256
        hashed_public_key = hashlib.sha256(self.public_key.encode()).digest()
        
        # Apply RIPEMD-160 hash function to the hashed public key
        ripemd160_hash = hashlib.new('ripemd160')
        ripemd160_hash.update(hashed_public_key)
        hashed_public_key_ripe = ripemd160_hash.digest()
        
        # Encode the hashed public key using Base58Check encoding
        address = base58.b58encode(hashed_public_key_ripe)
        
        return address.decode('utf-8')
    
    def generate_signature(self, sender_public_key, recipient_public_key, amount):
        """
        Generates a signature for the transaction data using RSA encryption.

        :param transaction_data: The transaction data to be signed.
        :return: The generated signature.
        """
        # Generate the transaction data string
        transaction_data_str = self.transaction_to_string(sender_public_key, recipient_public_key, amount)
        
        # Sign the transaction data with the private key
        signature = rsa.sign(transaction_data_str.encode(), self.private_key_obj, 'SHA-256')
        
        return signature
    
    def sign_transaction(self, sender_public_key, recipient_public_key, amount):
        """
        Sign a transaction with the wallet's private key
        """
        transaction = {
            'sender_public_key': sender_public_key,
            'recipient_public_key': recipient_public_key,
            'amount': amount,
        }

        # Generate the transaction data string
        # transaction_data = self.transaction_to_string(sender_public_key, recipient_public_key, amount)
        
        # Generate the signature
        signature = self.generate_signature(sender_public_key, recipient_public_key, amount)
        
        # Encode the signature to base64
        encoded_signature = base64.b64encode(signature).decode()
        
        # Add the signature to the transaction dictionary
        transaction['signature'] = encoded_signature

        return encoded_signature

    def transaction_to_string(self, sender_public_key, recipient_public_key, amount):
        """
        Convert transaction data to a string for signing/verification
        """
        return f"{sender_public_key}{recipient_public_key}{amount}"
    
class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.wallets = {}  # Map wallet addresses to wallet objects
        self.wallet_transactions = {}  # Wallet transaction index

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender_address, recipient_address, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender_address: Public key of the Sender
        :param recipient_address: Public key of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        # Create a new transaction
        transaction = {
            'txID': str(uuid.uuid4()),  # Generate a unique transaction txID
            'amount': amount,
            'sender': sender_address,
            'recipient': recipient_address
        }

        sender_wallet = self.wallets.get(sender_address)
        recipient_wallet = self.wallets.get(recipient_address)

        # Update wallet transaction index
        if sender_address in self.wallet_transactions:
            self.wallet_transactions[sender_address].append(transaction['txID'])
        else:
            self.wallet_transactions[sender_address] = [transaction['txID']]

        print(self.wallets.get(sender_address), "SENDERS WALLET")
        print(self.wallets.get(recipient_address)," RECIPIENT WALLET")
        if sender_wallet:
            result = sender_wallet.sign_transaction(sender_wallet.public_key, recipient_wallet.public_key, amount)  # Sign the transaction
            transaction['signature'] = result
        else:
            print("Sender's wallet not found.")

        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1
    
    def get_transactions(self, wallet_address):
        """
        Retrieve transactions sent by a specific wallet address
        """
        if wallet_address not in self.wallet_transactions:
            return []
        print("Transactions ", self.wallet_transactions[wallet_address])
        transactions = []
        for txID in self.wallet_transactions[wallet_address]:
            for block in self.chain:
                for transaction in block['transactions']:
                    if transaction['txID'] == txID:
                        transactions.append(transaction)
        return transactions
    
    def get_transaction_by_id(self, transaction_id):
        """
        Retrieve a transaction by its ID from the blockchain

        :param transaction_id: ID of the transaction to retrieve
        :return: The transaction if found, None otherwise
        """
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['txID'] == transaction_id:
                    return transaction
        return None
    
    def verify_transaction(self, transaction):
        try:
            # Retrieve sender's address from the transaction
            sender_address = transaction['sender']
            recipient_address = transaction['recipient']
            
            # Retrieve the sender's wallet from the wallets dictionary using the sender's address
            sender_wallet = self.wallets.get(sender_address)
            recipient_wallet = self.wallets.get(recipient_address)

            if sender_wallet:
                # Get the RSA public key object from the sender's wallet
                public_key_obj = rsa.PublicKey.load_pkcs1(sender_wallet.public_key.encode())
                
                # Decode the base64-encoded signature string to bytes
                signature = base64.b64decode(transaction['signature'])
                
                # Encode the transaction string to bytes using UTF-8 encoding
                transaction_string = sender_wallet.transaction_to_string(sender_wallet.public_key, recipient_wallet.public_key, transaction['amount']).encode('utf-8')
                
                # Verify the signature of the transaction using the public key object
                return rsa.verify(transaction_string, signature, public_key_obj)
            else:
                print("Sender's wallet not found.")
                return False
        except KeyError as e:
            print("KeyError:", e)
            return False
        except base64.binascii.Error as e:
            print("Base64 decoding error:", e)
            return False
        except rsa.pkcs1.VerificationError as e:
            print("Verification error:", e)
            return False
        
    def create_wallet(self):
        """
        Create a new wallet and store it in the wallets dictionary
        """
        wallet = Wallet()  # Create a new Wallet object
        self.wallets[wallet.address] = wallet  # Store the Wallet object using its public key
        return wallet
    @property
    def last_block(self):
        return self.chain[-1]
    @property
    def all_wallets(self):
        return self.wallets
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"



def create_app():
    """
    Create a Flask app instance
    """
    # Load environment variables from .env file
    load_dotenv()


    app = Flask(__name__)
    app.logger_name = "itesa-log"
    logging.basicConfig(level=logging.INFO)
    CORS(app, resources={r"/*": {"origins": os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000, http://172.17.0.2:5000")}})
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            # Create a response object with appropriate headers
            response = jsonify()
            response.headers['Access-Control-Allow-Origin'] = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000", "http://172.17.0.2:5000/")
            response.headers['Access-Control-Allow-Methods'] = os.environ.get("ALLOWED_HTTP_METHODS", "GET")
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

    return app

def create_blockchain():
    """
    Create an instance of the Blockchain class
    """
    return Blockchain()