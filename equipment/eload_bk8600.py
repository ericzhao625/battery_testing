"""
Module driver for a BK PRECISION 86XX series E-load.
"""

from pyvisa.errors import InvalidSession

import inst_pyvisa
import eload_bk8600_consts as bk_8600_const

class Bk8600(inst_pyvisa.PyVisaInstrument):
    """
    Class to represent a BK Precision 86XX series E-load.
    """
    def __init__(self, visa_name: str) -> None:
        super().__init__(visa_name)
        # Set safety limits based on model number.
        self.max_curr = bk_8600_const.MAX_SPECS[self.idn[1]][0]
        self.max_volt = bk_8600_const.MAX_SPECS[self.idn[1]][1]
        self.max_pow = bk_8600_const.MAX_SPECS[self.idn[1]][2]

        # Reset to default settings of E-load (constant current).
        self.inst.write("*RST")
        # E-load initializes to constant current mode.
        self.mode = "CURR"

    def set_const_curr_mode(self) -> None:
        """
        Changes the input regulation mode to constant current.
        E-Load will draw a constant current frorm the source.
        """
        self.mode = "CURR"
        self.inst.write("FUNC CURR")

    def set_curr(self, current: float) -> None:
        """
        Sets the constant current if the e-load is in constant current mode.

        Args:
            current (float): Current value in amps.
        """
        if self.mode == "CURR":
            if current <= self.max_curr:
                self.inst.write(f"CURR {current}")
            else:
                print(f"{current} greater than max current {self.max_curr}.")
        else:
            print(f"Attempt to change current in incorrect mode ({self.mode}).")

    def set_const_res_mode(self) -> None:
        """
        Changes the input regulation mode to constant voltage.
        E-Load will act as a resistor with constant resistance.
        """
        self.mode = "RES"
        self.inst.write("FUNC RES")

    def set_res(self, resistance: float) -> None:
        """
        Sets the constant resistance if the e-load is in constant resistance mode.

        Args:
            resistance (float): Resistance level in ohms.
        """
        if self.mode == "RES":
            self.inst.write(f"RES {resistance}")
        else:
            print(f"Attempt to change resistance in incorrect mode ({self.mode}).")

    def set_const_volt_mode(self) -> None:
        """
        Changes the input regulation mode to constant voltage.
        E-Load will serve as a constant voltage drop.
        """
        self.mode = "VOLT"
        self.inst.write("FUNC VOLT")

    def set_volt(self, voltage: float) -> None:
        """
        Sets the constant voltage if the e-load is in constant voltage mode.

        Args:
            voltage (float): Voltage level in volts.
        """
        if self.mode == "VOLT":
            if voltage <= self.max_volt:
                self.inst.write(f"VOLT {voltage}")
            else:
                print(f"{voltage} greater than max current {self.max_volt}.")
        else:
            print(f"Attempt to change voltage in incorrect mode ({self.mode}).")

    def set_const_pow_mode(self) -> None:
        """
        Changes the input regulation mode to constant voltage.
        E-Load will serve as a constant power drop, current determined by circuit.
        Current and voltage are determined by the circuit connected.
        """
        self.mode = "POW"
        self.inst.write("FUNC POW")

    def set_pow(self, power: float) -> None:
        """
        Sets the constant power if the e-load is in constant power mode.

        Args:
            power (float): Power level in watts.
        """
        if self.mode == "POW":
            if power <= self.max_pow:
                self.inst.write(f"POW {power}")
            else:
                print(f"{power} greater than max power {self.max_pow}.")
        else:
            print(f"Attempt to change power in incorrect mode ({self.mode}).")

    def toggle_output(self, state) -> None:
        """
        Toggles the input into the e-load.

        Args:
            state (bool): True for ON, False for OFF.
        """
        if state:
            self.inst.write("INP ON")
        else:
            self.inst.write("INP OFF")

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

    def measure_voltage(self) -> float:
        """
        Performs a "one-shot" measurement of the voltage drop across the e-load.

        Returns:
            float: voltage drop across the e-load in volts.
        """
        return float(self.inst.query("MEAS:VOLT?"))

    def measure_current(self) -> float:
        """
        Performs a "one-shot" measurement of the current draw by the e-load.

        Returns:
            float: current draw from the source (negative)
        """
        return -float(self.inst.query("MEAS:CURR?"))

    def __del__(self) -> None:
        try:
            self.toggle_output(False)
            self.disable_front_panel(False)
            self.inst.close()
        except (AttributeError, InvalidSession):
            pass
