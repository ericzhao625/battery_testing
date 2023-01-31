"""
Constants related to the RIGOL DL3000 series E-Loads
"""

# max_volt, max_curr, max_pow
MAX_SPECS = {
    'DL3021': {
        "MAX_VOLT": 150,
        "MAX_CURR": {
            "MIN": 4,
            "MAX": 40,
        },
        "MAX_POW": 200,
    },
    'DL3021A': {
        "MAX_VOLT": 150,
        "MAX_CURR": {
            "MIN": 4,
            "MAX": 40,
        },
        "MAX_POW": 200,
    },
    'DL3031': {
        "MAX_VOLT": 150,
        "MAX_CURR": {
            "MIN": 6,
            "MAX": 60,
        },
        "MAX_POW": 350,
    },
    'DL3031A': {
        "MAX_VOLT": 150,
        "MAX_CURR": {
            "MIN": 6,
            "MAX": 60,
        },
        "MAX_POW": 350,
    },
}
