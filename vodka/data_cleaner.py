# -*- coding: utf-8 -*-
import copy
import datetime


def clean_country(country):
    # start with capial letter
    return country.title()


def clean_firstname(name):
    # start with capial letter
    return name.title()


def clean_lastname(name):
    # start with capial letter
    return name.title()


def clean_datetime(dt):
    try:
        north_amercia_dt = datetime.datetime.strptime(
            dt, '%m/%d/%Y').strftime('%Y-%m-%d')
        return str(north_amercia_dt)
    except ValueError:
        return ""


def _dict_clean(d):
    result = {}
    for key, value in d.items():
        if value is None:
            value = 'default'
        result[key] = value
    return result


def perform_full_clean(data):
    cleaned_data = copy.deepcopy(data)
    cleaned_data = _dict_clean(cleaned_data)
    # Country
    cleaned_data["country"] = clean_country(cleaned_data.get("country", ""))
    # Firstname
    cleaned_data["first_name"] = clean_firstname(
        cleaned_data.get("first_name", ""))
    # Lastname
    cleaned_data["last_name"] = clean_lastname(cleaned_data.get("last_name", ""))
    # date
    cleaned_data["date"] = clean_datetime(cleaned_data.get("date", ""))
    return cleaned_data
