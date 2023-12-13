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
        self.month = month

    def __str__(self):
        return f'{self.name}: {self.day}, {self.month}'
    def __repr__(self):
        return f'{self.name}: {self.day}, {self.month}'



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
    sports_list: List[str] = list()
    associations: List[str] = list()
    events: List[str] = list()

    with open('unilife.csv', newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        line = 0
        for row in csvreader:
            sports_list.append(row[0])
            associations.append(row[1])
            events.append(row[2])
            line += 1

    events_list = parse_events(events)

    return (sports_list, associations, events_list)

def parse_events(events: List[str]) ->List[Event]:
    """
        This function takes a list of strings and parses it to make events objects.
    :param events:  a list of the events from the csv file.
    :return: This function returns a list of "Event" objects consisting of the name and date of the event.
    """
    list_events: List[Event] = list()
    for index, event_line in enumerate(events):
        if index == 0:
            continue
        match = re.match(r"(.+?)\s*\((\d+)\s*([a-zA-Z]+)\)", event_line)

        if match:
            name_of_event, day, month = match.groups()
            list_events.append( Event(name_of_event.strip(), int(day), month.strip()))

    return list_events




# determining the vocabulary associated with each topic and consequent subtopic (contained in lists)

###
sports_vocabulary_pre_plural = ["sport", "football", "game", "play", "tournament", "competition", "event"]
sports_vocabulary = make_plural(sports_vocabulary_pre_plural)
university_sport_vocabulary = ["aikido", "football", "soccer", "basketball", "tennis", "swimming", "zumba", "karate",
                               "yoga", "waterpolo"]
new_sport_vocabulary = ["new", "try", "looking", "for"]
###


schedule = """aikido,Poetry Pals,New Year's Party (13 Jan),basketball,Debate Club,Valentine's Dinner,(14 Feb),tennis,Science Society,Carnival Night,(1 March),swimming,Painting and Pottery,Karaoke Night,(18 April),football,Language Club,Kayaking Trip,(5 May)
Zumba, International Students Society, Seaside Picnic (15 Sep)
karate, Students for Sustainability, Halloween Party (31 Oct)
yoga, Animal Shelter Volunteers, Thanksgiving Jamboree (26 Nov)
waterpolo, Bunch of Backpackers, Christmas Dinner (18 Dec)"""

###
studying_vocabulary = ["studying", "studies", "study", "lecture", "lectures", "classes", "class"]
struggle_vocabulary = ["struggle", "struggling", "problem", "difficulty", "difficulties", "issue", ]
struggle_vocabulary = make_plural(struggle_vocabulary)
practical_info_vocabulary = ["info", "information", "guide"]
###


###
social_vocabulary = ["social", "activities", "club", "event", "group", "association"]
###


###
greetings_vocabulary = ["hi", "hello", "yo", "hey"]


###


def recognize_topic(text,
                    *topic_lists):  # the star allows us to pass multiple arguments of the same type and combine them into a list (of lists in this case)

    # the list that helps to keep track of the frequency of the words associated with each consecutive topic
    topic_counts = [0] * len(topic_lists)

    # divides the user's input into individual words
    user_words = text.lower().split()

    # counts word matches for each topic with the topic lists
    for word in user_words:
        for i, topic_words in enumerate(
                topic_lists):  # enumerate function helps us to access the index of each entry (in this case list of thematic words) and their items simultaneously
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


# Legacy code, Not needed
def studying(user_line: str):
    # subtopic variable helps to investigate the deeper context of the text after already narrowing the topic by detecting it as studying
    subtopic = recognize_topic(user_line, struggle_vocabulary, practical_info_vocabulary)

    if subtopic == struggle_vocabulary:
        print(
            "UniBot: I'm sorry to hear that. Would you be interested in sharing it with other students? Participation in a study group could be very helpful.\nWould you like me to sign you up?")

        decision = input()
        decision = decision.lower()

        while decision not in ["yes", "no"]:
            print("UniBot: Please indicate your choice through an answer of yes or no.")
            decision = input()
            decision = decision.lower()

        if decision == "no":
            print("Unibot: I suggest making an appointment with a student advisor.")

        elif decision == "yes":
            print("UniBot: I've signed you up for the study group, I hope ")

    elif subtopic == practical_info_vocabulary:
        print("UniBot: Please visit the Study Desk for all practical information")
    elif not subtopic:
        print("")


# Legacy code, Not needed
def sports(user_line):
    subtopic = recognize_topic(user_line, university_sport_vocabulary, new_sport_vocabulary)
    if subtopic == university_sport_vocabulary:
        print("This sport is available ")


# Legacy Code, Not Needed
def social_activities(user_line):
    subtopic = recognize_topic()
