class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""
    def __init__(self):
        self.__app_id = -1
        self.__app_name = ''
        self.__questionnaire = {}


class Question:
    """The questions"""
    def __init__(self):
        self.__q_id = -1
        self.__question = ''
        self.__section = -0.0


class Answer:
    """The answers"""
    def __init__(self):
        self.__a_id = -1
        self.__answer = ''

