---
sidebar_position: 6
---

# Technical choices

## The programming language: Python
This project was built using the Python programming language.

This language was not really chosen. Indeed, it has imposed by the context this project was lead, during an EPITA "Python for security" course.

However, the simplicity of this programming language made it rather easy to build a working prototype.


## The API framework: FastAPI
FastAPI is a well-known REST framework. Because, at the time of the construction  of this project, it had more than 56k stars and 4.7k forks [on GitHub](https://github.com/tiangolo/fastapi), we can make  the following assertions about this tool:

* It is worth it to spend time using it, otherwise it wouldn't be so popular
* Security researchers have certainly helped to harden the security of its source code.

Moreover, [the documentation of FastAPI](https://fastapi.tiangolo.com/) is well furbished, making it easy to get started with it.


## The ACME protocol test library: sewer 
In order to build our units tests, we needed a ACME-capable library that would act as a client to the ACME protocol. The requirements for such library were the following:

* The library must be able to act as an ACME client, following the RFC 8555 standard
* It must offer an API that allow programmatic calls, with some aspects hookable:
  * The library must allows to perform clear-text exchanges with the ACME backend
  * The library must be hook-able, allowing custom code to handle challenge deployment
* It must be written in Python
* The library must be usable with a free license

The [Sewer](https://github.com/komuw/sewer) library addresses all these requirements.


## Included features
* ✅ [Directory listing](https://www.rfc-editor.org/rfc/rfc8555#section-7.1.1). This is the  entrypoint to all the others features of the protocol. Without it, ACME is not ACME.
* ✅ [Account creation](https://www.rfc-editor.org/rfc/rfc8555#section-7.3). Accounts are required to manage orders.
* ✅ [Orders creation and management](https://www.rfc-editor.org/rfc/rfc8555#section-7.4): Orders are the basis of certificates generation and retrieval
* ✅ [HTTP-based challenge](https://www.rfc-editor.org/rfc/rfc8555#section-8.3) HTTP Challenges are the more common and more secure way to authenticate servers through  ACME
* ❌ [DNS-based challenges](https://www.rfc-editor.org/rfc/rfc8555#section-8.4) DNS based-challenge are quite challenging to test in an automated way. Due to constrained time, we decided not to implement it.
* ❌ [Certificates revocation](https://www.rfc-editor.org/rfc/rfc8555#section-7.6). We made explicitly the choice not to implement certificates revocations because :
  * It would add significant overhead in the management of the orders (the orders would have to be persisted)
  * It is often preferable, especially in controlled environment, to reduce the lifetime of the certificates rather than revoking leaked certificates.
* ❌ [Account key rollover and deactivation](https://www.rfc-editor.org/rfc/rfc8555#section-7.3.5). This feature present an interest only if the revocation itself is implemented, to prevent from unwanted revocation in case of account private key revocation. Because we did not implement revocation, it was not necessary to handle accounts key revocation. 


## The project itself: an ACME implementation
Let's Encrypt is a fantastic technology that we have been using for years to issue new certificates.

We saw this project as an opportunity to discover behind the hood Let's Encrypt handles its magic.