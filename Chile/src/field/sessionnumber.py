import re

"""
    fetch session number
"""

def fetch(text):
    regex = re.compile("Sesion(.*?),")
    r = regex.search(text)
    try:
        return r.groups()[0]
    except Exception, e:
        return "None"

        
