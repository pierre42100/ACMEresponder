---
sidebar_position: 4
---

# For developers

## Pre-requisites
* Python 3.9 
* Pip (Python package manager)
* Python-VENV (Python virtual environment management)
* OpenSSL CLI

## Setup a development environment
1. Create a Python environment:

```bash
python3 -m venv venv
```


2. Switch the shell to the created environment:

```bash
source venv/bin/activate
```


3. Setup dependencies

```bash
pip install -r requirements.txt
```

4. Generate self-signed certification authority

```bash
# Generate storage
mkdir storage

# Create a CA private key
openssl genrsa -out storage/ca-privkey.pem 4096

# Create a CA signing key
```
openssl req -new -key storage/ca-privkey.pem -x509 -days 1000 -out storage/ca-pubkey.pem -subj "/C=FR/ST=Loire/L=StEtienne/O=Global Security/OU=IT Department/CN=example.com"

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
Check for coding style issues:
```bash
pylint /*
```

Fix all coding style issues at once using `black`:
```bash
black src/* test/* 
```



