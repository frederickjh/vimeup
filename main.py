# This is a Python script for working with Vimeo's API called vimeup.

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import PySimpleGUI as sg
from configobj import ConfigObj


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.


def check_private_config():
    """Check that the private configuration file exists and contains valid authentication details."""
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
    """ Configure private configuration that should only need to be configured once."""
    privateconfig = ConfigObj('./private.ini')
    try:
        client_identifier_prefill = privateconfig["client_identifier"]
    except:
        client_identifier_prefill = ""
    try:
        client_secret_prefill = privateconfig["client_secret"]
    except:
        client_secret_prefill = ""
    try:
        personal_access_token_prefill = privateconfig["personal_access_token"]
        if (not personal_access_token_prefill):
            password_character = ""
        else:
            password_character ="●a6cc33b70824a9af75766beb01458426"
    except:
        personal_access_token_prefill = ""
        password_character = ""
    sg.theme('LightBlue')
    layout = [[sg.Text('Go to https://developer.vimeo.com/apps/209908 to copy Client Identifier and Client Secrets. There you can also generate a Personal Access Token.', enable_events=True, key='https://developer.vimeo.com/apps/209908')],
                [sg.Text('Vimeup Client ID', size=(30, 1)), sg.InputText(size=(40, 1), key='client_identifier', default_text=client_identifier_prefill, tooltip="Enter the client identifier for Vimeup."), sg.Text('40 Characters')],
                [sg.Text('Vimeup Client secret', size=(30, 1), justification='left'), sg.InputText(size=(135, 1), key='client_secret', default_text=client_secret_prefill, tooltip="Enter the client secret for Vimeup."), sg.Text('128 Characters')],
                [sg.Text('Vimeup Personal Access Token', size=(30, 1)), sg.InputText(size=(38, 1), key='personal_access_token', default_text=personal_access_token_prefill, password_char=password_character, tooltip="Enter the personal access token for Vimeup."), sg.Text('32 Characters'), sg.Text("Generate a new personal access token on Vimeo if you need one.", text_color="red")],
                [sg.Button('OK'), sg.Button('Cancel')]]
    # Create the Window
    window = sg.Window('Vimeup - Private Configuration Setup', layout, font=["Arial", 12])
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'OK':
            privateconfig
            private_config_write(**values)
            break
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
    window.close()



def private_config_write(client_identifier, client_secret, personal_access_token):
    """Writes the private configuration to the private configuration file."""
    privateconfig = ConfigObj('./private.ini')
    privateconfig['client_identifier'] = client_identifier
    privateconfig['client_secret'] = client_secret
    privateconfig['personal_access_token'] = personal_access_token
    privateconfig.write()

# ###### MAIN PROGRAM #######
check_private_config()
