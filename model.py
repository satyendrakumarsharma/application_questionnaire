from enum import Enum, unique
from typing import List


class Answer:
    """The answer"""

    _ans_id = 0
    _cache_value = {}  # { app_answer_str: list( answer ) }

    def __init__(self, ans_value, ans_tag):
        self.a_id = Answer._gen_ans_id()
        self.value = ans_value
        self.tag = ans_tag
        Answer.cache_answer_by_value(self.value, self)

    @staticmethod
    def cache_answer_by_value(answer_value, answer):
        return Answer._cache_value.update({answer_value: answer})

    @staticmethod
    def get_answer_by_value(answer_value):
        return Answer._cache_value.get(answer_value)

    @staticmethod
    def _gen_ans_id():
        Answer._ans_id += 1
        return Answer._ans_id

    def __repr__(self):
        return repr(self.value)


@unique
class QuestionType(Enum):
    LARGE_TEXT = 1
    CHECKBOX = 2
    RADIO = 3


class Question:
    """The question"""

    _cache_value = {}  # { app_question_str: question }

    def __init__(self, q_id: int, q_value: str, q_type: QuestionType, q_tag: str, q_default: str,
                 is_nullable=False):
        self.q_id = q_id
        self.q_value = q_value
        self.q_type = q_type
        self.q_tag = q_tag
        self.q_default = q_default
        self.is_nullable = is_nullable
        self.all_answer_options = []
        Question.cache_question_by_value(self.q_value, self)

    @staticmethod
    def cache_question_by_value(question_value: str, question):
        return Question._cache_value.update({question_value: question})

    @staticmethod
    def get_question_by_value(question_value: str):
        return Question._cache_value.get(question_value)

    @staticmethod
    def cache_items():
        """This method returns all the question-value:Question items from the cache."""
        return Question._cache_value.items()

    @staticmethod
    def cache_values():
        """This method returns all the 'Question' values from the cache."""
        return Question._cache_value.values()

    @staticmethod
    def get_all_answers_of_question(question) -> List[Answer]:
        return question.all_answer_options

    def __repr__(self):
        return repr(self.q_value)


class ApplicationData:
    """Represents each application and contains the corresponding questions and their answers."""

    _app_cache = {}

    def __init__(self, app_name: str):
        self._app_id = -1
        self._app_name = app_name
        self._questionnaire = {}  # { question : answers_by_user }
        ApplicationData._app_cache.update({app_name: self})

    def update_questionnaire(self, question: Question, answers: Answer):
        self._questionnaire.update({question: answers})

    def get_answers(self, question: Question) -> Answer:
        return self._questionnaire.get(question)

    @property
    def app_name(self):
        return self._app_name

    @staticmethod
    def app_cache_items():
        """This method returns all the cached applications and their 'ApplicationData' objects."""
        return ApplicationData._app_cache.items()

    @staticmethod
    def get_application_data_by_name(app_name: str):
        return ApplicationData._app_cache.get(app_name)
