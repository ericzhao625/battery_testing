"""
Module driver for the RIGOL DL3000 series E-loads.
"""

from eload_scpi_pyvisa import EloadScpi
import eload_dl3000_consts as dl3000_consts

class Dl3000(EloadScpi):
    """
    Class to represent a RIGOL DL3000 series E-load.

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
        self.max_volt = dl3000_consts.MAX_VOLT[self.model_number]
        self.max_pow = dl3000_consts.MAX_POW[self.model_number]
        self.set_range("MAX")

    def set_range(self, curr_range: str) -> None:
        """
        Sets the current range for constant current mode.
        Low range provides better resolution and accuracy.

        Args:
            range (str): "MIN" for low range, "MAX" for high range.
        """
        self.max_curr = dl3000_consts.MAX_CURR[self.model_number][curr_range]
        self.inst.write(f"CURR:RANG {curr_range}")
