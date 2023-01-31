"""
Module driver for a BK PRECISION 9103/9104 series power supply.
Note that this PSU uses "non-standard" serial commands.

There are some commands where the return value is two messages.
At the moment, these are cleared manually each time by querying
an empty string.
This could potentially be replaced by a function that automatically
clears/saves the message buffer.
"""

from pyvisa.errors import InvalidSession

import inst_pyvisa
import psu_bk9103_consts

class Bk9103(inst_pyvisa.PyVisaInstrument):
    """
    Class to represent a BK PRECISION 9103/9104 series power supply.

    Args:
        visa_name (str): VISA resource name of the instrument.
        model_number (str): Model number of the instrument.

    Attributes:
        inst: PyVISA resource instance.
        manufacturer: Manufacturer name of instrument.
        model_number: Model number of instrument.
        max_curr: Maximum current rating of instrument.
        max_volt: Maximum voltage rating of instrument.
        max_pow: Maximum power rating of instrument.
    """
    def __init__(self, visa_name: str, model_number: str) -> None:
        super().__init__(visa_name)
        self.inst.baud_rate = psu_bk9103_consts.BAUD_RATE
        self.inst.read_termination = psu_bk9103_consts.READ_TERMINATION
        self.inst.write_termination = psu_bk9103_consts.WRITE_TERMINATION

        # Manually setting these specifications as there is no *IDN? command.
        self.manufacturer = "B&K Precision"
        self.model_number = model_number

        self.max_curr = psu_bk9103_consts.MAX_SPECS[self.model_number][0]
        self.max_volt = psu_bk9103_consts.MAX_SPECS[self.model_number][1]
        self.max_pow = psu_bk9103_consts.MAX_SPECS[self.model_number][2]

        # Initialize settings of PSU.
        self.toggle_output(False)
        self.disable_front_panel(True)
        self.set_curr(0)
        self.set_volt(0)
        self.set_preset_mode(3)

    def float_to_4_dig(self, val: float) -> str:
        """
        Converts float value to a 4 digit int.
        Multiplies float value by 100 and adds leading zeros if needed.

        Args:
            val (float): Value to convert.

        Returns:
            str: Converted value.
        """
        val = str(int(val * 100))
        while len(val) < 4:
            val = '0' + val
        return val

    def query_to_float(self, val: str) -> float:
        """
        Divides queried value by 100 to convert it to its real float value.

        Returns:
            float: Converted value.
        """
        return float(val) / 100

    def set_curr(self, curr: float, preset_num: int=3) -> None:
        """
        Sets the output current of the PSU.

        Args:
            curr (float): Current level in amps.
            preset_num (int): Preset to use (0=A, 1=B, 2=C, 3=Normal).
        """
        curr = round(curr, 2)
        volt = self.get_volt(preset_num)
        if curr <= self.max_curr and curr * volt <= self.max_pow:
            self.inst.query(f"CURR{preset_num}{self.float_to_4_dig(curr)}")
        else:
            print("Invalid current.")

    def get_curr(self, preset_num: int=3) -> float:
        """
        Gets the output current setting of the PSU.

        Args:
            preset_num (int): Preset to use (0=A, 1=B, 2=C, 3=Normal).

        Returns:
            float: Set current value in amps.
        """
        curr = self.inst.query(f"GETS{preset_num}")[4:8]
        # Clear output buffer
        self.inst.query("")
        return self.query_to_float(curr)

    def measure_curr(self) -> float:
        """
        Measures the output current of the PSU.

        Returns:
            float: Displayed current value in amps.
        """
        curr = self.inst.query("GETD")[4:8]
        # Clear output buffer
        self.inst.query("")
        return self.query_to_float(curr)

    def set_volt(self, volt: float, preset_num: int=3) -> None:
        """
        Sets the output voltage of the PSU.

        Args:
            volt (float): Voltage level in volts.
            preset_num (int): Preset to use (0=A, 1=B, 2=C, 3=Normal).
        """
        volt = round(volt, 2)
        curr = self.get_curr(preset_num)
        if volt <= self.max_volt and volt * curr <= self.max_pow:
            self.inst.query(f"VOLT{preset_num}{self.float_to_4_dig(volt)}")
        else:
            print("Invalid voltage.")

    def get_volt(self, preset_num: int=3) -> float:
        """
        Gets the output voltage setting of the PSU.

        Args:
            preset_num (int): Preset to use (0=A, 1=B, 2=C, 3=Normal).

        Returns:
            float: Set voltage value in volts.
        """
        volt = self.inst.query(f"GETS{preset_num}")[0:4]
        # Clear output buffer
        self.inst.query("")
        return self.query_to_float(volt)

    def measure_volt(self) -> float:
        """
        Measures the output voltage of the PSU.

        Returns:
            float: Displayed voltage value in volts.
        """
        volt = self.inst.query("GETD")[0:4]
        # Clear output buffer
        self.inst.query("")
        return self.query_to_float(volt)

    def set_curr_volt(self, curr: float, volt: float, preset_num: int=3) -> None:
        """
        Sets the output voltage and current of the PSU.

        Args:
            curr (float): Current level in amps.
            volt (float): Voltage level in volts.
            preset_num (int): Preset to use (0=A, 1=B, 2=C, 3=Normal).
        """
        curr = round(curr, 2)
        volt = round(volt, 2)
        if (
            curr <= self.max_curr
            and volt <= self.max_volt
            and volt * curr <= self.max_pow
        ):
            self.inst.query(
                f"SETD{preset_num}{self.float_to_4_dig(volt)}{self.float_to_4_dig(curr)}"
            )
        else:
            print("Invalid voltage and current combination.")

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
            self.inst.query("SOUT1")
        else:
            self.inst.query("SOUT0")

    def set_preset_mode(self, preset_num: int=3) -> None:
        """
        Sets the preset mode of the PSU.

        Args:
            preset_num (int): Preset to use (0=A, 1=B, 2=C, 3=Normal).
        """
        self.inst.query(f"SABC{preset_num}")

    def disable_front_panel(self, state) -> None:
        """
        Toggles access to the front panel keys.
        Disables all keys except for the "LOCK" key which enables access.

        Args:
            state (bool): True for locked, False for unlocked.
        """
        if state:
            self.inst.query("SESS")
        else:
            self.inst.query("ENDS")

    def __del__(self):
        try:
            self.toggle_output(False)
            self.disable_front_panel(False)
            self.inst.close()
        except (AttributeError, InvalidSession):
            pass
