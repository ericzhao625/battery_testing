"""
Module driver for a KEYSIGHT E3631A series power supply.
Commands here: https://www.keysight.com/us/en/assets/9018-01308/user-manuals/9018-01308.pdf
"""

import psu_scpi_pyvisa
import psu_e3631a_consts

class E363xa(psu_scpi_pyvisa.ScpiPsu):
    """
    Class to represent a KEYSIGHT E3631A series power supply.

    Args:
        visa_name (str): VISA resource name of the instrument.

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
        self.min_volt = 0
        super().__init__(visa_name)
        self.inst.baud_rate = psu_e3631a_consts.BAUD_RATE
        self.set_channel(2)

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
            self.min_volt = psu_e3631a_consts.MAX_SPECS[channel][0]
            self.max_volt = psu_e3631a_consts.MAX_SPECS[channel][1]
            self.max_curr = psu_e3631a_consts.MAX_SPECS[channel][2]
            self.inst.write(f"INST:NSEL {channel}")
        else:
            print("Invalid channel.")

    def set_curr(self, curr: float) -> None:
        """
        Sets the output current of the current channel.

        Args:
            curr (float): Current level in amps.
        """
        super().set_curr(round(curr, 3))

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
