from datetime import datetime

import PySimpleGUI as sg
from Supporting_Functions import *
from Supporting_Functions import Event


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
            else:
                sg.popup_ok("I'm having trouble understanding you, please try again!", keep_on_top=True,
                            no_titlebar=True)
                window.close()
                studying_window()

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
    The window which opens when user wants to talk about social activites
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
            greetings_window()

        if event == 'Ok':

            # Checks to see if the input is empty, if it is then it gives a popup to remind to fill in the input
            if values['-SOCIAL_SUBTOPIC-'] == "":
                sg.popup_ok("Input needs to not be empty!", keep_on_top=True, no_titlebar=True, text_color='Red')
                window.close()
                social_window()

            subtopic = recognize_topic(values["-SOCIAL_SUBTOPIC-"], social_vocabulary, new_vocabulary,
                                       join_social_vocabulary)

            if subtopic == new_vocabulary:
                window.close()
                upcoming_social_activity_window()
            elif subtopic == join_social_vocabulary:
                window.close()
                join_association_window()
            elif subtopic == social_vocabulary:
                window.close()
                explicit_social_window()
            else:
                window.close()
                explicit_social_window()


def explicit_social_window():
    """
    The window which appears when the user needs to explicitly state what social activity they want to do.
    :return: This function returns nothing
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text("I'm sorry, I'm having trouble understanding you.")],
              [sg.Text('What do you need help with?'), sg.Button('Joining a new association'), sg.Button('Upcoming '
                                                                                                         'events')],
              [sg.Button('Cancel'), sg.Button('Back')]]

    # Create the Window
    window = sg.Window('Social Activities', layout, resizable=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Joining a new association':
            window.close()
            join_association_window()
        if event == 'Upcoming events':
            window.close()
            upcoming_social_activity_window()
        if event == 'Back':
            window.close()
            social_window()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)


def upcoming_social_activity_window():
    """
    This window appears when the user wants to know about the upcoming social events.
    :return: This function returns nothing.
    """
    # Get the upcoming events
    upcoming_event_list: List[Event] = upcoming_events(datetime.now().day, datetime.now().month)

    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text(" The upcoming Events are:")],
              [sg.Text(upcoming_event_list[0]), sg.Text(upcoming_event_list[1]), sg.Text(upcoming_event_list[2])],
              [sg.Text('Do you need help with anything else?')],
              [sg.Button('Yes'), sg.Button('No'), sg.Button('Cancel')]
              ]

    # Create the Window
    window = sg.Window('Social Activities', layout, resizable=True)
    while True:
        event, values = window.read()

        if event == 'Cancel' or event == 'No' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)
        if event == 'Yes':
            window.close()
            greetings_window()


def join_association_window():
    """
        This function appears when the user wants to join an association.
    :return: This function returns nothing.
    """
    sg.theme('DarkAmber')  # Add colour to window

    # All the stuff inside your window.
    layout = [[sg.Text("It seems as if you want to join an association.")],
              [sg.Text('What type of association would suit you best?')],
              [sg.Checkbox('International')],
              [sg.Checkbox('Artistic')],
              [sg.Checkbox('Debate')],
              [sg.Checkbox('Scientific')],
              [sg.Checkbox('Political')],
              [sg.Checkbox('Altruistic')],
              [sg.Button('Submit')],
              [sg.Button('Cancel'), sg.Button('Back')]]

    # Create the Window
    window = sg.Window('Social Activities', layout, resizable=True)

    while True:
        event, values = window.read()

        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)

        if event == 'Back':
            window.close()
            social_window()

        if event == 'Submit':
            selected_preferences = [key for key, value in values.items() if value]
            recommended_association = recommend_association(selected_preferences)
            sg.popup_ok(f"Based on your preferences, we recommend you join: {recommended_association}")


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
            subtopic = recognize_topic(values['-SPORT_SUBTOPIC-'], new_vocabulary, university_sport_vocabulary,
                                       current_sport_vocabulary)

            # If user wants to ask about a specific sport
            if subtopic == university_sport_vocabulary or subtopic == current_sport_vocabulary:
                window.close()
                university_sports_window()
            # If user wants to look for a new sport
            if subtopic == new_vocabulary:
                window.close()
                new_sport_window()
            else:
                sg.popup_ok("I'm having trouble understanding you, please try again!", keep_on_top=True,
                            no_titlebar=True)
                window.close()
                sports_window()


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
    layout = [[sg.Text('You want to talk about a new sport.')],
              [sg.Text('What type of sport are you looking for?')],
              [sg.Button('Team Sports'), sg.Button('Ballgames'), sg.Button('Cardio'), sg.Button('Strength Training')],
              [sg.Button('Cancel')]
              ]
    window = sg.Window('University Sports', layout, resizable=True)

    # Event loop
    while True:
        event, values = window.read()

        if event == "Team Sports":
            window.close()
            chose_new_sport("Team Sports", 0)
        elif event == 'Ballgames':
            window.close()
            chose_new_sport("Ballgames", 0)
        elif event == 'Cardio':
            window.close()
            chose_new_sport("Cardio", 0)
        elif event == 'Strength Training':
            window.close()
            chose_new_sport("Strength Training", 0)

        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)


def chose_new_sport(sport_type: str, index: int):
    """

  :param sport_type: the type of sport the user is looking for
  :param index: the index of the list of potential sports
  :return: This function returns nothing
  """

    sg.theme('DarkAmber')  # Add colour to window

    if index > len(choose_sport(sport_type)):
        sorry_window()

    sport_option: str = choose_sport(sport_type)[index]

    # Everything inside the window:
    layout = [[sg.Text(f'It looks like you want to take a {sport_type} sport!')],
              [sg.Text("Is this sport something you'd be interested in? "), sg.Text(sport_option)],
              [sg.Button('Yes'), sg.Button('No')],
              [sg.Button('Cancel')]
              ]
    window = sg.Window('University Sports', layout, resizable=True)

    while True:
        event, values = window.read()
        if event == 'No':
            index += 1
            window.close()
            chose_new_sport(sport_type, index)
        if event == 'Yes':
            window.close()
            chosen_sport_window(sport_option)

        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)


def sorry_window():
    """
    The window which displays if a user can't find a new sport that they are interested in.
    :param type: The type of sport the user is looking for
    :return: This function returns nothing.
    """

    sg.theme('DarkAmber')  # Add colour to window

    # Everything inside the window:
    layout = [[sg.Text('Unfortunately, I was not able to find a sport that you would enjoy.')],
              [sg.Text('Would you like to see a list of sports that the University offers?')],
              [sg.Button('Yes'), sg.Button('No'), sg.Button('Cancel')]
              ]
    window = sg.Window('University Sports', layout, resizable=True)

    while True:
        event, values = window.read()

        if event == "Yes":
            window.close()
            university_sports_window()
        if event == "No":
            window.close()
            greetings_window()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)


def chosen_sport_window(sport_option: str):
    """
    The window which displays if the user has chosen a sport.
    :param sport_option: The sport which the user has chosen to take
    :return: This function returns nothing
 """
    sg.theme('DarkAmber')  # Add colour to window

    # Everything inside the window:
    layout = [[sg.Text(f'You have chosen {sport_option}')],
              [sg.Text(f'For more information about {sport_option}, visit https://sportcentrumvu.nl/en/')],
              [sg.Text('Do you need help with anything else?')],
              [sg.Button('Yes'), sg.Button('No')]
              ]
    window = sg.Window('University Sports', layout, resizable=True)

    while True:
        event, values = window.read()

        if event == 'No' or event == sg.WIN_CLOSED:
            window.close()
            exit(0)
        if event == 'Yes':
            window.close()
            greetings_window()


greetings_window()
