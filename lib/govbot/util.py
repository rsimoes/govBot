import re

# Strip leading and trailing spaces on each line, redundant spacing:
def multiline_strip(string):
    string = re.sub(r'[ \t]+', ' ', string)
    string = re.sub(r'^\s+|\s+$', '', string, flags=re.MULTILINE)
    string = re.sub('[\n\r]+', '\n', string)
    return string
