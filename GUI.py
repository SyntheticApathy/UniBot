import PySimpleGUI as sg
from Supporting_Functions import *


def greetings_window():
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside the window.
    layout = [[sg.Text('Welcome to UniBot!')],
              [sg.Text('What do you need help with?'), sg.InputText(key='-USER_INPUT-')],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('UniBot', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # If user closes window or presses 'Cancel', program terminates.
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            exit(0)

        # When user clicks 'Ok'
        if event == 'Ok':

            # Checks to see if the input is empty, if it is then it gives a popup to remind to fill in the input
            if values['-USER_INPUT-'] == "":
                sg.popup_ok("Input needs to not be empty!", keep_on_top=True, no_titlebar=True, text_color='Red')
                window.close()
                greetings_window()

            # Closes current window to redirect to correct window after.
            window.close()

            # Decides the topic which the user wants to talk about
            topic = process_input(values['-USER_INPUT-'])

            # after parsing, direct to correct window
            if topic == 'sport':
                sports_window()
            elif topic == 'studying':
                studying_window()
            elif topic == 'social':
                social_window()
            elif topic == 'oops':
                explicit_ask_window()

    # Should be unreachable, but will close window in case of bug.
    window.close()
    exit(-1)


def explicit_ask_window():
    """
    The window that opens when the bot cannot parse what the user wants to talk about
    :return: nothing
    """
    # Create window and add things to it
    sg.theme('DarkAmber')
    layout = [[sg.Text('Uni bot had trouble understanding you, what do you need help with?')],
              [sg.Button('Social Activities')],
              [sg.Button('Sports')],
              [sg.Button('Studying')],
              [sg.Button('Cancel'), sg.Button('Back')]
              ]
    # Window creation
    window = sg.Window('UniBot', layout, resizable=True)

    # Event loop
    while True:
        event, values = window.read()

        # If user closes window or presses 'Cancel', program terminates.
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)

        # If user clicks back
        if event == 'Back':
            window.close()
            greetings_window()

        # If user clicks Sports / Social / Studying, directs to correct window.
        if event == 'Sports':
            window.close()
            sports_window()
        elif event == 'Studying':
            window.close()
            studying_window()
        elif event == 'Social Activities':
            window.close()
            social_window()

    # unreachable code, but just in case bug happens it closes.
    window.close()
    exit(-1)


def studying_window():
    """
    The window which opens when user wants to talk about studies
    :return: nothing
    """

    # Adding things to window
    sg.theme('DarkAmber')
    layout = [[sg.Text('You want to talk about study advice')],
              [sg.Text('What do you need help with?'), sg.InputText(key='-STUDY_SUBTOPIC-')],
              [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Back')]]

    # Create the Window
    window = sg.Window('Study Help', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # If user closes window or presses 'Cancel', program terminates.
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            exit(0)

        # If user clicks 'Ok'
        if event == 'Ok':

            # Checks to see if the input is empty, if it is then it gives a popup to remind to fill in the input
            if values['-STUDY_SUBTOPIC-'] == "":
                sg.popup_ok("Input needs to not be empty!", keep_on_top=True, no_titlebar=True, text_color='Red')
                window.close()
                studying_window()

            # Deciding what subtopic the user wants to talk about.
            subtopic = recognize_topic(values['-STUDY_SUBTOPIC-'], struggle_vocabulary, practical_info_vocabulary)

            # If user decides to talk about their struggle, directs to struggle window
            if subtopic == struggle_vocabulary:
                window.close()
                struggle_studies()

            # If user decides to ask for practical information, directs to practical info window.
            elif subtopic == practical_info_vocabulary:
                window.close()
                practical_info_studies()

        # If user clicks 'Back', redirects to last window
        if event == "Back":
            window.close()
            explicit_ask_window()

    # Unreachable code, closes window and exits program if something weird happens
    window.close()
    exit(-1)


def struggle_studies():
    """
    The window that opens if a user is having struggles with their studies
    :return: nothing
    """

    # Add things to window
    sg.theme('DarkAmber')
    layout1 = [[sg.Text('Im sorry to hear that. Would you be interested in sharing it with other students? '
                        'Participation in a study group could be very helpful.'
                        '\nWould you like me to sign you up?')],
               [sg.Button("Yes"), sg.Button("No"), sg.Button("Back"), sg.Button("Cancel")]
               ]
    # Create window
    window = sg.Window('Study Help', layout1, resizable=True)
    while True:
        event, values = window.read()

        # If user closes window or presses 'Cancel', program terminates.
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            exit(0)

        # If user wants help with their studies, they are invited to join a study group.
        if event == 'Yes':
            # Layout of new window
            sg.theme('DarkAmber')
            layout2 = [
                [sg.Text("OK! I recommend you reach out to your fellow students and try to join a study group!")],
                [sg.Text("Do you need help with anything else?")],
                [sg.Button('Yes'), sg.Button("Exit")]
            ]
            # Close old window
            window.close()
            # Create new window
            window = sg.Window('Study Help', layout2, resizable=True)

            while True:
                event, values = window.read()

                # If user closes window or presses 'Cancel', program terminates.
                if event == sg.WIN_CLOSED() or event == 'Exit':
                    window.close()
                    exit(0)

                # If user clicks 'yes', directs to greetings window
                if event == 'Yes':
                    window.close()
                    greetings_window()

                # If user does not want to join study group, bot recommends speaking with a study advisor
        if event == 'No':
            #
            sg.theme('DarkAmber')
            layout3 = [[sg.Text('Ok! I recommend you reach out to a study advisor!')],
                       [sg.Text('Do you need help with anything else?')],
                       [sg.Button('Yes'), sg.Button('Exit')]
                       ]
            # close old window
            window.close()

            # Create new window

            window = sg.Window('Study Help', layout3, resizable=True)

            while True:
                event, values = window.read()

                # If user clicks 'yes' button, then it redirects to the greetings window again for additional help.
                if event == 'Yes':
                    window.close()
                    greetings_window()

                # If user closes window or presses 'Cancel', program terminates.
                if event == 'Exit' or event == sg.WIN_CLOSED:
                    window.close()
                    exit(0)

        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            exit(0)
        # Directs user to last window
        if event == "Back":
            window.close()
            studying_window()

    # Unreachable code, closes window and exits program if something weird happens
    window.close()
    exit(-1)


def practical_info_studies():
    """
    The window that opens if the user needs practical info about their studies.
    :return: nothing
    """
    # Create window
    sg.theme('DarkAmber')
    layout = [[sg.Text('Please visit the student desk for all practical information.')],
              [sg.Button('Exit'), sg.Button('Back')]
              ]
    window = sg.Window('Study Help', layout, resizable=True)

    while True:
        event, values = window.read()

        # If user closes window or presses 'Cancel', program terminates.
        if event == 'Exit' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)
        # Directs user to last window if 'Back' is pressed
        if event == "Back":
            window.close()
            greetings_window()
    # Unreachable code, closes window and exits program if something weird happens
    window.close()
    exit(-1)


def social_window():
    """
    The window which opens when user wants to talk about social stuff
    :return:
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text('You need help with Social Activities')],
              [sg.Text('What do you need help with?'), sg.InputText(key="-SOCIAL_SUBTOPIC-")],
              [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Back')]]

    # Create the Window
    window = sg.Window('Social Activities', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        # If user closes window or presses 'Cancel', program terminates.
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            exit(0)
        # Directs user to last window if 'Back' Is pressed
        if event == 'Back':
            window.close()
            explicit_ask_window()

        if event == 'Ok':

            # Checks to see if the input is empty, if it is then it gives a popup to remind to fill in the input
            if values['-SOCIAL_SUBTOPIC-'] == "":
                sg.popup_ok("Input needs to not be empty!", keep_on_top=True, no_titlebar=True, text_color='Red')
                window.close()
                social_window()


def sports_window():
    """
    The window which opens when user wants to talk about sports
    :return: nothing
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside the window.
    layout = [[sg.Text('You need help with Sport Activities!')],
              [sg.Text('What exactly do you need help with?'), sg.InputText(key="-SPORT_SUBTOPIC-")],
              [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Back')]]

    # Create the Window
    window = sg.Window('Sport Activities', layout, resizable=True)
    # Event Loop
    while True:
        event, values = window.read()

        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            exit(0)
        if event == 'Back':
            window.close()
            explicit_ask_window()

        if event == "Ok":

            # Checks to see if the input is empty, if it is then it gives a popup to remind to fill in the input
            if values['-SPORT_SUBTOPIC-'] == "":
                sg.popup_ok("Input needs to not be empty!", keep_on_top=True, no_titlebar=True, text_color='Red')
                window.close()
                sports_window()
            # Decide what subtopic the user wants to talk about
            subtopic = recognize_topic(values['-SPORT_SUBTOPIC-'], new_sport_vocabulary, university_sport_vocabulary,
                                       current_sport_vocabulary)

            # If user wants to ask about a specific sport
            if subtopic == university_sport_vocabulary or subtopic == current_sport_vocabulary:
                window.close()
                university_sports_window()
            # If user wants to look for a new sport
            if subtopic == new_sport_vocabulary:
                window.close()
                new_sport_window()


def university_sports_window():
    """
    The window which opens when user wants to talk about current university sports
    :return: nothing
    """
    sg.theme('DarkAmber')  # Add colour to window

    # Everything inside the window:
    layout = [[sg.Text('You want to talk about a specific university sport.')],
              [sg.Text('The sports the university offers are:')],
              [sg.Text(read_from_csv()[0])],
              [sg.Text("Do you have a question about one of these sports?")],
              [sg.Button("Yes"), sg.Button("No"), sg.Button('Cancel')]
              ]
    window = sg.Window('University Sports', layout, resizable=True)

    # Event loop
    while True:
        event, values = window.read()

        if event == "Yes":
            window.close()
            current_sport_contact_window()
        if event == "No":
            window.close()
            new_sport_window()

        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            exit(0)


def current_sport_contact_window():
    """
            The window which opens when user wants to talk about a current university sport
            :return: nothing
            """
    sg.theme('DarkAmber')  # Add colour to window

    # Everything inside the window:
    layout = [[sg.Text('If you have a question about any one of the currently available sports, please contact the '
                       'University Sports Centre')],
              [sg.Text('You can view their website at: https://sportcentrumvu.nl/en/')],
              [sg.Text("Do you have any other questions?")],
              [sg.Button('Yes'), sg.Button("No"), sg.Button('Cancel')]
              ]
    # Create window
    window = sg.Window('University Sports', layout, resizable=True)
    # Event loop
    while True:
        event, values = window.read()

        # If user has more questions redirects to starting window
        if event == 'Yes':
            window.close()
            greetings_window()
            # If user has no more questions then closes window and exits program
        if event == 'No':
            window.close()
            exit(0)
        # If user cancels or closes window.
        if event == "Cancel" or event == sg.WIN_CLOSED:
            window.close()
            exit(0)


def new_sport_window():
    """
        The window which opens when user wants to talk about new university sports
        :return: nothing
        """
    sg.theme('DarkAmber')  # Add colour to window

    # Everything inside the window:
    layout = [[sg.Text('You want to talk about university sports!')],
              [sg.Text('The sports the university offers are:')],
              [sg.Text(university_sport_vocabulary)],
              [sg.Button('Ok')]
              ]
    window = sg.Window('University Sports', layout, resizable=True)

    # Event loop
    while True:
        event, values = window.read()


greetings_window()
