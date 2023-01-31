"""
Script for testing PyVISA connection to a new instrument.
Can be used for most interfaces (e.g. GPIB, RS232, USB, Ethernet).
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
        print(resource_list)
        # Prints the details of all available resources.
        print('\nAvailable Instrument List')
        for index, source in enumerate(resource_list):
            inst = rm.open_resource(source)
            try:
                print(f'Index: {index}  |  Instrument Details: {inst.query("*IDN?")}')
            except pyvisa.errors.VisaIOError:
                # Instrument does not support *IDN? command
                print(f'Index: {index}  |  Instrument Details: {source}')
        # Select a resource to communicate with, and print its VISA resource name.
        resource_num = int(input('Select Source Index: '))
        print(f'VISA Resource name: {resource_list[resource_num]}')

        # Send commands to the chosen resource.
        try:
            term_char = input("Termination character (n for \\n, r for \\r): ")
            if term_char == 'r':
                term_char = '\r'
            else:
                term_char = '\n'
            inst = rm.open_resource(
                resource_list[resource_num],
                write_termination = term_char,
                read_termination = term_char
            )
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
