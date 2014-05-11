import re

"""
    fetch legislature type
"""

def fetch(text):
    regex = re.compile("LEGISLATURA(.*?), (.*?) ")
    r = regex.search(text)
    try:
        return r.groups()[1]
    except Exception, e:
        return "None"

        
