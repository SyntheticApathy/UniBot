import PySimpleGUI as sg
from Supporting_Functions import *

def social_window():
    """
    The window which opens when user wants to talk about social stuff
    :return:
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text('You need help with Social Activities')],
              [sg.Text('What do you need help with?'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Social Activities', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()