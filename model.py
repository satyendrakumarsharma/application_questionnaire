class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""

    def __init__(self, question, answers):
        self.__app_id = -1
        self.__app_name = ''
        self.__questionnaire.update({question: answers})


class Question:
    """The questions"""

    question_cache = {}

    def __init__(self, q_id, question, section):
        self.__q_id = q_id
        self.__question = question
        self.__section = section


class Answer:
    """The answers"""

    answer_cache = {}

    def __init__(self, a_id, answer):
        self.__a_id = a_id
        self.__answer = answer


