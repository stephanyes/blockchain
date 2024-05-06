# Blockchain Implementation

This project is based on the source code found in [Building a Blockchain](https://github.com/dvf/blockchain).

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
    - [Creating a Blockchain](#creating-a-blockchain)
    - [Managing Wallets](#managing-wallets)
    - [Adding Transactions](#adding-transactions)
    - [Verifying Transactions](#verifying-transactions)
4. [Docker](#docker)
4. [API](#api)
    - [/demo](#demo)
    - [/mine](#mine)
    - [/chain](#chain)
    - [/transactions/new](#transactions-new)
    - [/transactions/verify-transaction](#transactions-verify-transaction)
    - [/transactions/address](#transactions-address)
    - [/transactions/id](#transactions-id)
    - [/transactions/seed](#transactions-seed)
    - [/nodes/register](#nodes-register)
    - [/nodes/resolve](#nodes-resolve)
    - [/create-wallet](#create-wallet)
    - [/wallets](#wallets)

---

1. ##### Introduction <a name="introduction"></a>

The `blockchain.py` module implements a simple blockchain and wallet system in Python. It includes classes for managing transactions, blocks, wallets, and a blockchain itself.

2. ##### Installation <a name="installation"></a>

To use the `blockchain.py` module, simply include it in your Python project directory. After completing the setup in `blockchain.py`, you'll also need to create a Dockerfile in the `/src` directory and you also need a `requirements.txt` so we can install the dependencies needed. Here's how the Dockerfile should look:

```Dockerfile
FROM python:3.6-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Add source code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "main.py", "--port", "5000"]
```
3. ##### Usage <a name="usage"></a>

##### Creating a Blockchain <a name="creating-a-blockchain"></a>

To create a new instance of the blockchain, use the `create_blockchain()` function:

```python
blockchain = create_blockchain()
```

##### Managing Wallets <a name="creating-a-blockchain"></a>

The Wallet class allows you to generate new wallet addresses and manage their balances. Here's an example of creating a new wallet:

```python
wallet = Wallet()
```

##### Adding Transactions <a name="adding-transactions"></a>

You can add transactions to the blockchain using the `new_transaction()` method of the `Blockchain` class:

```python
blockchain.new_transaction(sender_address, recipient_address, amount)
```

##### Verifying Transactions <a name="verifying-transactions"></a>

Transactions can be verified using the verify_transaction() method of the Blockchain class:

```python
verification_result = blockchain.verify_transaction(transaction)
```

4. ##### How to execute the `Dockerfile` <a name="docker"></a>

Run the following commands and thats all:

```
docker build -t blockchain .
docker run --rm -p 81:5000 blockchain
```

5. ##### API <a name="api"></a>

##### Demo <a name="demo"></a>

The `/demo` route generates a demo scenario by creating two wallets, performing transactions between them, and then returning a response with information about the demo. It creates two wallets using the create_wallet() method, generates 5 transactions between them, and logs the wallet addresses and completion of the demo. If an error occurs during the process, it logs the error and returns an error response with a status code of 500.

##### Mine <a name="mine"></a>

This route `/mine` handles the mining process to generate a new block in the blockchain. It starts by retrieving the last block from the blockchain, calculating the proof of work, and generating the hash of the previous block. Then, it creates a new transaction for mining reward, adds this transaction to the new block, and adds the block to the blockchain. Finally, it constructs a response containing information about the new block, including its index, transactions, proof, previous hash, and serialized wallet information. If an error occurs during the mining process, it logs the error and returns a JSON response with a corresponding error message and status code.

##### Chain <a name="chain"></a>

This route `/chain` returns the full blockchain and its length as a JSON response. It handles HTTP GET requests and constructs a response containing the blockchain and its length. The blockchain is represented as a list of blocks, and the length indicates the number of blocks in the blockchain. The response is returned with a status code of 200, indicating a successful request.


##### New Transactions <a name="transactions-new"></a>

This route `/transactions/new` handles HTTP POST requests to add a new transaction to the blockchain. It expects JSON data containing the sender's public key, recipient's public key, and the transaction amount. If any of these required fields are missing in the POST request, it returns a 'Missing values' message with a status code of 400.

After extracting the required data from the JSON payload, it creates a new transaction using the `new_transaction` method of the blockchain. The method returns the index of the block where the transaction will be added. Then, it constructs a response JSON containing a message indicating the block where the transaction will be added and returns it with a status code of 201, indicating successful creation.

##### Verify Transaction <a name="transactions-verify"></a>

This endpoint `/transactions/verify-transaction verifies` the signature of a transaction using the `sender`'s public key. It expects a JSON object in the request body containing the `sender` 's address, `recipient`'s address, `amount`, and `signature`. It then validates the presence of these parameters and retrieves the sender's public key from the blockchain. Finally, it verifies the transaction signature and returns a message indicating whether the signature is valid or invalid. If any error occurs during the process, it returns a 500 error with the error message.

##### Get all transactions by address <a name="transactions-address"></a>

This endpoint `/transactions/address` retrieves all transactions associated with a specific `address`. It expects a JSON object in the request body containing the `address`. It then retrieves the transactions from the blockchain using the provided `address` and returns them as a JSON response. If no transactions are found, it returns a message indicating that no transactions were found. If any error occurs during the process, it returns a 500 error with the error message.

##### Get transaction by id <a name="transactions-id"></a>

This endpoint /transactions/id retrieves a transaction by its ID. It expects a JSON object in the request body containing the transaction ID (txID). It then retrieves the transaction from the blockchain using the provided ID and returns it as a JSON response. If no transaction is found, it returns a message indicating that no transaction was found. If any error occurs during the process, it returns a 500 error with the error message.

##### Seed <a name="transactions-seed"></a>

This endpoint `/transactions/seed` creates a specified number of transactions. It expects JSON data in the request body with the fields: `sender`, `recipient`, `amount`, and `rounds`. It validates the input data, ensuring that all required fields are present and that `amount` and `rounds` are positive integers. If the input is valid, it creates the specified number of transactions and returns a success message. If any errors occur during the process, it returns an appropriate error message.

##### Create wallet <a name="create-wallet"></a>

This endpoint `/create-wallet` generates a new wallet and returns its details including the wallet `address`, `public_key`, `private_key`, and `balance`. If the wallet creation is successful, it returns the wallet details along with a status code of 200. If an error occurs during the process, it returns an error message along with a status code of 500.

##### Wallets <a name="Wallets"></a>

This endpoint `/wallets` retrieves all wallets stored in the blockchain and returns them as JSON. If successful, it returns the wallets along with a status code of 200. If an error occurs during the process, it returns an error message along with a status code of 500.

















<!-- # Are you looking for the source code for my book?

Please find it here: https://github.com/dvf/blockchain-book

The book is available on Amazon: https://www.amazon.com/Learn-Blockchain-Building-Understanding-Cryptocurrencies/dp/1484251709

# Learn Blockchains by Building One

[![Build Status](https://travis-ci.org/dvf/blockchain.svg?branch=master)](https://travis-ci.org/dvf/blockchain)

This is the source code for my post on [Building a Blockchain](https://github.com/dvf/blockchain). 

## Installation

1. Make sure [Python 3.6+](https://www.python.org/downloads/) is installed. 
2. Install [pipenv](https://github.com/kennethreitz/pipenv). 

```
$ pip install pipenv 
```
3. Install requirements  
```
$ pipenv install 
``` 

4. Run the server:
    * `$ pipenv run python blockchain.py` 
    * `$ pipenv run python blockchain.py -p 5001`
    * `$ pipenv run python blockchain.py --port 5002`
    
## Docker

Another option for running this blockchain program is to use Docker.  Follow the instructions below to create a local Docker container:

1. Clone this repository
2. Build the docker container

```
$ docker build -t blockchain .
```

3. Run the container

```
$ docker run --rm -p 80:5000 blockchain
```

4. To add more instances, vary the public port number before the colon:

```
$ docker run --rm -p 81:5000 blockchain
$ docker run --rm -p 82:5000 blockchain
$ docker run --rm -p 83:5000 blockchain
```

## Installation (C# Implementation)

1. Install a free copy of Visual Studio IDE (Community Edition):
https://www.visualstudio.com/vs/

2. Once installed, open the solution file (BlockChain.sln) using the File > Open > Project/Solution menu options within Visual Studio.

3. From within the "Solution Explorer", right click the BlockChain.Console project and select the "Set As Startup Project" option.

4. Click the "Start" button, or hit F5 to run. The program executes in a console window, and is controlled via HTTP with the same commands as the Python version.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. -->

