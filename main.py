# This is a Python script for working with Vimeo's API called vimeup.

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import PySimpleGUI as sg
from configobj import ConfigObj


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.


def check_private_config():
    private_config = './private.ini'
    # Check if the private configuration file exists...
    if not os.path.isfile(private_config):
        private_config_setup()
    else:
        # ...or is empty...
        if os.stat(private_config).st_size == 0:
            private_config_setup()
            # ... or values missing? TODO Check for missing values.
            # TODO Can we authenticate?


def private_config_setup():
    # Configure private configuration that should only need to be configured once.
    sg.theme('LightBlue')
    layout = [[sg.Text('Go to https://developer.vimeo.com/apps/209908 to copy Client Identifier and Client Secrets. There you can also generate a Personal Access Token.', enable_events=True, key='https://developer.vimeo.com/apps/209908')],
                [sg.Text('Vimeup Client ID', size=(30, 1)), sg.InputText(size=(40, 1), key='client_identifier', tooltip="Enter the client identifier for Vimeup."), sg.Text('40 Characters')],
                [sg.Text('Vimeup Personal Access Token', size=(30, 1)), sg.InputText(size=(32, 1), key='personal_access_token'), sg.Text('32 Characters')],
                [sg.Text('Vimeup Client secret', size=(30, 1), justification='left'), sg.InputText(size=(128, 1), key='client_secret'), sg.Text('128 Characters')],
                [sg.Button('OK'), sg.Button('Cancel')]]
    # Create the Window
    window = sg.Window('Vimeup - Private Configuration Setup', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'OK':
            print(event, values)
            break
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        # print('You entered ', values[0])
    window.close()
    print('End of private_config_setup')
    # TODO Display values for Client ID and Client Secret if available, but not for personal access tokens. These should be generated new for each install.


# ###### MAIN PROGRAM #######
check_private_config()
