class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""

    def __init__(self, app_name, question, answers):
        self.__app_id = -1
        self.__app_name = app_name
        self.__questionnaire = {question: answers}

    def update_questionnaire(self, question, answers):
        self.__questionnaire.update({question: answers})

    @property
    def app_name(self):
        return self.__app_name


class Question:
    """The questions"""

    q_id = 0
    question_cache = {}

    def __init__(self, question, section):
        self.__q_id = Question.q_id
        Question.q_id += 1
        self.__question = question
        self.__section = section


class Answer:
    """The answers"""

    a_id = 0
    answer_cache = {}

    def __init__(self, answer):
        self.__a_id = Answer.a_id
        Answer.a_id += 1
        self.__answer = answer


