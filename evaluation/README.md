# Evaluation
This directory contain data used to test our tool with Certbot.

See [our docs to learn more](../docs/docs/evaluation.md).

REQUESTS_CA_BUNDLE=/myca.crt certbot certonly -n  --webroot -w /storage -d client --server https://secure/directory --agree-tos --email mymail@corp.com