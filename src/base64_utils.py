import base64


def safe_base64_encode(un_encoded_data) -> str:
    """
    return ACME-safe base64 encoding of un_encoded_data as a string
    """
    if isinstance(un_encoded_data, str):
        un_encoded_data = un_encoded_data.encode("utf8")
    r = base64.urlsafe_b64encode(un_encoded_data).rstrip(b"=")
    return r.decode("utf8")


def fix_b64_padding(s):
    """
    Fix Base64 padding potential issue
    """
    if len(s) % 4 != 0:
        s += "==="[0 : 4 - (len(s) % 4)]
    return s


def safe_base64_decode(s: str) -> bytes:
    """
    Decode base64 encoded data sent to ACME provider
    """
    return base64.urlsafe_b64decode(fix_b64_padding(s))
