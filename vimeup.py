# This is a Python script for working with Vimeo's API called vimeup.

# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import PySimpleGUI as sg
from configobj import ConfigObj
from validate import Validator
import vimeo
import sys
import webbrowser
import gettext

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.


def check_private_config():
    """Check that the private configuration file exists and contains valid authentication details."""
    # Check if the private configuration file exists...
    if not os.path.isfile(private_config) or os.stat(private_config).st_size == 0:
        private_config_setup()
    # Validate the private configuration.
    result = privateconfig.validate(validator)

    if result != True:
        sg.theme('LightBlue')
        layout = [[sg.Text(t('The validation of the private configuration failed. This contains the authorization details for the Vimeo API. Without being able to authorize there is not much this program can do.'))],
                  [sg.Text(t('Would you like to fix the private configuration? Or exit? '))],
                  [sg.Button(t('Yes'),key='yes'), sg.Button(t('Exit'), key='exit')]]
        # Create the Window
        window = sg.Window(t('Vimeup - Private configuration validation failed!'), layout, font=["Arial", 12])
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == 'yes':
                window.close()
                private_config_setup()
                check_private_config()
                break
            if event == sg.WIN_CLOSED or event == 'exit':  # if user closes window or clicks cancel
                sys.exit(1)
                break
        window.close()


def private_config_setup():
    """Configure private configuration that should only need to be configured once."""
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
            password_character ="●"
    except:
        personal_access_token_prefill = ""
        password_character = ""
    sg.theme('LightBlue')
    layout = [[sg.Text(t('On the Vimeo Developer site you can copy the Client Identifier and Client Secrets. You can also generate a Personal Access Token.')),sg.Button(t('Open Vimeo developer site in a web browser'), key='-to-vimeo-')],
                [sg.Text(t('Vimeup Client ID'), size=(30, 1)), sg.InputText(size=(40, 1), key='client_identifier', default_text=client_identifier_prefill, tooltip=t("Enter the client identifier for Vimeup.")), sg.Text(t('40 Characters'))],
                [sg.Text(t('Vimeup Client secret'), size=(30, 1), justification='left'), sg.InputText(size=(135, 1), key='client_secret', default_text=client_secret_prefill, tooltip=t("Enter the client secret for Vimeup.")), sg.Text(t('128 Characters'))],
                [sg.Text(t('Vimeup Personal Access Token'), size=(30, 1)), sg.InputText(size=(38, 1), key='personal_access_token', default_text=personal_access_token_prefill, password_char=password_character, tooltip=t("Enter the personal access token for Vimeup.")), sg.Text(t('32 Characters')), sg.Text(t("Generate a new personal access token on Vimeo if you need one."), text_color="red")],
                [sg.Button(t('OK'), key='ok'), sg.Button(t('Cancel'), key='cancel')]]
    # Create the Window
    window = sg.Window(t('Vimeup - Private Configuration Setup'), layout, font=["Arial", 12])
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == '-to-vimeo-':
            popupreturned=sg.popup(t('I will now start a web browser and open the Vimeo developer site so you can get or create the required private configuration for this program, Vimeup.'), t('Click OK and the browser will open'), title=t('Vimeup - Launch Vimeo Developer site in web browser?'), line_width=70, font=["Arial", 12])
            if popupreturned == 'OK':
                # Open web browser window.
                webbrowser.open('https://developer.vimeo.com/apps/209908')
        if event == 'ok':
            private_config_write(**values)
            break
        if event == sg.WIN_CLOSED or event == 'cancel':  # if user closes window or clicks cancel
            break
    window.close()


def private_config_write(client_identifier, client_secret, personal_access_token):
    """Writes the private configuration to the private configuration file."""
    privateconfig['client_identifier'] = client_identifier
    privateconfig['client_secret'] = client_secret
    privateconfig['personal_access_token'] = personal_access_token
    privateconfig.write()


def vimeo_test_authentication():
    """Tests if we can authenticate with Vimeo using the private configuration."""
    client = vimeo.VimeoClient(
        token=privateconfig['personal_access_token'],
        key=privateconfig['client_identifier'],
        secret=privateconfig['client_secret']
    )
    # Make the request to the server for the "/me" endpoint.
    response = client.get('/tutorial')
    # Make sure we got back a successful response.
    if not response.status_code == 200:
        error_dict=response.json()
        unpack_error_message(**error_dict)
        sg.theme('LightBlue')
        layout = [[sg.Text(t('We were unable to authenticate or connect to Vimeo.'), size=(50, 1))],
                  [sg.Text(t('The HTTP response code returned was:')), sg.Text(str(response.status_code), text_color="red")],
                  [sg.Text(t('The error message was:'))],
                  [sg.Text(error_msg, text_color="red")],
                  [sg.Button(t('OK'), key='ok'), sg.Button(t('Cancel'), key='cancel')]]
        # Create the Window
        window = sg.Window(t('Vimeup - Authentication / Connection to Vimeo failed'), layout, font=["Arial", 12])
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == 'ok':
                break
            if event == sg.WIN_CLOSED or event == 'cancel':  # if user closes window or clicks cancel
                break
        window.close()


