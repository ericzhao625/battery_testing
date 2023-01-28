"""
Module for testing PyVISA connection to a new instrument.
Can be used for most interfaces (e.g. GPIB, RS232, USB, Ethernet)
Use to test commands for developing drivers.
Also serves as a basic template for using PyVISA with a device.
"""

import pyvisa

# Initialize PyVISA resource manager.
rm = pyvisa.ResourceManager()

try:
    while True:
        # Gets available resources (instruments).
        resource_list = rm.list_resources()
        # Prints the details of all available resources.
        print('\nAvailable Instrument List')
        for index, source in enumerate(resource_list):
            temp_inst = rm.open_resource(source)
            print(f'Index: {index}  |  Instrument Details: {temp_inst.query("*IDN?")}')

        # Select a resource to communicate with, and print its VISA resource name.
        resource_num = int(input('Select Source Index: '))
        print(f'VISA Resource name: {resource_list[resource_num]}')

        # Send commands to the chosen resource.
        try:
            # May need to change the termination character, input doesn't work with '\n' atm.
            # term_char = input("Termination character (\\n is the default): ")
            inst = rm.open_resource(resource_list[resource_num])
            while True:
                command = input("Command ('X' to change instruments): ")
                if command != 'X':
                    try:
                        # Try querying (Write command followed by a Read command).
                        print(inst.query(command))
                        print("Query command.")
                    except pyvisa.errors.VisaIOError:
                        # If query results in a timeout, may be a write command or error.
                        print("Either a write command OR invalid command.")
                else:
                    break
        except IndexError:
            print('Invalid index.\n')

except KeyboardInterrupt:
    print("\nQuit.")
