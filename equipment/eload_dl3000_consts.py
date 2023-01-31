"""
Constants related to the RIGOL DL3000 series E-Loads.
"""

MAX_VOLT = {
    "DL3021": 150,
    "DL3021A": 150,
    "DL3031": 150,
    "DL3031A": 150,
}

MAX_CURR = {
    "DL3021": {
        "MIN": 4,
        "MAX": 40,
    },
    "DL3021A":{
        "MIN": 4,
        "MAX": 40,
    },
    "DL3031":{
        "MIN": 6,
        "MAX": 60,
    },
    "DL3031A": {
        "MIN": 6,
        "MAX": 60,
    },
}

MAX_POW = {
    "DL3021": 200,
    "DL3021A": 200,
    "DL3031": 350,
    "DL3031A": 350,
}
