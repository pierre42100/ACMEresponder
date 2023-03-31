# ACME responder

Lightweight but still useful server-side ACME implementation.


## Pre-requisites
* Python 3.9 +
* Pip
* Python-VENV

## Setup dev environment
1. Create an environment:

```bash
python3 -m venv venv
```


2. Switch the shell to the environment:

```bash
source venv/bin/activate
```


3. Setup dependencies

```bash
pip install -r requirements.txt
```

4. Generate self-signe certification authority

```bash
# Generate storage
mkdir storage

# Create a CA private key
openssl genrsa -out storage/ca-privkey.pem 4096

# Create a CA signing key
openssl req -new -key storage/ca-privkey.pem -x509 -days 1000 -out storage/ca-pubkey.pem -subj "/C=FR/ST=Loire/L=StEtienne/O=Global Security/OU=IT Department/CN=example.com"
```

5. Run the server

```bash
uvicorn src.server:app --reload
```

## Unit testing
Simply run the following command:

```bash
pytest
```

## Code formatting
Check for issues:
```bash
pylint server.py
```

Fix coding style issues:
```bash
black server.py 
```

## Limitations
* HTTP-based challenge only are supported
* Account management is limited to accounts creation

## Members
* Yanis MAMMAR
* Ziyed MELIZI
* Arthur HOCHE
* Pierre HUBERT