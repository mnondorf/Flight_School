"""
Module providing utility functions for this project.

These functions are general purpose utilities used by other modules in this project.
Some of these functions were exercises in early course modules and should be copied
over into this file.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Melissa Nondorf
Date: 2/1/23
"""
import csv
import json
from dateutil.parser import parse
import datetime
import pytz


def read_csv(filename):
    """
    Returns the contents read from the CSV file filename.
    
    This function reads the contents of the file filename and returns the contents as
    a 2-dimensional list. Each element of the list is a row, with the first row being
    the header. Cells in each row are all interpreted as strings; it is up to the 
    programmer to interpret this data, since CSV files contain no type information.
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid CSV file
    """
    contents = []
    
    handle = open(filename, 'r')
    wrapper = csv.reader(handle)
    for row in wrapper:
        contents.append(row)
    handle.close()
    return contents


def write_csv(data,filename):
    """
    Writes the given data out as a CSV file filename.
    
    To be a proper CSV file, data must be a 2-dimensional list with the first row 
    containing only strings.  All other rows may be any Python value.  Dates are
    converted using ISO formatting. All other objects are converted to their string
    representation.
    
    Parameter data: The Python value to encode as a CSV file
    Precondition: data is a  2-dimensional list of strings
    
    Parameter filename: The file to read
    Precondition: filename is a string representing a path to a file with extension
    .csv or .CSV.  The file may or may not exist.
    """
    n = 0
    file = open(filename, 'w')
    wrapper = csv.writer(file)
    #wrapper.writerow(['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA','REASON'])
    for row in data:
        wrapper.writerow(data[n])
        n+=1
    file.close()


def read_json(filename):
    """
    Returns the contents read from the JSON file filename.
    
    This function reads the contents of the file filename, and will use the json module
    to covert these contents in to a Python data value.  This value will either be a
    a dictionary or a list. 
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid JSON file
    """
    file = open(filename)
    text = file.read()
    data = json.loads(text)
    file.close()

    return data


def str_to_time(timestamp,tzsource=None):
    """
    Returns the datetime object for the given timestamp (or None if timestamp is 
    invalid).
    
    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.
    
    If the timestamp has a time zone, then it should keep that time zone even if
    the value for tzsource is not None.  Otherwise, if timestamp has no time zone 
    and tzsource is not None, then this function will use tzsource to assign 
    a time zone to the new datetime object.
    
    The value for tzsource can be None, a string, or a datetime object.  If it 
    is a string, it will be the name of a time zone, and it should localize the 
    timestamp.  If it is another datetime, then the datetime object created from 
    timestamp should get the same time zone as tzsource.
    
    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string
    
    Parameter tzsource: The time zone to use (OPTIONAL)
    Precondition: tzsource is either None, a string naming a valid time zone,
    or a datetime object.
    """
    # HINT: Use the code from the previous exercise and add time zone handling.
    # Use localize if tzsource is a string; otherwise replace the time zone if not None
    try:
        d = parse(timestamp)
    except:
        return None

    if d.tzinfo != None:
        return d

    if not tzsource:
        return d

    if type(tzsource) == str:
        tz = pytz.timezone(tzsource)
        d = tz.localize(d)
    elif isinstance(tzsource, datetime.datetime):
        tz = tzsource.tzinfo
        d = d.replace(tzinfo = tz)

    return d

def daytime(time,daycycle):
    """
    Returns true if the time takes place during the day.
    
    A time is during the day if it is after sunrise but before sunset, as
    indicated by the daycycle dicitionary.
    
    A daycycle dictionary has keys for several years (as int).  The value for
    each year is also a dictionary, taking strings of the form 'mm-dd'.  The
    value for that key is a THIRD dictionary, with two keys "sunrise" and
    "sunset".  The value for each of those two keys is a string in 24-hour
    time format.
    
    For example, here is what part of a daycycle dictionary might look like:
    
        "2015": {
            "01-01": {
                "sunrise": "07:35",
                "sunset":  "16:44"
            },
            "01-02": {
                "sunrise": "07:36",
                "sunset":  "16:45"
            },
            ...
        }
    
    In addition, the daycycle dictionary has a key 'timezone' that expresses the
    timezone as a string. This function uses that timezone when constructing
    datetime objects from this set.  If the time parameter does not have a timezone,
    we assume that it is in the same timezone as the daycycle dictionary
    
    Parameter time: The time to check
    Precondition: time is a datetime object
    
    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: Use the code from the previous exercise to get sunset AND sunrise
    # Add a timezone to time if one is missing (the one from the daycycle)
    y = time.year
    md = time.strftime('%m')+'-'+time.strftime('%d')
    month = int(md[:2])
    day = int(md[3:])
    dctz = pytz.timezone(daycycle['timezone'])    # grab daycycyle tz string and make it comparable
    #Get sunset and sunrise
    try:    
        sunset_str = daycycle[str(y)][md]["sunset"]
        sunset_t = datetime.datetime(y, month, day, int(sunset_str[:2]), int(sunset_str[3:]))
        
        sunrise_str = daycycle[str(y)][md]["sunrise"]
        sunrise_t = datetime.datetime(y, month, day, int(sunrise_str[:2]), int(sunrise_str[3:]))            
    except:
        return None

    #check for tz and append, accordingly
    if time.tzinfo != None:                             # If time value includes a time zone
        sunrise_t = dctz.localize(sunrise_t)
        sunset_t= dctz.localize(sunset_t)    
    #check if time is between sunrise and sunset
    if time>sunrise_t and time<sunset_t:
        return True
    else:
        return False

def get_for_id(id,table):
    """
    Returns (a copy of) a row of the table with the given id.
    
    Table is a two-dimensional list where the first element of each row is an identifier
    (string).  This function searches table for the row with the matching identifier and
    returns a COPY of that row. If there is no match, this function returns None.
    
    This function is useful for extract rows from a table of pilots, a table of instructors,
    or even a table of planes.
    
    Parameter id: The id of the student or instructor
    Precondition: id is a string
    
    Parameter table: The 2-dimensional table of data
    Precondition: table is a non-empty 2-dimension list of strings
    """
    for row in range(len(table)):
        if id == table[row][0]:
            return table[row]
