import PySimpleGUI as sg
from Supporting_Functions import *

def sports_window():
    """
    The window which opens when user wants to talk about sports
    :return: nothing
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text('You need help with Sport Activities!')],
              [sg.Text('What do you need help with?'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Sport Activites', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
