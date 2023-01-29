"""
Template for a PyVISA instrument.
"""

import pyvisa

class PyVisaInstrument:
    """
    Class to represent a instrument for use with PyVISA.

    Args:
        visa_name (str): VISA resource name of the instrument.

    Attributes:
        inst: PyVISA resource instance.
        idn: Identifying details of the instrument.
    """
    def __init__(self, visa_name: str) -> None:
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(visa_name)
        self.idn = self.inst.query('*IDN?').split(', ')
        self.model_number = self.idn[1]
        print(f"Connected to {self.idn[0]} {self.idn[1]}.")
