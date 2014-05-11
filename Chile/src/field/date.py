import re

"""
    fetch date
"""

def fetch(text):
    regex = re.compile("en(.*?)\(")
    r = regex.search(text)
    try:
        return r.groups()[0]
    except Exception, e:
        return "None"

        
