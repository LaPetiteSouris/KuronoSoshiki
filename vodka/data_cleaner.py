# -*- coding: utf-8 -*-
import copy
import datetime


def clean_country(country):
    """Clean country data

    Args:
        country (str): 
    Returns:
        country starts with capital letter
    """
    # start with capial letter
    return country.title()


def clean_firstname(name):
    """Clean firstname

    Args:
        name (str): 
    Returns:
        firstname starts with capital letter
    """
    # start with capial letter
    return name.title()


def clean_lastname(name):
    """Clean lastname

    Args:
        name (str): 
    Returns:
        lastname starts with capital letter
    """
    # start with capial letter
    return name.title()


def clean_datetime(dt):
    """Change datetime format from European
    m/d/Y to US Y-m-d format

    Args:
        dt (str): datetime string in m/d/Y format
    Returns:
        datetime string in Y-m-d format
    """
    try:
        north_amercia_dt = datetime.datetime.strptime(
            dt, '%m/%d/%Y').strftime('%Y-%m-%d')
        return str(north_amercia_dt)
    except ValueError:
        return ""


def _dict_clean(d):
    """ Replace None with empty string in dict
    Args:
        d (dict): dictionary
    Returns:
        dict
    """
    result = {}
    for key, value in d.items():
        if value is None:
            value = ''
        result[key] = value
    return result


def perform_full_clean(data):
    """Perform a full clean on all fields of the data

    Args:
        data (dict): 
    Returns:
        cleaned data
    """
    cleaned_data = copy.deepcopy(data)
    cleaned_data = _dict_clean(cleaned_data)
    # Country
    cleaned_data["country"] = clean_country(cleaned_data.get("country", ""))
    # Firstname
    cleaned_data["first_name"] = clean_firstname(
        cleaned_data.get("first_name", ""))
    # Lastname
    cleaned_data["last_name"] = clean_lastname(
        cleaned_data.get("last_name", ""))
    # date
    cleaned_data["date"] = clean_datetime(cleaned_data.get("date", ""))
    return cleaned_data
