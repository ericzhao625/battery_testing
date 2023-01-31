"""
Constants related to KEYSIGHT E3631A control.
"""

BAUD_RATE = 9600

# min_volt, max_volt, max_curr

MIN_VOLT = {
    1: 0,
    2: 0,
    3: -25,
}

MAX_VOLT = {
    1: 5,
    2: 25,
    3: 0,
}

MAX_CURR = {
    1: 5,
    2: 1,
    3: 1,
}
