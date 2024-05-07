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

# Introduction <a name="introduction"></a>

The `blockchain.py` module implements a simple blockchain and wallet system in Python. It includes classes for managing transactions, blocks, wallets, and a blockchain itself.

# Installation <a name="installation"></a>

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
# Usage <a name="usage"></a>

## Creating a Blockchain <a name="creating-a-blockchain"></a>

To create a new instance of the blockchain, use the `create_blockchain()` function:

```python
blockchain = create_blockchain()
```

## Managing Wallets <a name="creating-a-blockchain"></a>

The Wallet class allows you to generate new wallet addresses and manage their balances. Here's an example of creating a new wallet:

```python
wallet = Wallet()
```

## Adding Transactions <a name="adding-transactions"></a>

You can add transactions to the blockchain using the `new_transaction()` method of the `Blockchain` class:

```python
blockchain.new_transaction(sender_address, recipient_address, amount)
```

## Verifying Transactions <a name="verifying-transactions"></a>

Transactions can be verified using the verify_transaction() method of the Blockchain class:

```python
verification_result = blockchain.verify_transaction(transaction)
```

## How to execute the `Dockerfile` <a name="docker"></a>

Run the following commands and thats all:

```
docker build -t blockchain .
docker run --rm -p 81:5000 blockchain
```

# API <a name="api"></a>

The REST API to the example app is described below.

## Demo <a name="demo"></a>

### Request

`GET /demo`

    curl -i -H 'Accept: application/json' http://localhost:3000/demo/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
    "message": "Demo completed",
    "transactions": 5,
    "wallet1": "wallet1.address",
    "wallet2": "wallet2.address"
    }


## Mine <a name="mine"></a>

### Request

`GET /mine`

    curl -i -H 'Accept: application/json' http://localhost:3000/mine/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
    "index": 2,
    "message": "New Block Forged",
    "previous_hash": "string",
    "proof": 666,
    "transactions": 
        [
            {
                "amount": 800,
                "recipient": "zfccSmzNkkTsePwQhm3nC1Hffqh",
                "sender": "2SuKMMXGTSbGFaZoZNtuhaueJttK",
                "signature": "lK9ggrdKLvsHgsOtPlkVhZ4suKe/B9ecGwfJRHo+E1M0Y/t2kGjHkaC9VefW+Bu8+Zb9711dwnOE0RW0m7Ft3w==",
                "txID": "b82eb028-cd24-41c1-b932-777a3c293ea2"
            },
        ]
    }

## Chain <a name="chain"></a>

`GET /chain`

    curl -i -H 'Accept: application/json' http://localhost:3000/chain/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
    "chain": 
        [
            {
                "index": 1,
                "previous_hash": "1",
                "proof": 100,
                "timestamp": 1714945098.908583,
                "transactions": [
                    {
                    "amount": 5,
                    "recipient": "39B8a1v5SmPKHZvVQ3TyuBzYSrfd",
                    "sender": "3TdFTtCchR3dyVpUDVL6puTxnK6t",
                    "txID": "3924fab6-52cd-4443-9775-131e8b649750"
                    },
                    {
                        "amount": 5,
                        "recipient": "39B8a1v5SmPKHZvVQ3TyuBzYSrfd",
                        "sender": "3TdFTtCchR3dyVpUDVL6puTxnK6t",
                        "txID": "65a506a4-a934-4b43-8fe8-497285ff7384"
                    },
                ]
            },
        ]
    }


## New Transactions <a name="transactions-new"></a>

`POST /transactions/new`

    curl -X POST -H "Content-Type: application/json" -d '{"sender": "my address", "recipient": "someone else's address", "amount": 5}' http://localhost:3000/transactions/new

### Response

    HTTP/1.1 201 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 201 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        'message': 'Transaction will be added to Block 4'
    }


## Verify Transaction <a name="transactions-verify"></a>

`POST /transactions/verify-transaction`

    curl -X POST -H "Content-Type: application/json" -d '{"amount": 5000, "recipient": "41G6q8TnADqshumPCBFoShaaNcAG", "sender": "uu7DbYLMjcxrVDkQYuWBSQTkNCu", "signature": "I5tpRiCMFAEqXRaPI5f8v16eNuC5rhFMPUg55R4ckQ5kmftI9yaT8AL357FDTkqf1NQSiJYk2Ke5c9P4/Lf1cQ=="}' http://localhost:3000/transactions/verify-transaction


### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        'message': 'Transaction signature is valid.'
    }


## Get all transactions by address <a name="transactions-address"></a>

`GET /transactions/verify-transaction`

    curl -X GET -H "Content-Type: application/json" -d '{"address": "string"}' http://localhost:3000/transactions/address


### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        'message': 'Transaction found!.',
        'transactions': [
            {
                "amount": 5,
                "recipient": "39B8a1v5SmPKHZvVQ3TyuBzYSrfd",
                "sender": "3TdFTtCchR3dyVpUDVL6puTxnK6t",
                "txID": "3924fab6-52cd-4443-9775-131e8b649750"
            },
            {
                "amount": 5,
                "recipient": "39B8a1v5SmPKHZvVQ3TyuBzYSrfd",
                "sender": "3TdFTtCchR3dyVpUDVL6puTxnK6t",
                "txID": "65a506a4-a934-4b43-8fe8-497285ff7384"
            },
        ]
    }

## Get transaction by id <a name="transactions-id"></a>

`GET /transactions/id`

    curl -X GET -H "Content-Type: application/json" -d '{"txID": "string"}' http://localhost:3000/transactions/id


### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        'message': 'Transaction found!.',
        'transactions': [
            {
                "amount": 5,
                "recipient": "39B8a1v5SmPKHZvVQ3TyuBzYSrfd",
                "sender": "3TdFTtCchR3dyVpUDVL6puTxnK6t",
                "txID": "3924fab6-52cd-4443-9775-131e8b649750"
            }
        ]
    }

