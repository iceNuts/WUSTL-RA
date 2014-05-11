import re

"""
    fetch legislature number
"""

def fetch(text):
    regex = re.compile("LEGISLATURA(.*?),")
    r = regex.search(text)
    try:
        return r.groups()[0]
    except Exception, e:
        return "None"

        
