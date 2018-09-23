from enum import Enum, unique


class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""

    def __init__(self, app_name, question, answers):
        self.__app_id = -1
        self.__app_name = app_name
        self.__questionnaire = {question: answers}

    def update_questionnaire(self, question, answers):
        self.__questionnaire.update({question: answers})

    def get_answers(self, question):
        return self.__questionnaire.get(question)

    @property
    def app_name(self):
        return self.__app_name


class Question:
    """The question"""

    cache_value = {}        # { app_question_str: question }
    cache_section = {}      # { app_section: question }
    cache_tag = {}          # { app_tag: question }

    def __init__(self, q_id, q_value, q_type, q_section, q_tag, is_nullable=False):
        self.__q_id = q_id
        self.__value = q_value
        self.__type = q_type
        self.__section = q_section
        self.__tag = q_tag
        self.__is_nullable = is_nullable

    @staticmethod
    def get_question(question_value):
        return Question.cache_value.get(question_value)


class Answer:
    """The answer"""

    answer_cache = {}       # { app_answer_str: list( answer ) }

    def __init__(self, ans_id, ans_value):
        self.__a_id = ans_id
        self.__answer = ans_value

    @staticmethod
    def get_answer(answer_value):
        return Answer.answer_cache.get(answer_value)


@unique
class QuestionType(Enum):
    LARGE_TEXT = 1
    CHECKBOX = 2
    RADIO = 3


