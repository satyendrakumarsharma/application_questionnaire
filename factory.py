from model import *


class ApplicationFactory:
    """This is a factory class that creates the 'ApplicationData' objects"""

    app_cache = {}

    @staticmethod
    def create_app_data(app_entry):
        app_name = app_entry[0]
        app_question = app_entry[1]
        app_answers = app_entry[2]

        app_data = ApplicationFactory.app_cache.get(app_name)

        if app_data is None:
            # a new app_data is needed only when it is not cached in dict
            question = ApplicationFactory.__fetch_question(app_question)
            answers = ()
            for app_answer in app_answers.split(','):
                answers += ApplicationFactory.__fetch_answer(app_answer)
            app_data = ApplicationData(question, answers)
            ApplicationFactory.app_cache.update({app_name: app_data})

    @staticmethod
    def __fetch_question(app_question):
        question = Question.question_cache.get(app_question)
        if question is None:
            question = Question(1, app_question, '')
        return question

    @staticmethod
    def __fetch_answer(app_answer):
        answers = Answer.answer_cache.get(app_answer)
        if answers is None:
            answers = Answer(1, app_answer)
        return answers


