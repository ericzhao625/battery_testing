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
        manufacturer: Manufacturer name of instrument.
        model_number: Model number of instrument.
        serial_number: Serial number of instrument.
        firmware_level: Firmware level of instrument.
    """
    def __init__(self, visa_name: str) -> None:
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(visa_name)
        try:
            idn = self.inst.query('*IDN?').split(', ')
            self.manufacturer = idn[0]
            self.model_number = idn[1]
            self.serial_number = idn[2]
            self.firmware_level = idn[3]
            print(f"Connected to {idn[0]} {idn[1]}.")
        except pyvisa.errors.VisaIOError:
            print(f"Connected to {visa_name}.")
