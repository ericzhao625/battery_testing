"""
Module driver template for a SCPI VISA power supply.
Implements all the standard SCPI commands for PSU control.
"""

from pyvisa.errors import InvalidSession

from inst_pyvisa import PyVisaInstrument

class PsuScpi(PyVisaInstrument):
    """
    Class to represent a standard SCPI VISA power supply.

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
        self.toggle_output(False)
        self.set_curr(0)
        self.set_volt(0)

    def set_curr(self, curr: float) -> None:
        """
        Sets the output current of the current channel.

        Args:
            curr (float): Current level in amps.
        """
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
        if volt <= self.max_volt:
            self.inst.write(f"VOLT {volt}")
        else:
            print(f"Invalid voltage, max voltage: {self.max_volt}V.")

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
        Disables all keys except for the key which enables local access.

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
