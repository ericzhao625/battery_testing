"""
Constants related to BK Precision 9103/9104 control.
"""

BAUD_RATE = 9600
READ_TERMINATION = '\r'
WRITE_TERMINATION = '\r'

MAX_VOLT = {
    '9103': 42,
    '9104': 84,
}

MAX_CURR = {
    '9103': 20,
    '9104': 10,
}

MAX_POW = {
    '9103': 320,
    '9104': 320,
}
