from enum import Enum, unique
from typing import List


class Answer:
    """The answer"""

    __ans_id = 0
    __cache_value = {}       # { app_answer_str: list( answer ) }

    def __init__(self, ans_value, ans_tag):
        self.a_id = Answer.__gen_ans_id()
        self.value = ans_value
        self.tag = ans_tag
        Answer.cache_answer_by_value(self.value, self)

    @staticmethod
    def cache_answer_by_value(answer_value, answer):
        return Answer.__cache_value.update({answer_value: answer})

    @staticmethod
    def get_answer_by_value(answer_value):
        return Answer.__cache_value.get(answer_value)

    @staticmethod
    def __gen_ans_id():
        Answer.__ans_id += 1
        return Answer.__ans_id


@unique
class QuestionType(Enum):
    LARGE_TEXT = 1
    CHECKBOX = 2
    RADIO = 3


class Question:
    """The question"""

    __cache_value = {}      # { app_question_str: question }
    cache_section = {}      # { app_section: question }
    cache_tag = {}          # { app_tag: question }

    cache_answers = {}      # { question: list( all answers ) }

    def __init__(self, q_id: int, q_value: str, q_type: QuestionType, q_section, q_tag: str, is_nullable=False):
        self.q_id = q_id
        self.q_value = q_value
        self.q_type = q_type
        self.q_section = q_section
        self.q_tag = q_tag
        self.is_nullable = is_nullable
        self.all_answer_options = []
        Question.cache_question_by_value(self.q_value, self)

    @staticmethod
    def cache_question_by_value(question_value: str, question):
        return Question.__cache_value.update({question_value: question})

    @staticmethod
    def get_question_by_value(question_value: str):
        return Question.__cache_value.get(question_value)

    @staticmethod
    def cache_items():
        """This method returns all the question-value:Question items from the cache."""
        return Question.__cache_value.items()

    @staticmethod
    def cache_values():
        """This method returns all the 'Question' values from the cache."""
        return Question.__cache_value.values()

    @staticmethod
    def get_all_answers_of_question(question) -> List[Answer]:
        return question.all_answer_options


class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""

    app_cache = {}

    def __init__(self, app_name: str):
        self.__app_id = -1
        self.__app_name = app_name
        self.__questionnaire = {}     # { question : answers_by_user }
        ApplicationData.app_cache.update({app_name: self})

    def update_questionnaire(self, question: Question, answers: Answer):
        self.__questionnaire.update({question: answers})

    def get_answers(self, question: Question) -> Answer:
        return self.__questionnaire.get(question)

    @property
    def app_name(self):
        return self.__app_name
