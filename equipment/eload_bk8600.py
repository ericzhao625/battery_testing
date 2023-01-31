"""
Module driver for a BK PRECISION 86XX series E-load.
"""

import eload_scpi_pyvisa
import eload_bk8600_consts

class Bk8600(eload_scpi_pyvisa.EloadScpi):
    """
    Class to represent a BK Precision 86XX series E-load.

    Args:
        visa_name (str): VISA resource name of the instrument.

    Attributes:
        inst: PyVISA resource instance.
        manufacturer: Manufacturer name of instrument.
        model_number: Model number of instrument.
        max_curr: Maximum current rating of instrument.
        max_volt: Maximum voltage rating of instrument.
        max_pow: Maximum power rating of instrument.
        mode: Operation mode (CC, CR, CV, CW) of instrument.
    """
    def __init__(self, visa_name: str) -> None:
        super().__init__(visa_name)
        # Set safety limits based on model number.
        self.max_volt = eload_bk8600_consts.MAX_VOLT[self.model_number]
        self.max_curr = eload_bk8600_consts.MAX_CURR[self.model_number]        
        self.max_pow = eload_bk8600_consts.MAX_POW[self.model_number]

    def toggle_remote_sense(self, state) -> None:
        """
        Toggles the use of remote sense.
        Ensure the remote sense is wired correctly to the I/O terminal
        block on the back of the e-load before using remote sense.
        Check manual for wiring help.

        Args:
            state (bool): True for ON, False for OFF.
        """
        if state:
            self.inst.write("REM:SENS ON")
        else:
            self.inst.write("REM:SENS OFF")
