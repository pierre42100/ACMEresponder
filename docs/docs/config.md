---
sidebar_position: 3
---

# Configuration
Some configuration option can be customized.


## Injection configuration customization
If you are using the Docker image, you can use the `--env` argument when launching the responder to change an option:

```bash
docker run --rm -v $(pwd)/storage:/storage -p 80:80 --env KEY=VALUE pierre42100/acme-responder
```

If you are running the project from sources, you can simply add the arguments at the beginning of the command:

```bash
KEY=VALUE uvicorn src.server:app --host 0.0.0.0 --port 80
```

## Available options

| Key          | Description | Default value |
| ------------ | ----------- | ------------- |
| `DOMAIN_URI` | The domain where the ACME server is available (without a trailing slash) | `http://localhost:8000`|
|`STORAGE_PATH`| Whether the persisted data (CA & account keys) can be found|`storage`|
|`CONTACT_MAIL`|The email where the team should be contacted|`contact@acme.corp`|
|`ORDER_LIFETIME`|The time a client has to fullfill the expectations of an order, in seconds (validate challenges)|`900` (15 minutes)|
|`CERTS_DURATION`|The duration of the issued certificates, in seconds|`2592000` (30 days)|
|`HTTP_CHALLENGE_PORT`|The port of the client on which the server should connect to check HTTP challenges. This value should be changed, appart in very specific business constraints.|`80`|


:::caution
It is recommended to change at least the value of the `DOMAIN_URI` parameter.
:::