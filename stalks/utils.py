#!.env/bin/python
from datetime import datetime, timedelta
from lxml import etree as ET


def convert_datetime_object(o):
    """
    Coerce input to datetime string
    :param datetime
    :return datetime <str>
    """
    if isinstance(o, datetime):
        return o.__str__()


def convert_utc_to_local(utcdate_obj):
    """ Convert UTC Time to Local Time
    :param utcdate
    :return utcdate + offset
    """
    nowtimestamp = time.time()
    offset = datetime.fromtimestamp(nowtimestamp) - datetime.utcfromtimestamp(nowtimestamp)
    return utcdate_obj + offset


def parse_xml(doc):
    """
    Parse the XML response and return a structured XML tree
    :param doc
    :return lxml tree
    """
    try:
        f = ET.fromstring(doc)
    except TypeError as err:
        print(str(err))

    return f
