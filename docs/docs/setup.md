---
sidebar_position: 2
---

# Setup for production

## Prepare the environment
In order to run an ACME responder, you will need:
* A Linux appliance with the 443 open
* Access to the port 80 of the clients
* A reverse proxy with a valid TLS certificate

## Prepare the storage
In order to use ACMEResponder, you must first create a directory to store the CA certificate and the accounts public keys:

```bash
mkdir storage
```

## Prepare the certification authority
You also (obviously) need a certification authority to sign the issued certificates. It is up to you to obtain a valid Certificate Authority.

However, for testing purpose, you can also create a self-signed certificate :

```bash
# Create a CA private key
openssl genrsa -out storage/ca-privkey.pem 4096

# Create a CA signing key
openssl req -new -key storage/ca-privkey.pem -x509 -days 1000 -out storage/ca-pubkey.pem -subj "/C=FR/ST=Loire/L=StEtienne/O=Global Security/OU=IT Department/CN=example.com"
```

:::danger

Without a certificate issued by a certification authority and authorized to sign certicate (`IsCA` constraint set to true), the certificate issued by ACMEREsponder will by default not be recognized by the TLS endpoints softwares (browsers, CLI utilities...)

However, you can still use your self-signed certification authority on your own devices by installing them on your truststores.

:::


## Using Docker
The easiest way to install ACMEResponder is to use our Docker image. You can run it using the following command:

```bash
docker run --rm -v $(pwd)/storage:/storage -p 80:80 pierre42100/acme-responder
```

## Install it from sources
You can also install ACMEResponder from source. In order to do so:

1. You must first clone the source code of the repository:

```bash
git clone https://github.com/pierre42100/ACMEresponder
cd ACMEresponder
```


3. Create a Python environment:

```bash
python3 -m venv venv
```


3. Switch the shell to the created environment:

```bash
source venv/bin/activate
```


4. Setup dependencies

```bash
pip install -r requirements.txt
```

5. You should then be ready to run  the server:

```bash
STORAGE_PATH=/path/to/storage uvicorn src.server:app --host 0.0.0.0 --port 80
```

## Configuration
Some aspects of ACMEResponder can be customized. See the [Configuration](./config) section to learn more.