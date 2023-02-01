"""
Module driver template for a SCPI VISA digital multimeter.
Implements all the standard SCPI commands for DMM control.
"""

from pyvisa.errors import InvalidSession

import dmm_ks34410a_consts as ks34410a_consts
from inst_pyvisa import PyVisaInstrument

class Ks34410A(PyVisaInstrument):
    """
    Class to represent a standard SCPI VISA digital multimeter.

    Args:
        visa_name (str): VISA resource name of the instrument.

    Attributes:
        inst: PyVISA resource instance.
        manufacturer: Manufacturer name of instrument.
        model_number: Model number of instrument.
        max_curr: Maximum current rating of the channel.
        max_volt: Maximum voltage rating of the channel.
    """
    def __init__(self, visa_name: str) -> None:
        super().__init__(visa_name)

        # Initialize settings of PSU.
        self.inst.write("*RST")
        self.disable_front_panel(True)
        self.max_curr = 0
        self.max_volt = 0
        self.mode = "NONE"
        self.nplc = 1
        self.resolution = 0
        self.meas_range = 0
        self.set_mode("VOLT:DC")


    def disable_front_panel(self, state) -> None:
        """
        Toggles access to the front panel keys.
        Remote disables all keys except for the "Local" key which enables access.

        Args:
            state (bool): True for remote mode, False for local mode.
        """
        if state:
            self.inst.write("SYST:REM")
        else:
            self.inst.write("SYST:LOC")

    def set_mode(self, mode: str="VOLT:DC") -> None:
        """
        Sets the output current of the current channel.

        Args:
            mode (str): Measurement mode.
                CAP = Capacitance
                CONT = Continuity
                CURR:AC = AC Current
                CURR:DC = DC Current
                DIOD = Diode
                FREQ = Frequency
                PER = Period
                RES = Resistance
                TEMP = Temperature
                VOLT:AC = AC Voltage
                VOLT:DC = DC Voltage
        """
        self.mode = mode
        self.inst.write(f"FUNC:{mode}")

    def set_nplc(self, nplc: float=1) -> None:
        """
        Sets the NPLC (integration time) for the current measurement mode.
        Larger NPLC uses longer integration times leading to better resolution
        but slower measurements.

        Args:
            nplc (float): NPLC value.
        """
        if nplc in ks34410a_consts.NPLC_RANGE:
            self.nplc = nplc
            self.resolution = self.calc_resolution(ks34410a_consts.NPLC_RANGE[nplc])
            self.inst.write(f"{self.mode}:NPLC {nplc}")
        else:
            print("Invalid NPLC selection.")

    def calc_resolution(self, pmm):
        res = round(0.000001 * pmm * self.meas_range)
        counter = 0
        if res > 1:
            while res % 10 == 0:
                res /= 10
                counter += 1
        elif res < 1:
            while res * 10 <= 10:
                res *= 10
                counter -= 1
        return 10 ** counter

    def convert_resolution(self, val):
        return round(val / self.resolution) * self.resolution

    def measure_volt(self, nplc: float=1, volt_range: str='AUTO') -> None:
        if self.mode != "VOLT:DC":
            self.set_mode("VOLT:DC")
        if self.nplc != nplc:
            self.set_nplc(nplc)

    def __del__(self) -> None:
        try:
            self.disable_front_panel(False)
            self.inst.close()
        except (AttributeError, InvalidSession):
            pass
