import csv
import re
from typing import *


class Event:
    """
        :param: name: the name of the event
        :param: day: the day of the event in numerical value
        :param: month: the month of the event in a string
    """

    def __init__(self, name: str, day: int, month: str):
        self.name = name
        self.day = day
        self.month = self.calculate_month(month)

    def __str__(self):
        return f'{self.name}: {self.day}, {self.month}'

    def __repr__(self):
        return f'{self.name}: {self.day}, {self.month}'

    def calculate_month(self, month) -> int:
        """
        This method returns the corresponding integer for the month.
        :param month: The month given when creating the object.
        :return: An integer depending on the corresponding month.
        """
        months: List[str] = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

        return months.index(month) + 1


def make_plural(vocabulary_list):
    transformed_list = []
    for word in vocabulary_list:
        transformed_list.append(word)
        word = word + "s"
        transformed_list.append(word)
    return transformed_list


def process_input(userInput: str) -> str:
    """
    This function takes the input from the GUI and reads it, then decides if the user wants to talk about
        studying / sports / social activities.

    :param userInput: the input from the user
    :return str: this functions returns a string, which tells us what topic
                the user wants to talk about
                studying == studying
                sport == sports
                social == social activities
                oops == the bot cannot parse
    """
    topic = recognize_topic(userInput, sports_vocabulary, studying_vocabulary, social_vocabulary, greetings_vocabulary)

    if topic == studying_vocabulary:
        return 'studying'
    elif topic == social_vocabulary:
        return 'social'
    elif topic == sports_vocabulary:
        return 'sport'
    elif not topic:
        return 'oops'

    # if chatbot cannot parse what the user wants it should then ask
    # explicitly
    return 'oops'


