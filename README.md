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


4. Run the server

```bash
uvicorn server:app --reload
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
* Nonce are not supported

## Members
* Yanis MAMMAR
* Ziyed MELIZI
* Arthur HOCHE
* Pierre HUBERT