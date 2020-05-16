# -*- coding: utf-8 -*-
import data_cleaner as cleaner


def test_clean_country():
    assert cleaner.clean_country("france") == "France"
    assert cleaner.clean_country("") == ""


def test_clean_firstname():
    assert cleaner.clean_firstname("mike") == "Mike"
    assert cleaner.clean_firstname("") == ""


def test_clean_lastname():
    assert cleaner.clean_lastname("liu") == "Liu"
    assert cleaner.clean_lastname("") == ""


def test_clean_date():
    assert cleaner.clean_datetime("12/01/2018") == "2018-12-01"
    assert cleaner.clean_datetime("") == ""


def test_full_clean():
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
        "id": 1,
        "first_name": "Barthel",
        "last_name": "Kittel",
        "email": "bkittel0@printfriendly.com",
        "gender": "Male",
        "ip_address": "130.187.82.195",
        "date": "2018-06-05",
        "country": "France"
    }
    assert expected == cleaner.perform_full_clean(data)