def unpack_error_message(error):
    global error_msg
    error_msg = error


def check_local_config():
    """Check that the local configuration file exists and is not empty."""
    # Check if the local configuration file exists...
    if not os.path.isfile(local_config) or os.stat(local_config).st_size == 0 :
        sg.theme('LightBlue')
        layout = [[sg.Text(t('The local configuration file either does not exist or is empty.'))],
                  [sg.Text(t('Would you like to setup the local configuration? Or use the default?'))],
                  [sg.Button(t('Yes'), key='yes'), sg.Button(t('Use Default local configuration'), key='default')]]
        # Create the Window
        window = sg.Window('Vimeup - Local configuration file missing or empty.', layout, font=["Arial", 12])
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == 'yes':
                window.close()
                local_config_setup()
                break
            if event == sg.WIN_CLOSED or event == 'default':  # if user closes window or choses to use the default local configuration
                localconfig['shared_configuration_file'] = './shared.ini'
                localconfig['upload_directory'] = './'
                localconfig['download_directory'] = './'
                localconfig.write()
                break
        window.close()

    # Validate the private configuration.
    result = localconfig.validate(validator)
    if result != True:
        local_config_setup()

def local_config_setup():
    """Configure local configuration."""
    try:
        shared_configuration_file_prefill = localconfig["shared_configuration_file"]
    except:
        shared_configuration_file_prefill = ""
    try:
        upload_directory_prefill = localconfig["upload_directory"]
    except:
        upload_directory_prefill = ""
    try:
        download_directory_prefill = localconfig["download_directory"]
    except:
        download_directory_prefill = ""
    sg.theme('LightBlue')
    layout = [[sg.Text(t('Vimeup shared configuration file'), size=(30, 1)), sg.InputText(size=(40, 1), key='shared_configuration_file', default_text=shared_configuration_file_prefill, tooltip=t("This is the location and name of the shared Vimeup configuration file. This can be shared via a file synchronization service.")),sg.FileSaveAs(button_text=t("Choose File"), file_types=((t("Configuration Files"), "*.ini"),(t("ALL Files"), "*.*")), initial_folder="./", default_extension=".ini", key='toss1')],
                [sg.Text(t('Vimeup upload directory'), size=(30, 1), justification='left'), sg.InputText(size=(40, 1), key='upload_directory', default_text=upload_directory_prefill, tooltip=t("This is the directory Vimeup will first open when you upload a video.")),sg.FolderBrowse(button_text=t("Choose Directory"), initial_folder="./", key='toss2')],
                [sg.Text(t('Vimeup download directory'), size=(30, 1)), sg.InputText(size=(40, 1), key='download_directory', default_text=download_directory_prefill, tooltip=t("This is the directory Vimeup will first open when you a download video.")),sg.FolderBrowse(button_text=t("Choose Directory"), initial_folder="./", key='toss3')],
                [sg.Button(t('OK'), key='ok'), sg.Button(t('Cancel'), key='cancel')]]
    # Create the Window
    window = sg.Window(t('Vimeup - Local Configuration Setup'), layout, font=["Arial", 12])
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'ok':
            local_config_write(**values)
            break
        if event == sg.WIN_CLOSED or event == 'cancel':  # if user closes window or clicks cancel
            break
    window.close()


def local_config_write(shared_configuration_file, upload_directory, download_directory, toss1, toss2, toss3):
    """Writes the private configuration to the private configuration file."""
    localconfig['shared_configuration_file'] = shared_configuration_file
    localconfig['upload_directory'] = upload_directory
    localconfig['download_directory'] = download_directory
    localconfig.write()


# ###### MAIN PROGRAM #######
# Multilingual Support
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('vimeup', localedir, fallback=True)
t = translate.gettext  # t is for translate
# Private Configuration check and setup
private_config = './private.ini'
privateconfig = ConfigObj(private_config, configspec='./privatespec.ini')
validator = Validator()
check_private_config()
# Local Configuration check and setup
local_config = './local.ini'
localconfig = ConfigObj(local_config, configspec='./localspec.ini')
check_local_config()