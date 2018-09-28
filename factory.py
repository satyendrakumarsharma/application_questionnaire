from model import *
from utils import *


class ApplicationFactory:
    """This is a factory class that creates the 'ApplicationData' objects"""

    app_cache = {}

    @staticmethod
    def create_app_data(app_entry):
        app_name = app_entry[0]
        app_question = app_entry[1]
        app_answers = app_entry[2]

        print('>>[ROW]<< ' + app_name + ' : ' + app_question + ' : ' + app_answers)

        if is_empty(app_name) or is_empty(app_question):
            print('[Empty Application questionnaire]')
            return

        question = Question.get_question_by_value(app_question)
        q_type = question.q_type

        if q_type == QuestionType.CHECKBOX:
            answers = []
            segregated_answers = [] if is_empty(app_answers) else app_answers.split(',')
            for app_answer in segregated_answers:
                answers.append(Answer.get_answer(app_answer))
        else:
            answers = app_answers

        app_data = ApplicationFactory.app_cache.get(app_name)
        if app_data is None:
            # a new app_data is needed only when it is not cached in dict
            app_data = ApplicationData(app_name)
            ApplicationFactory.app_cache.update({app_name: app_data})

        app_data.update_questionnaire(question, answers)

    @staticmethod
    def create_question_answer_mapping(mapping):
        q_id, q_value, ans_value, q_section, tag, q_type = mapping
        print('>>[Question]<<' + q_id + ':' + q_value + ':' + ans_value + ':' + q_section + ':' + tag + ':' + q_type)
        answer = ApplicationFactory.create_answer(ans_value, tag)
        question = Question.cache_value.get(q_value)
        if question is None:
            question = Question(q_id, q_value, str_to_type(q_type), q_section, tag)
            Question.cache_value.update({q_value: question})
        question.all_answers.append(answer)

    @staticmethod
    def create_answer(answer_value, answer_tag):
        answer = Answer.cache_value.get(answer_value)
        if answer is None:
            answer = Answer(0, answer_value, answer_tag)
            Answer.cache_value.update({answer_value: answer})
        return answer

