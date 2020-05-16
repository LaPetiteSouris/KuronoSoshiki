# -*- coding: utf-8 -*-
import data_quality_controller as controller


def test_check_email():
    assert controller.check_email("france@gmail.com") is True
    assert controller.check_email("totododo") is False


def test_check_ip():
    assert controller.check_ip("130.187.82.195") is True
    assert controller.check_ip("130.xx.82.195") is False


def test_full_check():
    data = {
        "id": 1,
        "first_name": "barthel",
        "last_name": "kittel",
        "email": "bkittel0@printfriendly.com",
        "gender": "Male",
        "ip_address": "130.187.82.195",
        "date": "06/05/2018",
        "country": "france"
    }
    expected = {
        "id": None,
        "first_name": None,
        "last_name": None,
        "email": True,
        "gender": None,
        "ip_address": True,
        "date": None,
        "country": None
    }
    assert expected == controller.perform_full_check(data)