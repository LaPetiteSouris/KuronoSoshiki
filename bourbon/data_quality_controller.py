# -*- coding: utf-8 -*-
import socket
import re


def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    return False


def check_ip(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False


def perform_full_check(data):
    check_result = {k: None for k in data.keys()}
    # check email:
    check_result["email"] = check_email(data["email"])
    # check ip
    check_result["ip_address"] = check_ip(data["ip_address"])
    return check_result
