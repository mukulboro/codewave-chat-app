import base64
import qrcode
import urllib.parse
from io import BytesIO
import hmac
import hashlib
import math
import time

TIME_PERIOD_SECONDS = 30 # 30s default in Google Authenticator

"""
This file contains utility functions to generate a token and QR code to be used with authenticator apps
Also contains fucntions to generate valid totp to be checked against user input
"""

def generate_qr(username:str):
    key = username.encode("utf-8") # The user's email is the key for the hash
    token = base64.b32encode(key)
    token = token.decode("utf-8") # Make token human readable
    safe_username = urllib.parse.quote(username) # Making email URL safe
    qr_string = f"otpauth://totp/{safe_username}?secret={token}&issuer=ChatAnon&algorithm=SHA1&digits=6&&period={TIME_PERIOD_SECONDS}"
    # ^ Creating URL with proper format to be recognized by authenticator apps
    qr_code = qrcode.make(qr_string)
    stream = BytesIO()
    qr_code.save(stream)
    return base64.b64encode(stream.getvalue()).decode('utf-8'), token
    # ^ Image is converted to base64 so it can be directly rendered in frontend

def generate_totp(username:str):
    # Following standards to generate OTP
    key = username.encode("utf-8")
    t = math.floor(time.time() // TIME_PERIOD_SECONDS)
    hmac_object = hmac.new(key, t.to_bytes(length=8, byteorder="big"), hashlib.sha1)
    hmac_sha1 = hmac_object.hexdigest()
    offset = int(hmac_sha1[-1], 16)
    binary = int(hmac_sha1[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
    # ^ Binary Magic 🧙
    totp = str(binary)[-6:]
    return int(totp)