def read_from_csv() -> (List[str], List[str], List[Event]):
    """
        This function reads from the csv file and returns all the information
    :return: This function returns a tuple of list of strings consisting of all the sports, associations, and events
    """
    # Return values, initialized and empty for now
    sports_list: List[str] = list()
    associations: List[str] = list()
    events: List[str] = list()

    # Read from csv, add to lists as needed.
    with open('unilife.csv', newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        line = 0
        for row in csvreader:
            sports_list.append(row[0])
            associations.append(row[1])
            events.append(row[2])
            line += 1

    # Parse events list from csv to a List of Event objects.
    events_list = parse_events(events)

    # deletes the first element of both lists as this is the identifier.
    del sports_list[0]
    del associations[0]
    # Return tuple of lists.
    return sports_list, associations, events_list


def parse_events(events: List[str]) -> List[Event]:
    """
        This function takes a list of strings and parses it to make events objects.
    :param events:  a list of the events from the csv file.
    :return: This function returns a list of "Event" objects consisting of the name and date of the event.
    """
    # Initialize return value
    list_events: List[Event] = list()

    for index, event_line in enumerate(events):
        # Skip over the first value, this is the string "events" in the csv file.
        if index == 0:
            continue
        # As the form of the events is atypical, use regex to parse event
        match = re.match(r"(.+?)\s*\((\d+)\s*([a-zA-Z]+)\)", event_line)
        if match:
            name_of_event, day, month = match.groups()

            # After parsing, create a new Event object and add to list.
            list_events.append(Event(name_of_event.strip(), int(day), month.strip()))

    return list_events


def choose_sport(sport_type: str) -> List[str]:
    """
    This function decides what sport to offer the user.
    :param sport_type: The option of type of sport
    :return: This function returns a sport depending on what the user choose before.
    """

    team_sports: List[str] = ['Basketball', 'Football', 'Waterpolo']
    ballgames: List[str] = ["Basketball", "tennis", "Football", "Waterpolo"]
    cardio: List[str] = ["Basketball", "Aikido", "Swimming", "Football", "Zumba", "Karate", "Waterpolo", "Yoga"]
    strength_training: List[str] = ["Aikido", "Swimming", "Zumba", "Karate", "Yoga"]

    if sport_type == 'Team Sports':
        return team_sports
    elif sport_type == 'Ballgames':
        return ballgames
    elif sport_type == 'Cardio':
        return cardio
    elif sport_type == "Strength Training":
        return strength_training


def upcoming_events(day: int, month: int) -> List[Event]:
    """
    This function checks what the next three events will be according to the given day and month
    :param day: the day we want to check the closest future event of
    :param month: the month we want to check the closest future event of.
    :return: this function returns 3 events
    """
    # A list of all the events
    event_list = read_from_csv()[2]
    # Sort the events by month
    sorted_event_list = sorted(event_list, key=lambda event_month: event_month.month)
    upcoming_events_list = []
    found_events = 0

    for event in sorted_event_list:
        if (month < event.month) or (month == event.month and day < event.day):
            upcoming_events_list.append(event)
            found_events += 1

        # Check if we have found the required number of events
        if found_events == 3:
            break

    # If we haven't found enough events, loop around the sorted list
    if found_events < 3:
        for event in sorted_event_list:
            upcoming_events_list.append(event)
            found_events += 1

            # Check if we have found the required number of events
            if found_events == 3:
                break

    return upcoming_events_list


def recommend_association(preferences):
    """
    This function maps the association to the preferences of the user and returns the association which the user will
    like.
    :param preferences: The preferences of the user
    :return: this function returns the association which is
    most like the preferences of the user.
    """
    # Map associations to their respective categories
    association_categories = {
        'Poetry Pals': ['Artistic'],
        'Debate Club': ['Debate'],
        'Science Society': ['Scientific'],
        'Painting and Pottery': ['Artistic'],
        'Language Club': ['International'],
        'International Students Society': ['International'],
        'Students for Sustainability': ['Political'],
        'Animal Shelter Volunteers': ['Altruistic'],
        'Bunch of Backpackers': ['International']
    }

    # Filter associations based on preferences
    filtered_associations = [association for association, categories in association_categories.items() if
                             all(category in preferences for category in categories)]

    # If no associations match the preferences, return a default recommendation
    if not filtered_associations:
        return "No specific recommendation. Explore all associations!"

    # Return the first matching association as the recommendation
    return filtered_associations[0]


# determining the vocabulary associated with each topic and consequent subtopic (contained in lists)

###
sports_vocabulary_pre_plural = ["sport", "football", "game", "play", "tournament", "competition", "event"]
sports_vocabulary = make_plural(sports_vocabulary_pre_plural)
university_sport_vocabulary = read_from_csv()[0]
current_sport_vocabulary = ["current"]
new_vocabulary = ["new", "try", "looking", "for", "upcoming"]
###

###
studying_vocabulary = ["studying", "studies", "study", "lecture", "lectures", "classes", "class"]
struggle_vocabulary = ["struggle", "struggling", "problem", "difficulty", "difficulties", "issue", ]
struggle_vocabulary = make_plural(struggle_vocabulary)
practical_info_vocabulary = ["info", "information", "guide"]
###


###
social_vocabulary = ["social", "activities", "club", "event", "group", "association"]
join_social_vocabulary = ["join", "participate"]
###


###
greetings_vocabulary = ["hi", "hello", "yo", "hey"]


###


def recognize_topic(text,
                    *topic_lists):  # the star allows us to pass multiple arguments of the same type and combine them
    # into a list (of lists in this case)

    # the list that helps to keep track of the frequency of the words associated with each consecutive topic
    topic_counts = [0] * len(topic_lists)

    # divides the user's input into individual words
    user_words = text.lower().split()

    # counts word matches for each topic with the topic lists
    for word in user_words:
        for i, topic_words in enumerate(
                topic_lists):  # enumerate function helps us to access the index of each entry (in this case list of
            # thematic words) and their items simultaneously
            if word in topic_words:
                topic_counts[i] += 1

    # the topic with the highest amount of matches with user's statement
    max_count = max(topic_counts)
    if max_count == 0:
        return None
    else:
        max_index = [i for i, count in enumerate(topic_counts) if count == max_count]
        if len(max_index) == 1:
            return topic_lists[max_index[0]]
        else:
            return None
