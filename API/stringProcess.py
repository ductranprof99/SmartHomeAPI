
"""
xu ly value cho feed, the form of the feed kinda retard, so i must change that shit
"""

def dehumanize(unit,value):
    if unit==None:
        return int(value)
    elif unit == "":
        if int(value) < 100: return 'Toi'
        return 'Sang'
    else:
        return [int(s) for s in value.split('-')]

