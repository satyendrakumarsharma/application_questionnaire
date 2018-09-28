from enum import Enum, unique


class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""

    def __init__(self, app_name):
        self.__app_id = -1
        self.__app_name = app_name
        self.questionnaire = {}

    def update_questionnaire(self, question, answers):
        self.questionnaire.update({question: answers})

    def get_answers(self, question):
        return self.questionnaire.get(question)

    @property
    def app_name(self):
        return self.__app_name


class Question:
    """The question"""

    cache_value = {}        # { app_question_str: question }
    cache_section = {}      # { app_section: question }
    cache_tag = {}          # { app_tag: question }

    cache_answers = {}      # { question: list( all answers ) }

    def __init__(self, q_id, q_value, q_type, q_section, q_tag, is_nullable=False):
        self.q_id = q_id
        self.q_value = q_value
        self.q_type = q_type
        self.q_section = q_section
        self.q_tag = q_tag
        self.is_nullable = is_nullable
        self.all_answers = []

    @staticmethod
    def get_question_by_value(question_value):
        return Question.cache_value.get(question_value)

    @staticmethod
    def get_all_answers_by_question(question):
        return Question.cache_answers.get(question)


class Answer:
    """The answer"""

    cache_value = {}       # { app_answer_str: list( answer ) }

    def __init__(self, ans_id, ans_value, ans_tag):
        self.a_id = ans_id
        self.answer = ans_value
        self.tag = ans_tag

    @staticmethod
    def get_answer(answer_value):
        return Answer.cache_value.get(answer_value)


@unique
class QuestionType(Enum):
    LARGE_TEXT = 1
    CHECKBOX = 2
    RADIO = 3


