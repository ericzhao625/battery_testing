"""
Module driver for a KEYSIGHT E3631A series power supply.
Commands here: https://www.keysight.com/us/en/assets/9018-01308/user-manuals/9018-01308.pdf
"""

from pyvisa.errors import InvalidSession

import inst_pyvisa
import psu_e3631a_consts

class E363xa(inst_pyvisa.PyVisaInstrument):
    """
    Class to represent a KEYSIGHT E3631A series power supply.

    Args:
        visa_name (str): VISA resource name of the instrument.
        model_number (str): Model number of the instrument.

    Attributes:
        inst: PyVISA resource instance.
        manufacturer: Manufacturer name of instrument.
        model_number: Model number of instrument.
        max_curr: Maximum current rating of the channel.
        min_volt: Minimum voltage rating of the channel
        max_volt: Maximum voltage rating of the channel.
        max_pow: Maximum power rating of instrument.
    """
    def __init__(self, visa_name: str) -> None:
        super().__init__(visa_name)
        self.inst.baud_rate = psu_e3631a_consts.BAUD_RATE

        # Initialize settings of PSU.
        self.inst.write("*RST")
        self.disable_front_panel(True)
        self.max_curr = 0
        self.min_volt = 0
        self.max_volt = 0
        self.set_channel(2)
        self.toggle_output(False)
        self.set_curr(0)
        self.set_volt(0)

    def set_channel(self, channel: int) -> None:
        """
        Sets the channel of the PSU to the one specified.
        1 is the 6V output.
        2 is the +25V output.
        3 is the -25V output.

        Args:
            channel (int): Channel number.
        """
        if channel in psu_e3631a_consts.MAX_SPECS:
            self.min_curr = psu_e3631a_consts.MAX_SPECS[channel][0]
            self.max_curr = psu_e3631a_consts.MAX_SPECS[channel][1]
            self.max_volt = psu_e3631a_consts.MAX_SPECS[channel][2]
            self.inst.write(f"INST:NSEL {channel}")
        else:
            print("Invalid channel.")

    def set_curr(self, curr: float) -> None:
        """
        Sets the output current of the current channel.

        Args:
            curr (float): Current level in amps.
        """
        curr = round(curr, 3)
        if curr <= self.max_curr:
            self.inst.write(f"CURR {curr}")
        else:
            print(f"Invalid current, max current {self.max_curr}A.")

    def measure_curr(self) -> float:
        """
        Measures the output current of the PSU.

        Returns:
            float: Measured current value in amps.
        """
        return self.inst.query("MEAS:CURR?")

    def set_volt(self, volt: float) -> None:
        """
        Sets the output voltage of the current channel.

        Args:
            volt (float): Voltage level in volts.
        """
        volt = round(volt, 3)
        if self.min_volt <= volt <= self.max_volt:
            self.inst.write(f"VOLT {volt}")
        else:
            print(f"Invalid voltage, voltage range: {self.min_volt} to {self.max_volt}V.")

    def measure_volt(self) -> float:
        """
        Measures the output voltage of the PSU.

        Returns:
            float: Measured voltage value in amps.
        """
        return self.inst.query("MEAS:VOLT?")

    def measure_pow(self) -> float:
        """
        Measures the power output of the PSU.

        Returns:
            float: Output power value.
        """
        return self.measure_volt() * self.measure_curr()

    def toggle_output(self, state: bool) -> None:
        """
        Toggles the output of the PSU.

        Args:
            state (bool): True for ON, False for OFF.
        """
        if state:
            self.inst.write("OUTP ON")
        else:
            self.inst.write("OUTP OFF")

    def disable_front_panel(self, state) -> None:
        """
        Toggles access to the front panel keys.
        Disables all keys except for the "Local" key which enables access.

        Args:
            state (bool): True for locked, False for unlocked.
        """
        if state:
            self.inst.write("SYST:REM")
        else:
            self.inst.write("SYST:LOC")

    def __del__(self):
        try:
            self.toggle_output(False)
            self.disable_front_panel(False)
            self.inst.close()
        except (AttributeError, InvalidSession):
            pass
