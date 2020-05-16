# -*- coding: utf-8 -*-
import socket
import re


def check_email(email):
    """Check if email is correctly formatted

    Args:
        email (str): 
    Returns:
        True of False
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    return False


def check_ip(addr):
    """Check if ip address is correctly formatted

    Args:
        addr (str): 
    Returns:
        True of False
    """
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False


def perform_full_check(data):
    """Perform full data check

    Args:
        data (dict):
    Returns:
        A dictionary, in which for each key is the
        key in data and value is either True if data
        has been checked and found to be valid, False if
        the check returns negative and None if no check
        has been performed.
    """
    check_result = {k: None for k in data.keys()}
    # check email:
    check_result["email"] = check_email(data["email"])
    # check ip
    check_result["ip_address"] = check_ip(data["ip_address"])
    return check_result