##### Seed <a name="transactions-seed"></a>

`POST /transactions/seed`

    curl -X POST -H "Content-Type: application/json" -d '{"amount": 5000, "recipient": "41G6q8TnADqshumPCBFoShaaNcAG", "sender": "uu7DbYLMjcxrVDkQYuWBSQTkNCu", "rounds": 5}' http://localhost:3000/transactions/seed


### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        "message": "5 transactions created successfully"
    }

## Create wallet <a name="create-wallet"></a>

`GET /create-wallet`

    curl -X GET -H "Content-Type: application/json" http://localhost:3000/create-wallet


### Response (Private keys SHOULD NOT be stored in anyway anywhere)

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        "address": "2mT7XqJM2ACQdZsJAgCthi4YcuA3",
        "balance": 1000,
        "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIBPAIBAAJBAKrHJtLglRimQi2urJFBwaTxdX3N+5wL8kdbmB+AnIv96tIyVXqT\nB5Kl1XkhUbjDBRpM1GEPmf63etI8m2+cNj0CAwEAAQJAQBkbk07D50qP0EGdd6+s\nlNIj/SIQ7BL3zpysTjahRn6KLckhl+oc1UdhTqmsJv60FBEDqfMDj26HeWX1xHzB\nKQIjALdfIr4/cmfym9LYVc/tL9j+d1BAZoynX38rkbhmG3MW3s8CHwDuaxYAbmt6\n67BVOB45StdWeD9zOUlNb6sxXWNBvTMCIlgMwZUSyC+rqjETGhlubfRHNCl/0v4k\n/FEHLcCanwGjcLcCHwDC0kyjQ5eeVVO8/2NrK6X1KcOncytcFKEOcKJ4CJMCIiLG\n3x34Ln6X9hTeL0KmaqOybil2FYHCLOB11/POGSOZ4T8=\n-----END RSA PRIVATE KEY-----\n",
        "public_key": "-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCqxybS4JUYpkItrqyRQcGk8XV9zfucC/JHW5gfgJyL/erSMlV6kweSpdV5\nIVG4wwUaTNRhD5n+t3rSPJtvnDY9AgMBAAE=\n-----END RSA PUBLIC KEY-----\n"
    }

## Wallets <a name="Wallets"></a>

`GET /wallets`

    curl -X GET -H "Content-Type: application/json" http://localhost:3000/wallets


### Response (Private keys SHOULD NOT be stored in anyway anywhere)

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
        "wallets": [
            {
                "address": "2mT7XqJM2ACQdZsJAgCthi4YcuA3",
                "balance": 1000,
                "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIBPAIBAAJBAKrHJtLglRimQi2urJFBwaTxdX3N+5wL8kdbmB+AnIv96tIyVXqT\nB5Kl1XkhUbjDBRpM1GEPmf63etI8m2+cNj0CAwEAAQJAQBkbk07D50qP0EGdd6+s\nlNIj/SIQ7BL3zpysTjahRn6KLckhl+oc1UdhTqmsJv60FBEDqfMDj26HeWX1xHzB\nKQIjALdfIr4/cmfym9LYVc/tL9j+d1BAZoynX38rkbhmG3MW3s8CHwDuaxYAbmt6\n67BVOB45StdWeD9zOUlNb6sxXWNBvTMCIlgMwZUSyC+rqjETGhlubfRHNCl/0v4k\n/FEHLcCanwGjcLcCHwDC0kyjQ5eeVVO8/2NrK6X1KcOncytcFKEOcKJ4CJMCIiLG\n3x34Ln6X9hTeL0KmaqOybil2FYHCLOB11/POGSOZ4T8=\n-----END RSA PRIVATE KEY-----\n",
                "public_key": "-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCqxybS4JUYpkItrqyRQcGk8XV9zfucC/JHW5gfgJyL/erSMlV6kweSpdV5\nIVG4wwUaTNRhD5n+t3rSPJtvnDY9AgMBAAE=\n-----END RSA PUBLIC KEY-----\n"
            },
                        {
                "address": "2mT7XqJM2ACQdZsJAgCthi4YcuA3",
                "balance": 1000,
                "private_key": "-----BEGIN RSA PRIVATE KEY-----\nMIIBPAIBAAJBAKrHJtLglRimQi2urJFBwaTxdX3N+5wL8kdbmB+AnIv96tIyVXqT\nB5Kl1XkhUbjDBRpM1GEPmf63etI8m2+cNj0CAwEAAQJAQBkbk07D50qP0EGdd6+s\nlNIj/SIQ7BL3zpysTjahRn6KLckhl+oc1UdhTqmsJv60FBEDqfMDj26HeWX1xHzB\nKQIjALdfIr4/cmfym9LYVc/tL9j+d1BAZoynX38rkbhmG3MW3s8CHwDuaxYAbmt6\n67BVOB45StdWeD9zOUlNb6sxXWNBvTMCIlgMwZUSyC+rqjETGhlubfRHNCl/0v4k\n/FEHLcCanwGjcLcCHwDC0kyjQ5eeVVO8/2NrK6X1KcOncytcFKEOcKJ4CJMCIiLG\n3x34Ln6X9hTeL0KmaqOybil2FYHCLOB11/POGSOZ4T8=\n-----END RSA PRIVATE KEY-----\n",
                "public_key": "-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCqxybS4JUYpkItrqyRQcGk8XV9zfucC/JHW5gfgJyL/erSMlV6kweSpdV5\nIVG4wwUaTNRhD5n+t3rSPJtvnDY9AgMBAAE=\n-----END RSA PUBLIC KEY-----\n"
            },
        ]
    }
















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

