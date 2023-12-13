import PySimpleGUI as sg
from Supporting_Functions import *


def studying_window():
    """
    The window which opens when user wants to talk about studies
    :return: nothing
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text('You want to talk about study advice')],
              [sg.Text('What do you need help with?'), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Study Help', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == 'Ok':
            # Deciding what subtopic the user wants to talk about.
            subtopic = recognize_topic(values[0], struggle_vocabulary, practical_info_vocabulary)
            print('you reached here')
            # If user decides to talk about their struggle.
            if subtopic == struggle_vocabulary:
                print('test')
                window.close()
                struggle_studies()

            # If user decides to ask for practical information.
            elif subtopic == practical_info_vocabulary:
                window.close()
                practical_info()

        if event == "Cancel":
            window.close()
            exit(0)

    # Unrechable code, closes window and exits program if something weird happens
    window.close()
    exit(-1)


def struggle_studies():
    """
    The window that opens if a user is having struggles with their studies
    :return: nothing
    """
    layout1 = [[sg.Text('Im sorry to hear that. Would you be interested in sharing it with other students? '
                        'Participation in a study group could be very helpful.'
                        '\nWould you like me to sign you up?')],
               [sg.Button("Yes"), sg.Button("No"), sg.Button("Back"), sg.Button("Cancel")]
               ]
    window = sg.Window('Study Help', layout1, resizable=True)
    while True:
        event, values = window.read()

        # If user wants help with their studies, they are invited to join a study group.
        if event == 'Yes':
            # todo change maybe the text for the layout, I used a random group number and time.

            layout2 = [[sg.Text("OK! I've signed you up for study group number 3, Wednesday at 18:00")],
                       [sg.Text("Do you need help with anything else?")],
                       [sg.Button('Yes'),sg.Button("Exit")]
                       ]
            window.close()
            window = sg.Window('Study Help', layout2, resizable=True)

            while True:
                event, values = window.read()

                if event == 'Exit':
                    window.close()
                    exit(0)
                if event == 'Yes':
                    window.close()
                    greetings_window()


        if event == 'No':
            window.close()
            studying_window()
        if event == "Back":
            window.close()
            studying_window()
        if event == "Cancel":
            window.close()
            studying_window()

    # Unrechable code, closes window and exits program if something weird happens
    window.close()
    exit(-1)


def practical_info():
    """
    The window that opens if the user needs practical info about their studies.
    :return: nothing
    """
    layout = [[sg.Text('Please Visit the student desk for all practical information.')],
              [sg.Button('Exit')]
              ]
    window = sg.Window('Study Help', layout, resizable=True)

    while True:
        event, values = window.read()

        if event == 'Exit':
            window.close()
            exit(0)

    # Unrechable code, closes window and exits program if something weird happens
    window.close()
    exit(-1)

