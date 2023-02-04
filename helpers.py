import os
import requests
import urllib.parse
import re

from flask import redirect, render_template, request, session
from functools import wraps

# Check user password for letters, numbers, special characters


def valid_password(password: str) -> bool:

    # Check if the password is atleast 8 characters long
    if len(password) < 8:
        return False

    # Check if the password contains letters numbers and characters (atleast 1)

    # 'r'[!@#$%^&*(),.?":{}|<>]': matches any password that contains at least one symbol
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    # 'r'[a-zA-Z]': matches any password that contains at least one letter
    if not re.search(r'[a-zA-Z]', password):
        return False

    # r'[0-9]': matches any password that contains at least one numeric
    if not re.search(r'[0-9]', password):
        return False

    # If the pasword passes all checks, return true
    return True

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Check post for scammers
def scam_catcher(comment: str) -> bool:

    #check if comment contains a phone number
    """""

    Here's a breakdown of the regex:

    ^ - Matches the start of the string
    (?:(?:\+254|0{0,2})) - Matches the Kenyan country code +254, with or without leading zeroes
    (7|01[01]\d|01[12]\d{2}) - Matches either 7 or 0110 or 0111 or 0112 or 0113 or 0114 or 0115
    \d{6} - Matches exactly 6 digits
    $ - Matches the end of the string

    """""
    phone_number_regex = "^(?:(?:\+254|0{0,2}))(7|01[01]\d|01[12]\d{2})\d{6}$"

    match = re.search(phone_number_regex, comment)

    if match:
        return True

    return False
